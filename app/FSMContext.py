from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class PriceState(StatesGroup):
    waiting_for_token = State()