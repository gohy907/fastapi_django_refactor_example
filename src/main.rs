mod domain;
mod handlers;
mod models;
mod repositories;
mod schemas;
mod storages;

use crate::repositories::users::UserRepository;
use crate::storages::users::UserStorage;
use axum::Router;
use dotenvy::dotenv;
use handlers::users::{UserRouter, UsersDocs};
use schemas::users::{UserCreate, UserResponse};
use sqlx::postgres::PgPoolOptions;
use std::env;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

#[derive(OpenApi)]
#[openapi(info(title = "Blazingly-fast API!!!", version = "1.0.0"))]
struct ApiDoc;

use crate::domain::use_cases::users::create_user::RegisterUseCase;
use std::sync::Arc;

#[derive(Clone)]
pub struct AppState {
    pub register_use_case: Arc<RegisterUseCase>,
}

#[tokio::main]
async fn main() {
    dotenv().ok();

    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set in .env file");

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Не удалось подключиться к базе данных");

    println!("Успешное подключение к PostgreSQL!");
    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .expect("Failed to run database migrations");

    let user_repo = UserRepository { pool };
    let user_storage: Arc<dyn UserStorage> = Arc::new(user_repo);
    let open_api = ApiDoc::openapi().nest("/users", UsersDocs::openapi());
    let swagger_router = SwaggerUi::new("/docs").url("/api-docs/openapi.json", open_api);

    let register_use_case = Arc::new(RegisterUseCase::new(user_storage));
    let state = AppState { register_use_case };
    let base_router = Router::new()
        .nest("/users", UserRouter::new())
        .merge(swagger_router)
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();

    println!("Сервер запущен: http://localhost:3000/docs/");
    axum::serve(listener, base_router.into_make_service())
        .await
        .unwrap();
}
