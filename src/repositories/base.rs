use sqlx::{Database, Encode, Executor, FromRow, IntoArguments, Type};

pub trait IntoArgs<'q, DB: sqlx::Database, O> {
    fn names() -> &'static [&'static str];

    fn values(
        self,
        query: sqlx::query::QueryAs<'q, DB, O, DB::Arguments<'q>>,
    ) -> sqlx::query::QueryAs<'q, DB, O, DB::Arguments<'q>>;
}

pub trait Repository<DB, T>
where
    DB: Database,
    T: for<'r> FromRow<'r, DB::Row> + Send + Unpin,
{
    fn pool(&self) -> &sqlx::Pool<DB>;
    fn table_name(&self) -> &str;

    async fn get<ID>(&self, id: ID) -> Result<Option<T>, sqlx::Error>
    where
        ID: Type<DB> + for<'a> Encode<'a, DB> + Send,
        for<'a> DB::Arguments<'a>: IntoArguments<'a, DB>,
        for<'c> &'c sqlx::Pool<DB>: Executor<'c, Database = DB>,
    {
        let table = self.table_name();
        let sql = format!("SELECT * FROM {} WHERE id = $1", table);

        let result = sqlx::query_as::<DB, T>(&sql)
            .bind(id)
            .fetch_optional(self.pool())
            .await?;

        Ok(result)
    }

    async fn get_all(&self) -> Result<Vec<T>, sqlx::Error>
    where
        for<'a> DB::Arguments<'a>: IntoArguments<'a, DB>,
        for<'c> &'c sqlx::Pool<DB>: Executor<'c, Database = DB>,
    {
        let sql = format!("SELECT * FROM {}", self.table_name());

        let result = sqlx::query_as::<DB, T>(&sql).fetch_all(self.pool()).await?;

        Ok(result)
    }

    async fn create<D>(&self, data: D) -> Result<T, sqlx::Error>
    where
        D: for<'a> IntoArgs<'a, DB, T> + Send,
        for<'a> DB::Arguments<'a>: IntoArguments<'a, DB>,
        for<'c> &'c sqlx::Pool<DB>: Executor<'c, Database = DB>,
    {
        let table = self.table_name();
        let names = D::names();
        let cols = names.join(", ");

        let placeholders = (1..=names.len())
            .map(|i| format!("${}", i))
            .collect::<Vec<_>>()
            .join(", ");

        let sql = format!(
            "INSERT INTO {} ({}) VALUES ({}) RETURNING *",
            table, cols, placeholders
        );

        let query = sqlx::query_as::<DB, T>(&sql);
        let query = data.values(query);

        let result = query.fetch_one(self.pool()).await?;
        Ok(result)
    }
}
