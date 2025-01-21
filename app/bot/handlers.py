from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.states import States
from app.bot.keyboards import get_main_keyboard
from app.services.products import get_data_from_wb

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    """Обработчик команды /start."""
    await state.set_state(States.base)
    await message.answer(
        "Выберите действие из меню ниже:",
        reply_markup=get_main_keyboard(),
    )


@router.message(F.text == "Получить данные по товару")
async def get_product_data(message: Message, state: FSMContext):
    """Запрашивает артикул товара."""
    await state.set_state(States.waiting)
    await message.answer("Введите артикул товара:")


@router.message(StateFilter(States.waiting))
async def process_artikul(message: Message, state: FSMContext):
    """Обработчик ввода артикула."""
    artikul = message.text.strip()

    try:
        product = await get_data_from_wb(artikul)
        response = (
            f"Название: {product['name']}\n"
            f"Артикул: {product['artikul']}\n"
            f"Цена: {product['price']} руб.\n"
            f"Рейтинг: {product['rating']}\n"
            f"Наличие на складах: {product['total_in_stock']}"
        )

    except ValueError as e:
        response = str(e)

    await state.set_state(States.base)
    await message.answer(response, reply_markup=get_main_keyboard())
