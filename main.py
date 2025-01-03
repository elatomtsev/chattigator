import botyara
from database import DateBase

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command, or_f

bot = Bot(token=botyara.bot_token)
dp = Dispatcher()
db = DateBase()


@dp.message(Command(commands="all", prefix=["@", "/"]))
async def ping_all(message: Message):
    text = []
    for id, telegram, fullname, username in db.select_data():
        text.append(f"[{fullname}](tg://user?id={telegram})")
    await message.reply(
        # chat_id=message.chat.id,
        text=", ".join(text),
        parse_mode="Markdown",
    )
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.message_id)


# @dp.message(F.content_type.in_({ContentType.TEXT}))
@dp.message()
async def any_messages(message: Message):
    for data in db.select_data("telegram"):
        if message.from_user.id in data:
            break
    else:
        db.insert_data(
            telegram=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
        )


if __name__ == "__main__":
    db.create_table(
        "Chatters",
        id="INTEGER PRIMARY KEY",
        telegram="INTEGER",
        fullname="TEXT",
        username="TEXT",
    )

    dp.run_polling(bot)
