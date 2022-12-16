import sqlite3
import os


class LocalDB:
    DB_NAME = "app.db"
    PATH = "./app.db"
    isExist = os.path.exists(PATH)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    table = '''
            CREATE TABLE IF NOT EXISTS restaurants (
                name TEXT,
                address TEXT,
                phone_number TEXT,
                city TEXT
            );   
    '''
    if not isExist:
        print("table created")
        cursor.execute(table)

    def insert_data(self, name, address, phone_number, city):
        try:
            print("data inserted")
            self.cursor.execute(f"INSERT INTO restaurants VALUES  ('{name}','{address}','{phone_number}','{city}')")
            self.conn.commit()
        except Exception as e:
            print("data insert failed ", e)

    def get_restaurant(self, city):
        data = self.cursor.execute(f"SELECT * FROM restaurants WHERE city = '{city}'")
        return data
