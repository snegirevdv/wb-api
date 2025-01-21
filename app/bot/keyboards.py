from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Получить данные по товару")
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
