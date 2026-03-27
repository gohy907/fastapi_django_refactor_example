use crate::AppState;
use crate::domain::DBError;
use crate::{UserCreate, UserResponse};
use axum::Router;
use axum::extract::State;
use axum::extract::{Json, Path};
use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::routing::post;
use utoipa::OpenApi;

pub struct UserRouter;
impl UserRouter {
    pub fn new() -> Router<AppState> {
        Router::new()
            .route("/register", post(create_user_handler))
            .route("/aboba/{aboba}", post(aboba))
    }
}

#[derive(OpenApi)]
#[openapi(
    paths(create_user_handler, aboba),
    components(schemas(UserCreate, UserResponse))
)]
pub struct UsersDocs;

#[utoipa::path(
    post,
    path = "/aboba/{aboba}",
    params(
        ("aboba" = String, Path, description = "Абоба параметр")
    ),
    responses(
        (status = 200, description = "абоба", body = String)
    )
)]
pub async fn aboba(Path(aboba): Path<String>) -> String {
    aboba
}

#[utoipa::path(
    post,
    path = "/register",
    request_body = UserCreate,
    responses(
        (status = 201, description = "Регистрация пользователя", body = UserResponse)
    )
)]
pub async fn create_user_handler(
    State(state): State<AppState>,
    Json(payload): Json<UserCreate>,
) -> impl IntoResponse {
    match state.register_use_case.execute(payload).await {
        Ok(user) => (StatusCode::CREATED, Json(user)).into_response(),
        Err(e) => {
            match e {
                DBError::AlreadyExists => {
                    eprintln!("aboba1");
                }
                _ => {
                    eprintln!("unknown: {}", e);
                }
            }
            // eprintln!("Registration error: {:?}", e);
            (StatusCode::INTERNAL_SERVER_ERROR, "Failed to create user").into_response()
        }
    }
}
