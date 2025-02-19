import sqlite3


class DateBase:
    def __init__(self, name_db):
        self.name_db = name_db
        self.open_db()

    def open_db(self):
        # Подключаеися к БД
        self.connection = sqlite3.connect(self.name_db)
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def create_table(self, name_table: str, **column: str):
        # self.name_table = name_table

        # Добавляем колонки с именем и типом
        cols = ",\n".join([f"{name} {type}" for name, type in column.items()])

        # Создаем таблицу, если она не создана
        req = f"""CREATE TABLE IF NOT EXISTS {name_table} (\n{cols})"""
        self.cursor.execute(req)
        self.connection.commit()

    def insert_data(self, name_table: str, **row: str):
        # Формируем строчку
        names = ", ".join(row.keys())
        values = ", ".join(["?" for i in range(len(row.values()))])

        # Добавляем данные: тг айди, полное имя, юзернейм
        req = f"INSERT INTO {name_table} ({names}) VALUES ({values})"
        self.cursor.execute(req, tuple(row.values()))

        self.connection.commit()

    def select_data(self, name_table: str, column: list[str] = "*", where: str = "", order: str = ""):
        if where: where = " WHERE " + where
        if order: order = " ORDER BY " + order + " DESC"

        # Выбираем колонки, которые будем парсить
        column = ", ".join(column)

        # Возвращаем данные
        req = f"SELECT {column} from {name_table}" + where + order

        self.cursor.execute(req)

        self.connection.commit()

        return self.cursor.fetchall()

    def update_data(self, name_table: str, **kwargs: str):
        # Формируеи строку замены
        new_data = ", ".join([f"{column} = ?" for column in list(kwargs.keys())[1:]])
        # Сохраняем название колонки и данные, которые надо заменить
        name_column, need_data = list(kwargs.items())[0]

        req = f"UPDATE {name_table} SET {new_data} WHERE {name_column} = {need_data}"
        self.cursor.execute(req, tuple(kwargs.values())[1:])

        self.connection.commit()

    def close_db(self):
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
