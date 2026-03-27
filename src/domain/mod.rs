pub mod use_cases;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DBError {
    #[error("User already exists in the database")]
    AlreadyExists,

    #[error("Database error: {0}")]
    UnnamedError(String),
}
