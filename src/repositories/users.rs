use crate::models::users::User;
use crate::repositories::base::Repository;
use sqlx::{Pool, Postgres};

pub struct UserRepository<T>
where
    T: sqlx::Database,
{
    pub pool: Pool<T>,
}

impl Repository<sqlx::Postgres, User> for UserRepository<sqlx::Postgres> {
    fn pool(&self) -> &Pool<Postgres> {
        &self.pool
    }
    fn table_name(&self) -> &str {
        "users"
    }
}
