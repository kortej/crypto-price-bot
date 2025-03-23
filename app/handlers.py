import logging
import requests
import app.api_requests as aq
import app.FSMContext as fsm
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Викличте функцію /price щоб дізнатися ціну однієї монети!\nАбо напишіть назву токена і кількість в форматі: токен кіл-сть!")


@router.message(Command('price'))
async def cmd_price(message: Message, state: fsm.FSMContext):
    # Встановлюємо стан "waiting_for_token"
    await state.set_state(fsm.PriceState.waiting_for_token)
    logger.info(f"Стан встановлено: waiting_for_token для користувача {message.from_user.id}")
    await message.answer('Введіть токен (наприклад, BTC, ETH): ')


@router.message(fsm.PriceState.waiting_for_token)
async def process_token(message: Message, state: fsm.FSMContext):
    # Отримуємо введений користувачем токен
    token = message.text.strip().upper()  # Прибираємо зайві пробіли і переводимо у верхній регістр
    logger.info(f"Отримано токен: {token} від користувача {message.from_user.id}")

    # Параметри для запиту до CoinMarketCap API
    params = {
        "symbol": token,
        "convert": "USD",
    }

    try:
        logger.info(f"Робимо запит до API для токена: {token}")
        # Робимо запит до API
        response = requests.get(aq.CMC_URL, headers=aq.headers, params=params)
        data = response.json()
        logger.info(f"Відповідь API: {data}")

        # Перевіряємо, чи є дані у відповіді
        if "data" in data and token in data["data"]:
            price = data["data"][token][0]["quote"]["USD"]["price"]
            await message.answer(f"Ціна токена {token}: {price:.2f} USD")
        else:
            await message.answer(f"Токен {token} не знайдено. Перевірте правильність введення.")

    except Exception as e:
        logger.error(f"Помилка при запиті до API: {e}")
        await message.answer("Не вдалося отримати дані про ціну. Спробуйте пізніше.")

    # Скидаємо стан після завершення обробки
    await state.clear()
    logger.info(f"Стан скинуто для користувача {message.from_user.id}")


@router.message(F.text)
async def price_crypto(message: Message):
    parts = message.text.strip().split()

    if len(parts) == 2:
        token = parts[0].upper()
        try:
            amount = float(parts[1])
        except ValueError:
            await message.answer("Невірний формат\nВірний формат (приклад): BTC 1")
            return
        

        params = {
            "symbol": token,
            "convert": "USD",
        }

        try:
            response = requests.get(aq.CMC_URL, headers=aq.headers, params=params)
            data = response.json()

            if "data" in data and token in data["data"]:
                price = data['data'][token][0]['quote']["USD"]["price"]
                total_price = price * amount
                await message.answer(f"Ціна {amount} {token}: {total_price:.2f} USD")
            else:
                await message.answer(f"Токен {token} не знайдено. Перевірте правильність введення.")

        except Exception as e:
            await message.answer("Не вдалося отримати дані про ціну. Спробуйте пізніше.")
        

    
