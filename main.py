import botyara
from database import DateBase

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command, or_f

bot = Bot(token=botyara.bot_token)
dp = Dispatcher()
db = DateBase("database.db")


def check_exist_data(name_table: str, message: Message, column: list[str]) -> bool:
    # Извлекаем все telegram_id и ищем есть необходимый
    for telegram in db.select_data(name_table, ["telegram"]):
        if message.chat.id in telegram:
            return True
    return False


@dp.message(Command(commands="all", prefix=["@", "/"]))
async def ping_all(message: Message):
    # Добавляем chat к telegram_id, удалив минус, потому что sqlite не позволяет создать таблицу, где есть число и минус
    chat_id = "chat" + str(message.chat.id).strip("-")

    # Сюда будем складывать строки с ссылками на участников для их отметки
    text = []

    for id, telegram, fullname, username in db.select_data(chat_id):
        # Не отмечать бота
        if telegram == bot.id:
            continue
        text.append(f"[{fullname}](tg://user?id={telegram})")

    # Отмечаем всех участников
    await message.reply(
        text=", ".join(text),
        parse_mode="Markdown",
    )
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message()
async def any_message(message: Message):
    # Добавляем chat к telegram_id, удалив минус, потому что sqlite не позволяет создать таблицу, где есть число и минус
    chat_id = "chat" + str(message.chat.id).strip("-")

    # Создаём таблицу, если она не существует, с участниками чата
    db.create_table(
        chat_id,
        id="INTEGER PRIMARY KEY",
        telegram="INTEGER",
        fullname="TEXT",
        username="TEXT",
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
        )
    else:
        db.update_data(
            chat_id,
            telegram=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
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
