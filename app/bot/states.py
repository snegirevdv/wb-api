from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    """Состояния бота."""

    base = State()
    waiting = State()
