import botyara
from database import DateBase

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command, or_f

bot = Bot(token=botyara.bot_token)
dp = Dispatcher()
db = DateBase("database.db")


def check_exist_data(name_table: str, message: Message, column: list[str]) -> bool:
    # Если проверяется таблица с чатами, то искать айди чата, если таблица с участниками, то искать айди участника
    id = message.from_user.id if str(message.chat.id).strip("-") in name_table else message.chat.id

    # Извлекаем все telegram_id и ищем необходимый
    for telegram in db.select_data(name_table, column):
        if id in telegram:
            return True
    return False


@dp.message(Command(commands="all", prefix=["@", "/"]))
async def ping_all(message: Message):
    # Добавляем chat к telegram_id, удалив минус, потому что sqlite не позволяет создать таблицу, где есть число и минус
    chat_id = "chat" + str(message.chat.id).strip("-")

    # Сюда будем складывать строки с ссылками на участников для их отметки
    text = []

    for id, telegram, fullname, *other in db.select_data(chat_id):
        text.append(f"[{fullname}](tg://user?id={telegram})")

    # Отмечаем всех участников
    await message.reply(
        text=", ".join(text),
        parse_mode="Markdown",
    )
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message(Command(commands="stat"))
async def stat_messages(message: Message):
    # Добавляем chat к telegram_id, удалив минус, потому что sqlite не позволяет создать таблицу, где есть число и минус
    chat_id = "chat" + str(message.chat.id).strip("-")

    text = ["*Статистика отправленных сообщений:*"]

    for fullname, cnt_messages in db.select_data(chat_id, ["fullname", "cnt_messages"], order=f"cnt_messages"):
        text.append(f"{fullname} - {cnt_messages}")

    await message.reply(text="\n".join(text), parse_mode="Markdown")


# Исключаем сообещения от бота и группы (например, когда начинается видеочат)
@dp.message(lambda message: message.from_user.is_bot == False)
async def any_message(message: Message):
    # Не отмечать бота
    if message.from_user.id == bot.id:
        return False

    # Добавляем chat к telegram_id, удалив минус, потому что sqlite не позволяет создать таблицу, где есть число и минус
    chat_id = "chat" + str(message.chat.id).strip("-")

    # Создаём таблицу, если она не существует, с участниками чата
    db.create_table(
        chat_id,
        id="INTEGER PRIMARY KEY",
        telegram="INTEGER",
        fullname="TEXT",
        username="TEXT",
        cnt_messages="INTEGER",
    )

    # Если чат уже есть в таблице, то обновляем данные (может быть, что-то изменилось)
    if not check_exist_data("Chatters", message, ["telegram"]):
        db.insert_data(
            "Chatters",
            telegram=message.chat.id,
            name=message.chat.full_name,
            username=message.chat.username,
        )
    else:
        db.update_data(
            "Chatters",
            telegram=message.chat.id,
            name=message.chat.full_name,
            username=message.chat.username,
        )

    # Если участник есть в таблице, то обновляем его данные
    if not check_exist_data(chat_id, message, ["telegram"]):
        db.insert_data(
            chat_id,
            telegram=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
            cnt_messages=0,
        )
    else:
        # Узнаём количество отправленных сообщений и обновляем данные, прибавив 1
        cnt = db.select_data(chat_id, ["cnt_messages"], f"telegram = {message.from_user.id}")[0][0]
        db.update_data(
            chat_id,
            telegram=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
            cnt_messages=cnt + 1,
        )


if __name__ == "__main__":
    db.create_table(
        "Chatters",
        id="INTEGER PRIMARY KEY",
        telegram="INTEGER",
        name="TEXT",
        username="TEXT",
    )
    dp.run_polling(bot)
