import sqlite3


class DateBase:
    def __init__(self):
        self.open_table()

    def open_table(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    def create_table(self, name_table: str, **column: str):
        self.name_table = name_table
        # Добавляем колонки с именем и типом
        cols = ",\n".join([f"{name} {type}" for name, type in column.items()])
        # Создаем таблицу, если она не создана
        req = f"""CREATE TABLE IF NOT EXISTS {self.name_table} (\n{cols})"""

        self.cursor.execute(req)

    def insert_data(self, **row: str):
        self.open_table()
        # Формируем строчку
        names = ", ".join(row.keys())
        values = ", ".join(["?" for i in range(len(row.values()))])
        # Добавляем данные: тг айди, полное имя, юзернейм
        req = f"INSERT INTO {self.name_table} ({names}) VALUES ({values})"
        #print(req)
        self.cursor.execute(req, tuple(row.values()))
        self.close_table()

    def select_data(self, column="*"):
        self.open_table()
        req = f"SELECT {column} from {self.name_table}"

        self.cursor.execute(req)
        return self.cursor.fetchall()
        self.close_table()

    def close_table(self):
        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    db = DateBase()
    db.create_table(
        name_table="Chatters",
        id="INTEGER PRIMARY KEY",
        telegram="INTEGER",
        fullname="TEXT NOT NULL",
        username="TEXT NOT NULL",
    )
    # db.insert_data(telegram=2132131, fullname="AlexGolotin", username="penis")
    # db.cursor.execute(f'SELECT telegram from Chatters')
    db.select_data("telegram")
    for i in db.cursor.fetchall():
        print(*i)
    db.close_table()
