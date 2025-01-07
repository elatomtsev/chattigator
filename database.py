import sqlite3


class DateBase:
    def __init__(self, name_db):
        self.name_db = name_db
        self.open_table()

    def open_table(self):
        # Подключаеися к БД
        self.connection = sqlite3.connect(self.name_db)
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
        self.cursor.execute(req, tuple(row.values()))
        self.close_table()

    def select_data(self, column: list[str] = "*"):
        self.open_table()

        # Выбираем колонки, которые будем парсить
        column = ", ".join(column)

        # Возвращаем данные
        req = f"SELECT {column} from {self.name_table}"
        self.cursor.execute(req)
        return self.cursor.fetchall()

    def update_data(self, key_name, key_data, **kwargs: str):
        self.open_table()

        # Формируеи строку замены
        new_data = ", ".join([f"{column} = ?" for column in kwargs.keys()])

        req = f"UPDATE {self.name_table} SET {new_data} WHERE {key_name} = {key_data}"
        self.cursor.execute(req, tuple(kwargs.values()))

        self.close_table()

    def close_table(self):
        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    db = DateBase("1.db")
    db.create_table(
        name_table="Chatters",
        id="INTEGER PRIMARY KEY",
        telegram="INTEGER",
        fullname="TEXT NOT NULL",
        username="TEXT NOT NULL",
    )
    # db.insert_data(telegram=2132131, fullname="AlexGolotin", username="penis")
    # db.cursor.execute(f'SELECT telegram from Chatters')
    db.select_data(["telegram"])
    db.update_data("telegram", 779490247, fullname="alexander", username="sashka")
