use axum::{
    Router,
    body::Bytes,
    extract::{Extension, Json, Path, Query, Request},
    http::header::HeaderMap,
    routing::post,
};
use serde_json::Value;
use std::collections::HashMap;

// `Path` gives you the path parameters and deserializes them. See its docs for
// more details
async fn path(Path(user_id): Path<u32>) {}

// `Query` gives you the query parameters and deserializes them.
async fn query(Query(params): Query<HashMap<String, String>>) {}

// `HeaderMap` gives you all the headers
async fn headers(headers: HeaderMap) {}

// `String` consumes the request body and ensures it is valid utf-8
async fn string(body: String) {
    println!("{}", body);
}

// `Bytes` gives you the raw request body
async fn bytes(body: Bytes) {}

// We've already seen `Json` for parsing the request body as json
async fn json(Json(payload): Json<Value>) {}

// `Request` gives you the whole request for maximum control
async fn request(request: Request) {}

// `Extension` extracts data from "request extensions"
// This is commonly used to share state with handlers
async fn extension(Extension(state): Extension<State>) {}

#[derive(Clone)]
struct State {/* ... */}

#[tokio::main]
async fn main() {
    // build our application with a single route
    let app = Router::new()
        .route("/path/{user_id}", post(path))
        .route("/query", post(query))
        .route("/string", post(string))
        .route("/bytes", post(bytes))
        .route("/json", post(json))
        .route("/request", post(request))
        .route("/extension", post(extension));

    // run our app with hyper, listening globally on port 3000
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
