use crate::models::users::User;
use crate::repositories::base::IntoArgs;
use crate::repositories::base::Repository;
use crate::repositories::users::UserRepository;
use crate::schemas::users::UserCreate;
use async_trait::async_trait;
use sqlx::Postgres;

#[async_trait]
pub trait UserStorage: Send + Sync {
    async fn find_user(&self, id: i32) -> Result<Option<User>, sqlx::Error>;
    async fn create_user(&self, user: UserCreate) -> Result<User, sqlx::Error>;
}

impl<'q> IntoArgs<'q, Postgres, User> for UserCreate {
    fn names() -> &'static [&'static str] {
        &["username", "password"]
    }

    fn values(
        self,
        query: sqlx::query::QueryAs<
            'q,
            Postgres,
            User,
            <Postgres as sqlx::Database>::Arguments<'q>,
        >,
    ) -> sqlx::query::QueryAs<'q, Postgres, User, <Postgres as sqlx::Database>::Arguments<'q>> {
        query.bind(self.username).bind(self.password)
    }
}

#[async_trait]
impl UserStorage for UserRepository<sqlx::Postgres> {
    async fn find_user(&self, id: i32) -> Result<Option<User>, sqlx::Error> {
        self.get(id).await
    }
    async fn create_user(&self, user: UserCreate) -> Result<User, sqlx::Error> {
        self.create(user).await
    }
}
