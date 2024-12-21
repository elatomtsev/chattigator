import sqlite3


class DateBase:
    def __init__(self, name_table: str):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.name_table = name_table

    def create_table(self, **column: str):
        # Добавляем колонки с именем и типом
        cols = ",\n".join([f"{name} {type}" for name, type in column.items()])
        # Создаем таблицу, если она не создана
        req = f"""CREATE TABLE IF NOT EXISTS {self.name_table} (\n{cols})"""

        self.cursor.execute(req)

    def insert_data(self, **row: str):
        names = ", ".join(row.keys())
        values = ", ".join(["?" for i in range(len(row.values()))])
        req = f"INSERT INTO {self.name_table} ({names}) VALUES ({values})"

        self.cursor.execute(req, tuple(row.values()))

    def close_table(self):
        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    db = DateBase("Chatters")
    db.create_table(
        id="INTEGER PRIMARY KEY",
        telegram="INTEGER",
        fullname="TEXT NOT NULL",
        username="TEXT NOT NULL",
    )
    print()
    db.insert_data(telegram=2132131, fullname="AlexGolotin", username="penis")
    db.close_table()
