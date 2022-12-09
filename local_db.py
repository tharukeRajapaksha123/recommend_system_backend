from simple_sqlite import SimpleSqlite


class LocalDB:
    DB_NAME = "app.db"
    ssql = SimpleSqlite(DB_NAME)
    result, message = ssql.create_database()