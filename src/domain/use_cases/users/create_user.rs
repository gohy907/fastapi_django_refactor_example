use std::sync::Arc;

use crate::{
    domain::DBError, models::users::User, schemas::users::UserCreate, storages::users::UserStorage,
};

pub struct RegisterUseCase {
    storage: Arc<dyn UserStorage>,
}

impl RegisterUseCase {
    pub fn new(storage: Arc<dyn UserStorage>) -> Self {
        Self { storage }
    }
    pub async fn execute(&self, user_in: UserCreate) -> Result<User, DBError> {
        match self.storage.create_user(user_in).await {
            Err(e) => Err(DBError::UnnamedError(e.to_string())),
            Ok(user) => Ok(user),
        }
    }
}
