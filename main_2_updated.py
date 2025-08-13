# -*- coding: utf-8 -*-

# ЗАМЕНИТЬ ВЕСЬ БЛОК ИМПОРТОВ
import asyncio
import time
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
import aiosqlite
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from collections import Counter
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.state import StateFilter
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
import traceback
import html
from aiogram.types import CallbackQuery
from openai import OpenAI
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from functools import wraps
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner
import translations_2
from datetime import datetime, timedelta, timezone
import datetime
import asyncio
import logging # Для логирования
import traceback # Для вывода полного трейсбека
from translations_2 import PROMPT_KIT_EN
from aiogram.types import InputFile
from aiogram.types import BufferedInputFile
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout
import logging  # Для теста запросов

# НОВЫЕ ИМПОРТЫ
from deep_translator import GoogleTranslator

# main_2_updated.py (ДОБАВИТЬ К ИМПОРТАМ)
import httpx
from bybit_api import get_market_data
# Добавьте этот импорт к остальным из translations_2
from translations_2 import PROMPT_MARKET_KIT_RU, PROMPT_TF_KIT
import pandas as pd
from bybit_api import get_market_data, plot_chart, calculate_advanced_metrics, get_stock_data, aggregate_kline, load_coins_list, BASE_URL, get_coin_id
import re
import aiogram.exceptions as aio_exc  # Добавь к imports (для TelegramNetworkError)
import logging
from io import BytesIO
import pandas_ta as ta  # Убедитесь, что библиотека установлена (pip install pandas_ta)
from deep_translator import GoogleTranslator  # Для перевода, если нужно
import yfinance as yf
from aiogram.client.default import DefaultBotProperties
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# client = OpenAI(
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNmM2Y3M2UzLTJkYTItNDQzZC1iYWRkLWQ1YTcyMzA3YjhiNiIsImlzRGV2ZWxvcGVyIjp0cnVlLCJpYXQiOjE3NTA1Nzg3NzAsImV4cCI6MjA2NjE1NDc3MH0.gDY05uWtqB3DnJKlhbU36Lrahtd3JEcQGWnYfdgw0LM",
#     base_url="https://bothub.chat/api/v2/openai/v1",
# )
client = OpenAI(
    api_key=os.getenv('GPT_API_KEY'),
    base_url="https://bothub.chat/api/v2/openai/v1",
)

# API_TOKEN = '8027101036:AAGQjcGPo6eh7zzkfvcdixRC5FR2pk6LmAY'
# API_TOKEN = '7844407804:AAHRAMGDGcZqTJ-C5tWkOCZuESl6LS08Qww'
API_TOKEN = os.getenv('API_TOKEN_TG_BOT')

# session = AiohttpSession(timeout=ClientTimeout(total=60))

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

logging.basicConfig(level=logging.INFO)
# ============================================
# ГЛОБАЛЬНЫЙ ОБРАБОТЧИК ОТМЕНЫ - РАЗМЕСТИТЬ ЗДЕСЬ
# ============================================
@router.message(Command("cancel"))
async def cancel_handler(msg: types.Message, state: FSMContext):
    """
    Этот хэндлер отменяет любое активное состояние (FSM)
    и удаляет связанные сообщения.
    """
    user_id = msg.from_user.id
    lang = await get_user_lang(user_id)
    current_state = await state.get_state()
    if current_state is None:
        # Для UX можно либо ничего не отвечать, либо отправить тихое уведомление
        # и удалить его через пару секунд, чтобы не засорять чат.
        return

    # Удаляем все сообщения, которые бот и пользователь отправляли
    # в рамках этого диалога FSM.
    await delete_fsm_messages(msg.chat.id, state)

    # Полностью очищаем состояние пользователя.
    await state.clear()

    # Отправляем подтверждение, которое потом удалится.
    confirmation = await msg.answer(translations_2.translations[lang]['cancel_disvie'], reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(2)

    try:
        # Удаляем сообщение "Действие отменено"
        await bot.delete_message(msg.chat.id, confirmation.message_id)
        # Удаляем саму команду /cancel
        await bot.delete_message(msg.chat.id, msg.message_id)
    except (TelegramBadRequest, TelegramForbiddenError):
        # Игнорируем ошибки, если сообщения уже были удалены или недоступны
        pass

# Словарь для хранения последних сообщений бота для каждого пользователя
last_bot_messages = {}
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# photo_statistika_bot = FSInputFile("statistika_bot.png")
# photo_otzivi = FSInputFile("otzivi.png")
# photo_tip_prognoza = FSInputFile("tip_prognoza.png")
# photo_katalog = FSInputFile("katalog.png")
# photo_katalog_prognoz = FSInputFile("katalog_prognoz.png")
# photo_katalog_subscriptions = FSInputFile("katalog_subscriptions.png")
# photo_profil = FSInputFile("profil.png")
photo_admin_panel = FSInputFile("admin.png")
photo_statistika_traffer = FSInputFile("statistika_tr.png")
photo_promo = FSInputFile("promokod.png")
photo_iaziki = FSInputFile("iaziki.png")

BOT_USERNAME = "SportNeyroAnalitikbot"

ADMIN_ID: set[int] = {2122289037, 1244773560, 5099581636}
DETAIL_STORE: dict[int, str] = {}

# ──────────────────────────────────────────────────────────────────────────
PRICES = {
    # Обычные прогнозы:
    '1_ob_prognoz': 59,  # 30₽ за 1 обычный прогноз
    '5_ob_prognoz': 249,  # 140₽ за 5 обычных прогнозов
    '15_ob_prognoz': 699,  # 390₽ за 15 обычных прогнозов

    # VIP-прогнозы:
    '1_rach_prognoz': 99,  # 60₽ за 1 VIP-прогноз
    '5_rach_prognoz': 399,  # 280₽ за 5 VIP-прогнозов
    '15_rach_prognoz': 1159,  # 780₽ за 15 VIP-прогнозов

    # Подписки:
    'standart': 199,  # 499₽ за Standart (неделя; выдаёт 5 об., 0 VIP)
    'medium': 999,  # 875₽ за medium (неделя; выдаёт 12 об., 6 VIP)
    'premium': 1899,  # 1299₽ за Premium (две недели; выдаёт 30 об., 15 VIP)
}

VIP_PREDICTION_PRICE = 5  # Первичная цена VIP-прогноза
REGULAR_PREDICTION_PRICE = 2  # Первичная цена обычного прогноза

# ───────────────────────────────────────────────────────────────────────────────
async def polling_with_retry(dp: Dispatcher, bot: Bot, max_retries: int = 10):
    retries = 0
    while retries < max_retries:
        try:
            await dp.start_polling(bot)
            break
        except aio_exc.TelegramNetworkError as e:
            logging.error(f"Polling error: {e}. Retry {retries+1}/{max_retries}")
            await asyncio.sleep(min(60, 2 ** retries))  # Max sleep 60s
            retries += 1
        except Exception as e:
            logging.error(f"Fatal polling error: {e}\n{traceback.format_exc()}")
            break
    if retries >= max_retries:
        logging.error("Max retries reached. Shutting down.")


async def _show_traffer_profile(
        user_id: int,
        trafer_name: str,
        t_id: str,
        trafer_username: str,
        t_promo: str,
        t_telefon: str,
        t_karta: str,
        t_kripta: str,
        crypto_network: str,
        pay_model: str,
        pay_value: int,
        pay_link: str,
        invite_link: str,
        leads: int,
        users: list[int],
        dst: types.CallbackQuery | types.Message,
        is_admin: bool = True
):
    # Считаем статистику
    total, paid, balance = await get_traffer_balance(t_id)

    # Читаем человеко-понятные названия моделей
    model_names = {
        'model_bot': f"₽{pay_value} за подписчика",
        'model_percent': f"{pay_value}% от трат",
        'model_channel': f"Фиксированная плата {pay_value}₽"
    }
    human_model = model_names.get(pay_model, pay_model)

    # Формируем текст (одинаковый для админ- и трафферской панели)
    lang = await get_user_lang(user_id)
    raw = translations_2.translations[lang]['traff_info'].format(
        trafer_name=trafer_name,
        t_id=t_id,
        t_promo=t_promo,
        t_telefon=t_telefon,
        t_karta=t_karta,
        t_kripta=t_kripta,
        t_username=trafer_username,
        crypto_network=crypto_network,
        human_model=human_model,
        leads=leads,
        total=total,
        paid=paid,
        balance=balance
    )
    text_lines = [line for line in raw.strip().split('\n')]


    # Если модель «₽ за подписчика» или «₽ за канал», показываем реф-ссылку
    if pay_model in ['model_bot', 'model_channel'] and invite_link:
        text_lines.insert(10, translations_2.translations[lang]['traff_id_kanala'].format(pay_link=pay_link))
        text_lines.insert(11, translations_2.translations[lang]['traff_priglos_ssilka'].format(invite_link=invite_link))

    text = "\n".join(text_lines)

    # Формируем кнопки в зависимости от контекста
    if is_admin:
        # Определяем callback_data для кнопки "Обновить" в зависимости от pay_model
        update_callback = f"trafer_update:{t_id}"
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text=translations_2.translations[lang]['obnovit_traf_info'],
                callback_data=update_callback  # Используем переменную здесь
            )],  # Добавляем кнопку "Обновить"
            [types.InlineKeyboardButton(
                text=translations_2.translations[lang]['edit_traffera'],
                callback_data=f"edit_traffer:{t_id}"
            )],
            [types.InlineKeyboardButton(
                text=translations_2.translations[lang]['del_traffera'],
                callback_data=f"delete_trafer_{trafer_name}"
            )],
            [types.InlineKeyboardButton(
                text=translations_2.translations[lang]['back'],
                callback_data='baza_traferov'
            )]
        ])
    else:
        # Определяем callback_data для кнопки "Обновить" в зависимости от pay_model
        update_callback = f"trafer_update:{t_id}"
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text=translations_2.translations[lang]['obnovit_traf_info'],
                callback_data=update_callback  # Используем переменную здесь
            )],  # Добавляем кнопку "Обновить"
            [types.InlineKeyboardButton(
                text=translations_2.translations[lang]['vivisti_money'],
                callback_data='withdraw'
            )],
            [types.InlineKeyboardButton(
                text=translations_2.translations[lang]['back_traff_panel'],
                callback_data='close_trafer_panel'
            )]
        ])
        # Отправляем или редактируем
    if isinstance(dst, types.Message):
        await send_photo_with_delete(dst.chat.id, photo_statistika_traffer, text, reply_markup=markup)
    else:
        await send_photo_with_delete(dst.from_user.id, photo_statistika_traffer, text, reply_markup=markup)
        await dst.answer()

# ──────────────────────────────────────────────────────────────────────────


# ============================================
# меню команд:
# ============================================
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram.exceptions import TelegramBadRequest


# async def setup_bot_commands():
#     # Команды по умолчанию для всех пользователей
#     await bot.set_my_commands(
#         [BotCommand(command="start", description=translations_2.translations[lang]['command_start'])],
#         scope=BotCommandScopeDefault()
#     )
#
#     # Словарь для накопления команд по конкретному чату
#     # Ключ: chat_id (int), значение: набор команд (тип BotCommand)
#     chat_commands = {}
#
#     # Функция для добавления команды в набор для данного чата
#     def add_command(chat_id: int, command: BotCommand):
#         if chat_id not in chat_commands:
#             chat_commands[chat_id] = {}
#         # Используем имя команды как ключ, чтобы избежать дублирования
#         chat_commands[chat_id][command.command] = command
#
#     # Добавляем команды для администраторов
#     admin_ids = [2122289037, 1244773560, 5099581636]
#     for admin_id in admin_ids:
#         try:
#             # Если админ уже есть, просто добавляем нужные команды
#             add_command(admin_id, BotCommand(command="admin", description=translations_2.translations[lang]['command_admin']))
#         except Exception as e:
#             print(f"Ошибка при добавлении команд для admin с chat_id={admin_id}: {e}")
#
#     # Добавляем команды для трафферов
#     async with aiosqlite.connect('traffers.db') as db:
#         async with db.execute("SELECT trafer_id FROM traffers") as cursor:
#             rows = await cursor.fetchall()
#             for (trafer_id,) in rows:
#                 try:
#                     chat_id = int(trafer_id)
#                 except ValueError:
#                     print(f"Пропущен trafer_id='{trafer_id}': невозможно преобразовать в int")
#                     continue
#
#                 try:
#                     add_command(chat_id, BotCommand(command="start", description=translations_2.translations[lang]['command_start']))
#                     add_command(chat_id, BotCommand(command="traffer", description=translations_2.translations[lang]['command_traffer']))
#                 except Exception as e:
#                     print(f"Ошибка при добавлении команд для trafer с chat_id={chat_id}: {e}")
#
#     # Устанавливаем команды для каждого чата из нашего словаря
#     for chat_id, commands_dict in chat_commands.items():
#         commands_list = list(commands_dict.values())
#         try:
#             await bot.set_my_commands(
#                 commands_list,
#                 scope=BotCommandScopeChat(chat_id=chat_id)
#             )
#         except TelegramBadRequest as e:
#             print(f"Не удалось установить команды для chat_id={chat_id}: {e}")
#

# ============================================
# Инициализация базы данных пользователей
# ============================================
async def init_databases():
    """Инициализирует все базы данных при старте бота."""
    async with aiosqlite.connect('traffer_payouts.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS withdraw_notifications (
                trafer_id INTEGER,
                amount INTEGER,
                admin_id INTEGER,
                message_id INTEGER
            )
        ''')
        await db.commit()

    async with aiosqlite.connect('partners.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS partners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL UNIQUE, title TEXT, username TEXT, description TEXT, link TEXT
            )""")
        await db.commit()

    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, name TEXT, subscription TEXT DEFAULT '-', time INTEGER DEFAULT 0,
                ob_prognoz INTEGER DEFAULT 0, rach_prognoz INTEGER DEFAULT 0, ob_vr_prognoz INTEGER DEFAULT 0,
                rach_vr_prognoz INTEGER DEFAULT 0, last_active INTEGER DEFAULT 0, lang TEXT, referred_by INTEGER DEFAULT NULL,
                has_made_purchase INTEGER DEFAULT 0
            )''')
        # Таблица для использованных промокодов (если ее нет)
        await db.execute('''
            CREATE TABLE IF NOT EXISTS used_promocodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, promokod TEXT,
                UNIQUE(user_id, promokod)
            )''')
        await db.commit()
    async with aiosqlite.connect('payments.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, type TEXT,
                amount INTEGER, count INTEGER, timestamp INTEGER, bot TEXT
            )''')
        await db.commit()
    async with aiosqlite.connect('traffers.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS traffers (
                id INTEGER PRIMARY KEY AUTOINCREMENT, trafer_name TEXT, trafer_id TEXT, trafer_promo TEXT,
                trafer_telefon TEXT, trafer_karta TEXT, trafer_kripta TEXT, pay_model TEXT,
                pay_value INTEGER, pay_link TEXT, invite_link TEXT, last_subscribers INTEGER DEFAULT 0, trafer_username TEXT, crypto_network TEXT
            )''')
        await db.commit()
    async with aiosqlite.connect('promocodes.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS promocodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, promokod TEXT, ob_prognoz INTEGER, rach_prognoz INTEGER,
                subscription TEXT, kolichestvo_ispolzovaniy INTEGER
            )''')
        await db.commit()
    async with aiosqlite.connect('traffer_payouts.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS traffer_payouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, trafer_id INTEGER, amount INTEGER,
                timestamp INTEGER, status TEXT
            )''')
        await db.commit()


# ============================================
# Функции для работы с базой пользователей
# ============================================
# Добавление пользователя
async def add_user(user_id: int, user_name: str, referred_by: int = None):
    lang = await get_user_lang(user_id)
    async with aiosqlite.connect('users.db') as db:
        # Проверяем, существует ли пользователь
        async with db.execute("SELECT id FROM users WHERE id = ?", (user_id,)) as cursor:
            if await cursor.fetchone():
                # Пользователь существует, обновляем referred_by, если оно NULL
                if referred_by is not None:
                    await db.execute("UPDATE users SET referred_by = ? WHERE id = ? AND referred_by IS NULL", (referred_by, user_id))
                    # logging.info(f"Обновлён referred_by для пользователя {user_id} на {referred_by}")
            else:
                # Пользователь не существует, добавляем нового
                # await db.execute("INSERT INTO users (id, name, lang, referred_by) VALUES (?, ?, ?, ?)", (user_id, user_name, lang, referred_by))
                # logging.info(f"Добавлен новый пользователь {user_id} с referred_by {referred_by}")
                # В add_user, вместо INSERT VALUES
                await db.execute("INSERT OR IGNORE INTO users (id, name, lang, referred_by) VALUES (?, ?, ?, ?)",
                                 (user_id, user_name, lang, referred_by))
        await db.commit()

async def add_traffer(trafer_name: str, trafer_id: str, trafer_promo: str,
                      trafer_telefon: str, trafer_karta: str, trafer_kripta: str,
                      pay_model: str, pay_value: int, pay_link: str, invite_link: str, trafer_username: str, crypto_network: str):
    async with aiosqlite.connect('traffers.db') as db:
        await db.execute('''
            INSERT INTO traffers (
                trafer_name, trafer_id, trafer_promo, trafer_telefon, trafer_karta, trafer_kripta,
                pay_model, pay_value, pay_link, invite_link, trafer_username, crypto_network
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (trafer_name, trafer_id, trafer_promo, trafer_telefon, trafer_karta, trafer_kripta,
              pay_model, pay_value, pay_link, invite_link, trafer_username, crypto_network))
        await db.commit()


async def add_promocode(promokod: str, ob_prognoz: int, rach_prognoz: int,
                        subscription: str, kolichestvo_ispolzovaniy: int):
    async with aiosqlite.connect('promocodes.db') as db:
        await db.execute('''
            INSERT INTO promocodes (promokod, ob_prognoz, rach_prognoz, subscription, kolichestvo_ispolzovaniy)
            VALUES (?, ?, ?, ?, ?)
        ''', (promokod, ob_prognoz, rach_prognoz, subscription, kolichestvo_ispolzovaniy))
        await db.commit()


async def check_partners_subscription(user_id: int) -> bool:
    async with aiosqlite.connect("partners.db") as db:
        async with db.execute("SELECT chat_id FROM partners") as cursor:
            rows = await cursor.fetchall()

    for (chat_id,) in rows:
        try:
            member = await bot.get_chat_member(chat_id, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        except Exception:
            return False
    return True

# Подсчёт приглашённых друзей
async def get_referred_count(user_id: int) -> int:
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

# Проверка первой покупки
async def check_first_purchase(user_id: int) -> bool:
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT has_made_purchase FROM users WHERE id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] == 0 if result else False

# Выдача реферальной награды
async def give_referral_reward(user_id: int):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT has_made_purchase, referred_by FROM users WHERE id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
        if result:
            has_made_purchase, referred_by = result
            # logging.info(f"Пользователь {user_id}: has_made_purchase={has_made_purchase}, referred_by={referred_by}")
            if has_made_purchase == 0 and referred_by is not None:
                # logging.info(f"Начисляем награду для пользователя {user_id} и реферала {referred_by}")
                await db.execute("UPDATE users SET rach_prognoz = rach_prognoz + 1 WHERE id = ?", (user_id,))
                await db.execute("UPDATE users SET rach_prognoz = rach_prognoz + 1 WHERE id = ?", (referred_by,))
                user_lang = await get_user_lang(user_id)
                await bot.send_message(user_id, translations_2.translations[user_lang]['referral_reward'].format(amount=1))
                referrer_lang = await get_user_lang(referred_by)
                await bot.send_message(referred_by, translations_2.translations[referrer_lang]['referral_reward'].format(amount=1))
                await db.execute("UPDATE users SET has_made_purchase = 1 WHERE id = ?", (user_id,))
                await db.commit()
                await process_profile_redirect(referred_by)
            # else:
                # logging.info(f"Награда не начислена: пользователь {user_id} уже купил или не был приглашён")
            # Устанавливаем has_made_purchase = 1 для любой первой покупки
            if has_made_purchase == 0:
                await db.execute("UPDATE users SET has_made_purchase = 1 WHERE id = ?", (user_id,))
                await db.commit()
        # else:
            # logging.warning(f"Пользователь {user_id} не найден в базе данных")

def require_subscription(next_action: str):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(event, *args, **kwargs):
            user_id = (event.from_user.id
                       if isinstance(event, (types.Message, types.CallbackQuery))
                       else event.chat.id)
            if not await check_partners_subscription(user_id):
                # отправляем партнёров и «маркируем» callback_data
                await send_partners_list(user_id, next_action)
                return
            # если подписан — переходим к изначальному хэндлеру
            return await handler(event, *args, **kwargs)

        return wrapper

    return decorator


async def get_user(user_id: int):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE id = ?', (user_id,)) as cursor:
            return await cursor.fetchone()


async def update_ob_prognoz(user_id: int, amount: int):
    async with aiosqlite.connect('users.db') as db:
        await db.execute(
            'UPDATE users SET ob_prognoz = ob_prognoz + ? WHERE id = ?',
            (amount, user_id)
        )
        await db.commit()

async def get_user_lang(user_id: int) -> str | None:
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT lang FROM users WHERE id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row and row[0]:
                return row[0]  # 'ru' или 'en'
            else:
                return None  # ещё не выбрано

async def set_user_lang(user_id: int, lang: str):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("UPDATE users SET lang = ? WHERE id = ?", (lang, user_id))
        await db.commit()

async def setup_bot_commands(lang: str):
    # Команды по умолчанию для всех пользователей

    await bot.set_my_commands(
        [BotCommand(command="start", description=translations_2.translations[lang]['start']),
        BotCommand(command="cancel", description=translations_2.translations[lang]['cancel']),],
        scope=BotCommandScopeDefault()
    )

    # Словарь для накопления команд по конкретному чату
    # Ключ: chat_id (int), значение: набор команд (тип BotCommand)
    chat_commands = {}

    # Функция для добавления команды в набор для данного чата
    def add_command(chat_id: int, command: BotCommand):
        if chat_id not in chat_commands:
            chat_commands[chat_id] = {}
        # Используем имя команды как ключ, чтобы избежать дублирования
        chat_commands[chat_id][command.command] = command

    # Добавляем команды для администраторов
    admin_ids = [2122289037, 1244773560, 5099581636]
    for admin_id in admin_ids:
        try:
            # Если админ уже есть, просто добавляем нужные команды
            add_command(admin_id, BotCommand(command="start", description=translations_2.translations[lang]['start']))
            add_command(admin_id, BotCommand(command="cancel", description=translations_2.translations[lang]['cancel']))
            add_command(admin_id, BotCommand(command="admin", description=translations_2.translations[lang]['admin']))
        except Exception as e:
            print(f"Ошибка при добавлении команд для admin с chat_id={admin_id}: {e}")

    # Добавляем команды для трафферов
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("SELECT trafer_id FROM traffers") as cursor:
            rows = await cursor.fetchall()
            for (trafer_id,) in rows:
                try:
                    chat_id = int(trafer_id)
                except ValueError:
                    print(f"Пропущен trafer_id='{trafer_id}': невозможно преобразовать в int")
                    continue

                try:
                    add_command(chat_id, BotCommand(command="start", description=translations_2.translations[lang]['start']))
                    add_command(chat_id, BotCommand(command="cancel", description=translations_2.translations[lang]['cancel']))
                    add_command(chat_id, BotCommand(command="traffer", description=translations_2.translations[lang]['traffer']))
                except Exception as e:
                    print(f"Ошибка при добавлении команд для trafer с chat_id={chat_id}: {e}")

    # Устанавливаем команды для каждого чата из нашего словаря
    for chat_id, commands_dict in chat_commands.items():
        commands_list = list(commands_dict.values())
        try:
            await bot.set_my_commands(
                commands_list,
                scope=BotCommandScopeChat(chat_id=chat_id)
            )
        except TelegramBadRequest as e:
            print(f"Не удалось установить команды для chat_id={chat_id}: {e}")



async def update_rach_prognoz(user_id: int, amount: int):
    async with aiosqlite.connect('users.db') as db:
        await db.execute(
            'UPDATE users SET rach_prognoz = rach_prognoz + ? WHERE id = ?',
            (amount, user_id)
        )
        await db.commit()


async def update_subscription(user_id: int, subscription_name: str, add_ob_vr: int, add_rach_vr: int,
                              duration_seconds: int):
    expiration = int(time.time()) + duration_seconds
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            UPDATE users
            SET subscription = ?,
                time = ?,
                ob_vr_prognoz = ?,
                rach_vr_prognoz = ?
            WHERE id = ?
        ''', (subscription_name, expiration, add_ob_vr, add_rach_vr, user_id))
        await db.commit()


def format_remaining_time(seconds: int, lang: str) -> str:
    if seconds <= 0:
        return translations_2.translations[lang]['podpiska_istekla']
    days = seconds // (24 * 3600)
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return translations_2.translations[lang]['bolche_day'].format(days=days, hours=hours)
    elif hours > 0:
        return translations_2.translations[lang]['menche_day'].format(hours=hours, minutes=minutes)
    else:
        return translations_2.translations[lang]['menche_hour'].format(minutes=minutes)


# ============================================
# Фоновая задача проверки подписок
# ============================================
async def check_expired_subscriptions():
    while True:
        current_time = int(time.time())
        async with aiosqlite.connect('users.db') as db:
            async with db.execute("SELECT id FROM users WHERE subscription != '-' AND time <= ?",
                                  (current_time,)) as cursor:
                expired_users = await cursor.fetchall()
            for (user_id,) in expired_users:
                await db.execute('''
                    UPDATE users
                    SET subscription = '-', time = 0, ob_prognoz = 0, rach_prognoz = 0
                    WHERE id = ?
                ''', (user_id,))
                await db.commit()
        await asyncio.sleep(60)


# ============================================
# Функции для анимации и отправки сообщений
# ============================================



def sanitize_telegram_html(html_text: str) -> str:
    # Экранируем все метки HTML и спецсимволы
    escaped = html.escape(html_text)
    # Разрешённые теги Telegram
    allowed_tags = ['b', 'i', 'code', 'pre', 'blockquote', 'a']
    for tag in allowed_tags:
        # открывающие теги
        if tag == 'a':
            # восстановим <a href="...">
            escaped = re.sub(
                r'&lt;a href=&quot;([^&]+)&quot;&gt;',
                r'<a href="\1">',
                escaped
            )
        else:
            escaped = re.sub(rf'&lt;{tag}&gt;', f'<{tag}>', escaped)
        # закрывающие теги
        escaped = re.sub(rf'&lt;/{tag}&gt;', f'</{tag}>', escaped)
    return escaped

async def animate_deletion(user_id: int, message_id: int):
    stages = ["⌛", "⏳", "🕐", "🕑", "🕒"]
    for stage in stages:
        try:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=stage)
            await asyncio.sleep(0.3)
        except Exception:
            break
    try:
        await bot.delete_message(chat_id=user_id, message_id=message_id)
    except Exception:
        pass


# async def delete_previous_message(user_id: int, animate: bool = False):
#     if user_id in last_bot_messages and last_bot_messages[user_id]:
#         try:
#             if animate:
#                 await animate_deletion(user_id, last_bot_messages[user_id])
#             else:
#                 await bot.delete_message(chat_id=user_id, message_id=last_bot_messages[user_id])
#         except Exception:
#             pass
#
#
# async def send_message_with_delete(user_id: int, text: str, reply_markup=None, delete_previous: bool = True,
#                                    animate_delete: bool = False):
#     if delete_previous:
#         await delete_previous_message(user_id, animate=animate_delete)
#     sent_message = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
#     if delete_previous:
#         last_bot_messages[user_id] = sent_message.message_id
#
#
# async def send_photo_with_delete(user_id: int, photo: str, caption: str = "", reply_markup=None,
#                                  delete_previous: bool = True, animate_delete: bool = False, parse_mode: str = None):
#     if delete_previous:
#         await delete_previous_message(user_id, animate=animate_delete)
#     sent_message = await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=reply_markup,
#                                         parse_mode=parse_mode)
#     if delete_previous:
#         last_bot_messages[user_id] = sent_message.message_id


async def delete_previous_message(user_id: int, animate: bool = False):
    """Удаляет или анимирует удаление предыдущего сообщения, если оно есть."""
    prev = last_bot_messages.get(user_id)
    if not prev:
        return
    message_id = prev["message_id"]
    try:
        if animate:
            await animate_deletion(user_id, message_id)
        else:
            await bot.delete_message(chat_id=user_id, message_id=message_id)
    except Exception:
        pass
    finally:
        last_bot_messages.pop(user_id, None)

async def send_message_with_delete(
    user_id: int,
    text: str,
    reply_markup=None,
    delete_previous: bool = True,
    animate_delete: bool = False,
    parse_mode: str | None = None
):
    """
    Отправляет или редактирует текстовое сообщение.
    Параметры совпадают с предыдущей версией:
      user_id, text, reply_markup, delete_previous, animate_delete, parse_mode
    """
    # 1) Попробуем отредактировать прошлое сообщение
    if delete_previous and user_id in last_bot_messages and last_bot_messages[user_id]["type"] == "text":
        prev_id = last_bot_messages[user_id]["message_id"]
        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=prev_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
            return
        except (TelegramBadRequest, TelegramForbiddenError):
            # не удалось — убираем из кэша и пошлём новое
            last_bot_messages.pop(user_id, None)

    # 2) Если редактировать нельзя или delete_previous=False — удаляем старое вручную
    if delete_previous:
        await delete_previous_message(user_id, animate=animate_delete)

    # 3) Отправляем новое сообщение
    msg = await bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )
    # 4) Сохраняем ID для будущих правок
    if delete_previous:
        last_bot_messages[user_id] = {"message_id": msg.message_id, "type": "text"}

async def send_photo_with_delete(
    user_id: int,
    photo: str | types.InputFile,
    caption: str = "",
    reply_markup=None,
    delete_previous: bool = True,
    animate_delete: bool = False,
    parse_mode: str | None = None
):
    """
    Умная отправка фото: поддерживает плавное обновление фото + подписи.
    Если фото - это FSInputFile, сравнивает пути к файлам.
    Это позволяет использовать динамические пути для разных языков.
    """
    prev = last_bot_messages.get(user_id)

    # Получаем уникальный и стабильный идентификатор для текущего фото.
    # Если это файл на диске, его ID - это путь. Если это file_id из Telegram - то это сама строка.
    current_photo_identifier = photo.path if isinstance(photo, types.FSInputFile) else photo

    # Если есть предыдущее сообщение и оно было с фото
    if delete_previous and prev and prev["type"] == "photo":
        # Сравниваем идентификаторы (путь к файлу или file_id)
        if prev.get("photo_id") == current_photo_identifier:
            # Фото то же самое (например, 'images/ru/faq.png' == 'images/ru/faq.png')
            # Пытаемся просто отредактировать подпись
            try:
                await bot.edit_message_caption(
                    chat_id=user_id,
                    message_id=prev["message_id"],
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
                return # Выходим, так как сообщение успешно отредактировано
            except TelegramBadRequest:
                # Редактировать не удалось (например, сообщение слишком старое)
                # Удаляем его из кеша, чтобы отправить новое
                last_bot_messages.pop(user_id, None)
        else:
            # Фото изменилось (например, было 'images/ru/support.png', а стало 'images/ru/faq.png')
            # Удаляем старое сообщение
            await delete_previous_message(user_id, animate=animate_delete)

    # Отправляем новое фото, если не удалось отредактировать или его не было
    msg = await bot.send_photo(
        chat_id=user_id,
        photo=photo,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )

    # Сохраняем в кеш ID сообщения, тип и УНИКАЛЬНЫЙ ИДЕНТИФИКАТОР ФОТО
    if delete_previous:
        last_bot_messages[user_id] = {
            "message_id": msg.message_id,
            "type": "photo",
            "photo_id": current_photo_identifier
        }



async def add_fsm_message_id(state: FSMContext, message_id: int):
    """Сохраняет ID сообщения в состоянии FSM."""
    data = await state.get_data()
    ids = data.get("message_ids", [])
    ids.append(message_id)
    await state.update_data(message_ids=ids)


async def delete_fsm_messages(chat_id: int, state: FSMContext):
    """Удаляет все сообщения формы после завершения."""
    data = await state.get_data()
    message_ids = data.get("message_ids", [])
    for mid in message_ids:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=mid)
        except Exception:
            pass
    await state.update_data(message_ids=[])


async def process_profile_redirect(user_id: int):
    user = await get_user(user_id)
    lang = await get_user_lang(user_id)
    referral_link = f"https://t.me/{BOT_USERNAME}?start=referral_{user_id}"
    referred_count = await get_referred_count(user_id)
    # logging.info(f"Generating referral link for user {user_id}: {referral_link}")
    if not user:
        return
    current_time = int(time.time())
    remaining = user[3] - current_time
    remaining_str = format_remaining_time(remaining, lang) if user[3] > current_time else "-"
    profile_text = translations_2.translations[lang]['profile_text'].format(
        user_name=user[1],
        user_id=user[0],
        subscription=user[2],
        remaining=remaining_str,
        ob_prognoz=user[4],
        rach_prognoz=user[5],
        ob_vr_prognoz=user[6],
        rach_vr_prognoz=user[7],
        referral_link=referral_link,
        referred_count=referred_count
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['katalog'], callback_data='katalog')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['sozdat_prognoz'], callback_data='prognoz')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['iazik'], callback_data="change_lang"),
         types.InlineKeyboardButton(text=translations_2.translations[lang]['otzivi'], callback_data='otzivi')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['promokod'], callback_data='promokod'),
         types.InlineKeyboardButton(text=translations_2.translations[lang]['support'], callback_data='support_menu')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['instruction'], callback_data='instruction_menu')]
    ])
    photo_path = translations_2.translations[lang]['photo_profil']
    await send_photo_with_delete(user_id, FSInputFile(photo_path), profile_text, parse_mode="Markdown", reply_markup=markup)


# ============================================
# подсчёт оплаты
# ============================================

@router.message(F.successful_payment)
async def on_payment_success(msg: types.Message):
    # Telegram вложил успешный платёж прямо в msg.successful_payment
    amount_kopeks = msg.successful_payment.total_amount
    amount_rub = amount_kopeks / 100
    user_id = msg.from_user.id
    lang = await get_user_lang(user_id)

    # логируем сумму в таблицу payments
    async with aiosqlite.connect('payments.db') as pdb:
        await pdb.execute(
            """
            INSERT INTO payments (user_id, type, amount, count, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                msg.from_user.id,
                'user_purchase',
                amount_rub,
                1,
                int(time.time()),
            )
        )
        await pdb.commit()

    await msg.answer(text=translations_2.translations[lang]['spasibo_za_oplaty'])


# ============================================
# FSM для добавления партнёра
# ============================================
# === Админ-панель: партнёры ===

@router.callback_query(F.data == "partners")
async def show_partners(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    # Получаем chat_id, username и описание
    async with aiosqlite.connect("partners.db") as db:
        async with db.execute("SELECT chat_id, title, description, link FROM partners") as cursor:
            rows = await cursor.fetchall()

    text = "Партнеры:\n"
    buttons = []
    for i, (chat_id, title, description, link) in enumerate(rows, start=1):
        text += f"{i}. <a href=\"{link}\">{title}</a> — {description}\n"
        buttons.append([
            types.InlineKeyboardButton(
                text=f"❌ {title}",
                callback_data=f"delete_partner:{chat_id}"
            )
        ])

    buttons.append([types.InlineKeyboardButton(text="➕ Добавить партнёра", callback_data="add_partner")])
    buttons.append([types.InlineKeyboardButton(text="↩️ Назад", callback_data="back_admin_panel")])

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await send_photo_with_delete(
        user_id,
        photo_admin_panel,
        text if rows else "Список партнёров пуст",
        reply_markup=markup,
        parse_mode=ParseMode.HTML
    )


# === FSM для добавления партнёра через интерфейс (с поддержкой закрытых каналов) ===


# ============================================
# Состояния для добавления партнёра
# ============================================
class AddPartnerState(StatesGroup):
    input = State()
    manual_title = State()
    link = State()
    description = State()


# ============================================
# Запуск FSM добавления партнёра
# ============================================
@router.callback_query(F.data == "add_partner")
async def start_add_partner(cb: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(AddPartnerState.input)
    await delete_previous_message(cb.from_user.id)
    msg = await cb.message.answer("Введите @username канала ИЛИ chat_id (например: -1001234567890):")
    await add_fsm_message_id(state, msg.message_id)


# ============================================
# Шаг 1: ввод @username или chat_id
# ============================================
@router.message(StateFilter(AddPartnerState.input))
async def step_input(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    input_val = msg.text.strip()
    chat_id = input_val if input_val.startswith("-100") else None
    username = input_val.lstrip("@") if not chat_id else None

    try:
        chat = await bot.get_chat(chat_id or f"@{username}")
        chat_id = str(chat.id)
        title = chat.title or ""
        # проверяем, что бот админ с нужными правами
        member = await bot.get_chat_member(chat_id, bot.id)
        if not isinstance(member, (ChatMemberOwner, ChatMemberAdministrator)):
            raise Exception("Бот не админ")
        if isinstance(member, ChatMemberAdministrator) and not (
                member.can_invite_users or member.can_manage_chat or member.can_post_messages
        ):
            raise Exception("Недостаточно прав")
    except Exception:
        # не удаётся получить данные автоматически — переходим в ручной ввод названия
        await state.update_data(chat_id=chat_id or "", username=username or "")
        await state.set_state(AddPartnerState.manual_title)
        err = await msg.answer(
            "❌ Не удалось получить данные о канале автоматически.\n"
            "Пожалуйста, введите **название** канала вручную:",
            parse_mode=ParseMode.MARKDOWN
        )
        await add_fsm_message_id(state, err.message_id)
        return

    # успешно получили — сохраняем и идём к вводу ссылки
    await state.update_data(chat_id=chat_id, username=username or chat.username or "", title=title)
    await state.set_state(AddPartnerState.link)
    msg2 = await msg.answer("Отправьте ссылку на канал (https://t.me/...):")
    await add_fsm_message_id(state, msg2.message_id)


# ============================================
# Шаг 2: ручной ввод названия (если нужно)
# ============================================
@router.message(StateFilter(AddPartnerState.manual_title))
async def step_manual_title(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    title = msg.text.strip()
    await state.update_data(title=title)
    await state.set_state(AddPartnerState.link)
    msg2 = await msg.answer("Теперь отправьте ссылку на канал (https://t.me/...):")
    await add_fsm_message_id(state, msg2.message_id)


# ============================================
# Шаг 3: ввод ссылки на канал
# ============================================
@router.message(StateFilter(AddPartnerState.link))
async def step_link(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    link = msg.text.strip()
    if not link.startswith("http"):
        err = await msg.answer("❌ Укажите корректную ссылку на канал.")
        await add_fsm_message_id(state, err.message_id)
        return
    await state.update_data(link=link)
    await state.set_state(AddPartnerState.description)
    msg2 = await msg.answer("Введите описание партнёра:")
    await add_fsm_message_id(state, msg2.message_id)


# ============================================
# Шаг 4: ввод описания и сохранение
# ============================================
@router.message(StateFilter(AddPartnerState.description))
async def step_description(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    await state.update_data(description=msg.html_text)
    data = await state.get_data()

    async with aiosqlite.connect("partners.db") as db:
        await db.execute("""
            INSERT OR REPLACE INTO partners
              (chat_id, title, username, description, link)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data['chat_id'],
            data.get('title') or data.get('username'),
            data['username'],
            data['description'],
            data['link']
        ))
        await db.commit()

    # очищаем FSM-сообщения и состояние
    await delete_fsm_messages(msg.chat.id, state)
    await state.clear()

    done = await msg.answer("✅ Партнёр успешно добавлен!")
    await asyncio.sleep(3)
    try:
        await done.delete()
    except:
        pass

    # показываем обновлённый список партнёров в админке
    await show_partners(msg)


# ============================================
# Хендлер удаления партнёра по кнопке ❌
# ============================================
@router.callback_query(lambda cb: cb.data and cb.data.startswith("delete_partner:"))
async def delete_partner_handler(cb: types.CallbackQuery):
    await cb.answer("✅ Партнёр удалён.", show_alert=False)
    _, chat_id = cb.data.split(":", maxsplit=1)

    # удаляем из базы
    async with aiosqlite.connect("partners.db") as db:
        await db.execute("DELETE FROM partners WHERE chat_id = ?", (chat_id,))
        await db.commit()

    # удаляем старое сообщение
    try:
        await cb.message.delete()
    except:
        pass

    # заново показываем админ-панель с обновлённым списком
    await show_partners(cb)


# ============================================
# Функция отправки списка партнёров пользователю
# ============================================
# 1) Правильный send_partners_list
async def send_partners_list(user_id: int, next_action: str):
    lang = await get_user_lang(user_id)
    if not lang:  # Если язык не установлен, используем русский по умолчанию
        lang = 'ru'

    async with aiosqlite.connect("partners.db") as db:
        async with db.execute("SELECT chat_id, title, description, link FROM partners") as cursor:
            partners = await cursor.fetchall()

    if not partners:
        # Если партнеров нет, просто продолжаем действие (показываем главный экран)
        await send_welcome_logic(user_id)
        return

    translator = GoogleTranslator(source='auto', target=lang)

    # Используем ключ из словаря переводов для заголовка
    header_key = translations_2.translations.get(lang, {}).get('partners_header')
    text_lines = [header_key]
    buttons = []

    for i, (chat_id, title, description, link) in enumerate(partners, start=1):
        translated_description = description
        if lang != 'ru' and description:
            try:
                # переводим через deep-translator
                translated_description = translator.translate(description)
            except Exception as e:
                print(f"Ошибка перевода для языка '{lang}': {e}")
                # В случае ошибки оставляем оригинальное описание

        # Название (title) НЕ переводим. HTML-теги в description сохранятся.
        text_lines.append(f"{i}. <a href=\"{link}\">{title}</a> — {translated_description}")

        subscribe_text = translations_2.translations.get(lang, {}).get('subscribe_to', 'Подписаться на')
        buttons.append([types.InlineKeyboardButton(
            text=f"{subscribe_text} {title}",
            url=link
        )])

    # Кнопка для проверки подписки
    buttons.append([
        types.InlineKeyboardButton(
            text=translations_2.translations[lang]['chek_partners'],
            callback_data=f"check_partners_again:{next_action}"
        )
    ])

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    final_text = "\n\n".join(text_lines)

    photo_path = translations_2.translations[lang]['photo_cponsori']
    await bot.send_photo(user_id, caption=final_text, photo=FSInputFile(photo_path), reply_markup=markup, parse_mode=ParseMode.HTML)


# 2) Обработчик кнопки «Проверить подписку»
@router.callback_query(F.data.startswith("check_partners_again:"))
async def check_partners_again_handler(cb: CallbackQuery, state: FSMContext):
    _, next_action = cb.data.split(":", 1)
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)


    # если подписки нет — напоминаем
    if not await check_partners_subscription(user_id):
        await cb.answer(text=translations_2.translations[lang]['NO_chek_partners'], show_alert=True)
        return

    # удаляем список партнёров и убираем «крутилку»
    try:
        await cb.message.delete()
    except:
        pass
    await cb.answer()

    # ——— дозавершаем нужное действие ———
    if next_action == "start":
        # запускаем вашу «чистую» логику старта профиля
        await send_welcome_logic(user_id)

    elif next_action == "new_ob_prognoz":
        # вызываем оригинальный хэндлер создания обычного прогноза
        await market_prognoz_start(cb, state)

    elif next_action == "new_rach_prognoz":
        # и хэндлер VIP‑прогноза
        await market_prognoz_start(cb, state)

    # при необходимости добавьте другие ветки по next_action

# ============================================
# Обновление профиля Траффера
# ============================================
@router.callback_query(F.data.startswith("trafer_update:"))
async def handle_traffer_profile_refresh(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = await get_user_lang(user_id)
    trafer_id_to_refresh = callback_query.data.split(":")[1]

    # Логируем начало обработки
    # logging.info(f"Обработка обновления профиля для пользователя {user_id}, trafer_id: {trafer_id_to_refresh}")

    # Получаем актуальную информацию о траффере
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("""
            SELECT trafer_name, trafer_id, trafer_promo, trafer_telefon, trafer_karta, trafer_kripta,
                   pay_model, pay_value, pay_link, invite_link, trafer_username, crypto_network
            FROM traffers WHERE trafer_id = ?
        """, (trafer_id_to_refresh,)) as cursor:
            row = await cursor.fetchone()

    if not row:
        await callback_query.answer("Траффер не найден.", show_alert=True)
        return

    # Распаковываем данные
    (t_name, t_id, t_promo, t_telefon, t_karta, t_kripta,
     pay_model, pay_value, pay_link, invite_link, trafer_username, crypto_network) = row

    # Получаем актуальное количество лидов и список пользователей
    async with aiosqlite.connect('users.db') as udb:
        async with udb.execute(
                "SELECT COUNT(*), GROUP_CONCAT(user_id) FROM used_promocodes WHERE promokod = ?",
                (f"trafer:{t_promo}",)
        ) as cur:
            leads_data = await cur.fetchone()
            leads = leads_data[0] if leads_data else 0
            users_csv = leads_data[1] if leads_data and leads_data[1] else ''

    users = list(map(int, users_csv.split(','))) if users_csv else []

    # Определяем, кто запрашивает обновление
    is_admin_user = (user_id in ADMIN_ID)
    # logging.info(f"Пользователь {user_id} является админом: {is_admin_user}")

    # Явно удаляем предыдущее сообщение перед отправкой нового
    if user_id in last_bot_messages:
        try:
            await bot.delete_message(chat_id=user_id, message_id=last_bot_messages[user_id]["message_id"])
            # logging.info(f"Удалено предыдущее сообщение с ID {last_bot_messages[user_id]['message_id']}")
        # except Exception as e:
        #     # logging.error(f"Не удалось удалить предыдущее сообщение: {e}")
        finally:
            last_bot_messages.pop(user_id, None)

    # Вызываем функцию для отображения профиля с актуальными данными
    await _show_traffer_profile(
        user_id=user_id,
        trafer_name=t_name,
        t_id=t_id,
        trafer_username=trafer_username,
        t_promo=t_promo,
        t_telefon=t_telefon,
        t_karta=t_karta,
        t_kripta=t_kripta,
        crypto_network=crypto_network,
        pay_model=pay_model,
        pay_value=pay_value,
        pay_link=pay_link,
        invite_link=invite_link,
        leads=leads,
        users=users,
        dst=callback_query,
        is_admin=is_admin_user
    )

    # Показываем уведомление об успешном обновлении
    await callback_query.answer("✅ Профиль обновлен!", show_alert=False)

# ============================================
# Редактирование профиля траффера
# ============================================

class EditTrafferState(StatesGroup):
    choosing_field = State()
    editing_value = State()

@router.callback_query(F.data.startswith("edit_traffer:"))
async def start_edit_traffer(cb: types.CallbackQuery, state: FSMContext):
    t_id = cb.data.split(":")[1]
    await state.set_state(EditTrafferState.choosing_field)
    await state.update_data(t_id=t_id)

    lang = await get_user_lang(cb.from_user.id)

    buttons = [
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['edit_name'], callback_data="edit_field:trafer_name")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['edit_id'], callback_data="edit_field:trafer_id")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['edit_username'], callback_data="edit_field:trafer_username")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['edit_telefon'], callback_data="edit_field:trafer_telefon")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['edit_karta'], callback_data="edit_field:trafer_karta")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['edit_kripta'], callback_data="edit_field:trafer_kripta")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['edit_crypto_network'], callback_data="edit_field:crypto_network")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['cancel_edit'], callback_data="cancel_edit")],
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await cb.message.edit_reply_markup(reply_markup=markup)

@router.callback_query(F.data.startswith("edit_field:"), EditTrafferState.choosing_field)
async def ask_for_new_value(cb: types.CallbackQuery, state: FSMContext):
    field = cb.data.split(":")[1]
    await state.update_data(field=field)
    await state.set_state(EditTrafferState.editing_value)

    lang = await get_user_lang(cb.from_user.id)
    prompts = {
        "trafer_name": "enter_new_name",
        "trafer_id": "enter_new_id",
        "trafer_username": "enter_new_username",
        "trafer_telefon": "enter_new_telefon",
        "trafer_karta": "enter_new_karta",
        "trafer_kripta": "enter_new_kripta",
        "crypto_network": "enter_new_crypto_network"
    }

    await cb.message.edit_reply_markup(reply_markup=None)
    msg = await cb.message.answer(translations_2.translations[lang][prompts[field]])
    await add_fsm_message_id(state, msg.message_id)

@router.message(EditTrafferState.editing_value)
async def save_new_value(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    field = data['field']
    t_id = data['t_id']
    new_value = msg.text

    async with aiosqlite.connect("traffers.db") as db:
        await db.execute(f"UPDATE traffers SET {field} = ? WHERE trafer_id = ?", (new_value, t_id))
        await db.commit()

    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)  # удаляем сообщение админа
    await delete_fsm_messages(msg.chat.id, state)  # удаляем FSM-сообщения
    await state.clear()

    lang = await get_user_lang(msg.from_user.id)
    await msg.answer(  # отправим "всплывающее" сообщение, затем удалим
        translations_2.translations[lang]['traffer_updated_success']
    )
    await asyncio.sleep(1)
    try:
        await bot.delete_message(msg.chat.id, msg.message_id + 1)  # удаляем "✅ обновлено"
    except:
        pass

    # Получаем обновлённые данные траффера
    async with aiosqlite.connect("traffers.db") as db:
        async with db.execute("SELECT * FROM traffers WHERE trafer_id = ?", (t_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                await msg.answer(translations_2.translations[lang]['no_traffer_found'])
                return

            await _show_traffer_profile(
                user_id=msg.from_user.id,
                trafer_name=row[1],
                t_id=row[2],
                trafer_username=row[12],
                t_promo=row[3],
                t_telefon=row[4],
                t_karta=row[5],
                t_kripta=row[6],
                crypto_network=row[13],
                pay_model=row[7],
                pay_value=row[8],
                pay_link=row[9],
                invite_link=row[10],
                leads=0,
                users=[],
                dst=msg,
                is_admin=True
            )

@router.callback_query(F.data == "cancel_edit", EditTrafferState.choosing_field)
async def cancel_edit(cb: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()


# ============================================
# Проверка подписки повторно
# ============================================
@router.callback_query(F.data.startswith("check_partners_again:"))
async def check_partners_again_handler(cb: types.CallbackQuery):
    _, next_action = cb.data.split(":", 1)
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)

    if not await check_partners_subscription(user_id):
        await cb.answer(text=translations_2.translations[lang]['NO_chek_partners'], show_alert=True)
        return

    # удаляем сообщение со списком партнёров
    try:
        await cb.message.delete()
    except:
        pass
    await cb.answer()  # убираем «крутилку»

    # дозавершаем исходное действие
    if next_action == "start":
        await send_welcome_logic(user_id)
    elif next_action == "new_ob_prognoz":
        # в обычном прогнозе можно пересоздать CallbackQuery-объект или напрямую запустить логику
        await new_ob_prognoz_start_cb(user_id, State)
    elif next_action == "new_rach_prognoz":
        await new_rach_prognoz_start_cb(user_id, State)
    # добавьте сюда обработку других next_action, если потребуется


# 1) Логика /start без декоратора
async def send_welcome_logic(user_id: int):
    # обновляем last_active

    lang = await get_user_lang(user_id)
    await setup_bot_commands(lang)
    current_timestamp = int(time.time())
    async with aiosqlite.connect('users.db') as db:
        await db.execute(
            "UPDATE users SET last_active = ? WHERE id = ?",
            (current_timestamp, user_id)
        )
        await db.commit()

    # получаем или создаём пользователя
    user = await get_user(user_id)
    lang = await get_user_lang(user_id)
    if user is None:
        # NOTE: на этом этапе пользователь уже должен быть в базе,
        # но на всякий случай можно завести инициализацию
        await add_user(user_id, "Unknown")
        user = await get_user(user_id)

    if user is None:
        return await bot.send_message(user_id, text=translations_2.translations[lang]['error_profile'])

    # формируем текст профиля
    referral_link = f"https://t.me/{BOT_USERNAME}?start=referral_{user_id}"
    referred_count = await get_referred_count(user_id)
    current_time = int(time.time())
    remaining = user[3] - current_time
    remaining_str = format_remaining_time(remaining, lang) if user[3] > current_time else "-"
    profile_text = translations_2.translations[lang]['profile_text'].format(
        user_name=user[1],
        user_id=user[0],
        subscription=user[2],
        remaining=remaining_str,
        ob_prognoz=user[4],
        rach_prognoz=user[5],
        ob_vr_prognoz=user[6],
        rach_vr_prognoz=user[7],
        referral_link=referral_link,
        referred_count=referred_count
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['katalog'], callback_data='katalog')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['sozdat_prognoz'], callback_data='prognoz')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['iazik'], callback_data="change_lang"),
         types.InlineKeyboardButton(text=translations_2.translations[lang]['otzivi'], callback_data='otzivi')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['promokod'], callback_data='promokod'),
         types.InlineKeyboardButton(text=translations_2.translations[lang]['support'], callback_data='support_menu')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['instruction'], callback_data='instruction_menu')]
    ])
    photo_path = translations_2.translations[lang]['photo_profil']
    await send_photo_with_delete(user_id, FSInputFile(photo_path), profile_text, parse_mode="Markdown", reply_markup=markup)


# 2) Логика запуска обычного прогноза без декоратора
async def new_ob_prognoz_start_cb(user_id: int, state: FSMContext):
    # 1) Получаем остатки прогнозов
    user = await get_user(user_id)
    lang = await get_user_lang(user_id)
    ob_cnt, _, ob_vr, _ = user[4], user[5], user[6], user[7]

    # 2) Если прогнозов нет — уведомляем
    if ob_vr <= 0 and ob_cnt <= 0:
        return await bot.send_message(user_id, translations_2.translations[lang]['NOT_od_prognoz'])

    # 3) Иначе — старт FSM
    await state.update_data(message_ids=[], prog_type='ob')
    msg = await bot.send_message(user_id,translations_2.translations[lang]['vvedite_daty_vremia'])
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(MarketPrognozState.date_time)


# 3) Логика запуска VIP‑прогноза без декоратора
async def new_rach_prognoz_start_cb(user_id: int, state: FSMContext):
    # проверяем VIP‑прогнозы
    user = await get_user(user_id)
    lang = await get_user_lang(user_id)
    _, rach_cnt, _, rach_vr = user[4], user[5], user[6], user[7]

    if rach_vr <= 0 and rach_cnt <= 0:
        return await bot.send_message(user_id, translations_2.translations[lang]['NOT_VIP_prognoz'])

    # старт FSM
    await state.update_data(message_ids=[], prog_type='rach')
    msg = await bot.send_message(user_id,translations_2.translations[lang]['vvedite_daty_vremia'])
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(MarketPrognozState.date_time)


# ============================================
# FSM для добавления траффера
# ============================================
async def get_traffer_by_id(trafer_id_str: str):
    """
    Получает полную информацию о траффере из базы данных по его строковому ID.
    Args:
        trafer_id_str (str): Строковый ID траффера, как он хранится в traffers.db.
    Returns:
        tuple or None: Кортеж с данными траффера, если найден, иначе None.
    """
    async with aiosqlite.connect('traffers.db') as db:
        # Важно: trafer_id в traffers.db - TEXT, поэтому ищем по строке.
        async with db.execute('SELECT * FROM traffers WHERE trafer_id = ?', (trafer_id_str,)) as cursor:
            return await cursor.fetchone() # Возвращаем первую найденную запись

async def get_traffer_balance(trafer_id: str):
    # 1) посчитали всего заработано (см. пункт 2)
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("SELECT pay_model, pay_value, trafer_promo FROM traffers WHERE trafer_id = ?",
                              (str(trafer_id),)) as cur:
            pay_model, pay_value, promo = await cur.fetchone()
    # — leads, total_spent тут можно переиспользовать код из пункта 2
    # получим total_earned
    if pay_model == 'model_bot':
        async with aiosqlite.connect('users.db') as udb:
            async with udb.execute("SELECT COUNT(*) FROM used_promocodes WHERE promokod = ?",
                                   (f"trafer:{promo}",)) as c1:
                leads = (await c1.fetchone())[0]
        total = leads * pay_value
    elif pay_model == 'model_percent':
        # 1) получаем список user_id из used_promocodes для этого промокода
        async with aiosqlite.connect('users.db') as udb:
            async with udb.execute(
                    "SELECT user_id FROM used_promocodes WHERE promokod = ?",
                    (f"trafer:{promo}",)
            ) as c:
                users = [row[0] for row in await c.fetchall()]

        if users:
            # 2) считаем сумму всех amount в таблице payments для этих пользователей
            q_marks = ",".join("?" for _ in users)
            sql = f"SELECT SUM(amount) FROM payments WHERE user_id IN ({q_marks})"
            async with aiosqlite.connect('payments.db') as pdb:
                async with pdb.execute(sql, users) as c2:
                    total_spent = (await c2.fetchone())[0] or 0

        else:
            total_spent = 0

        # 3) проценты
        total = total_spent * pay_value // 100

    elif pay_model == 'model_channel':
        # считаем число юзеров, пришедших по invite_link этого traffer’а
        async with aiosqlite.connect('users.db') as udb:
            async with udb.execute(
                    "SELECT COUNT(*) FROM used_promocodes WHERE promokod = ?",
                    (f"trafer:{promo}",)
            ) as cur:
                subscribers = (await cur.fetchone())[0] or 0
        total = subscribers * pay_value


    else:
        total = 0
    # 2) сколько вывел
    async with aiosqlite.connect('traffer_payouts.db') as pdb:
        async with pdb.execute(
                "SELECT SUM(amount) FROM traffer_payouts WHERE trafer_id = ? AND status = 'done'", (trafer_id,)
        ) as c2:
            paid = (await c2.fetchone())[0] or 0
    return total, paid, total - paid


class AddTrafferState(StatesGroup):
    trafer_name = State()
    trafer_id = State()
    trafer_promo = State()
    trafer_telefon = State()
    trafer_karta = State()
    trafer_kripta = State()
    trafer_username = State()      # ← 🔧 добавить
    crypto_network = State()       # ← 🔧 добавить
    pay_model = State()
    pay_value = State()
    pay_link = State()
    finish = State()




class WithdrawState(StatesGroup):
    amount = State()
    confirm = State()


@router.callback_query(lambda c: c.data == 'new_trafer')
async def new_trafer_start(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id not in [2122289037, 1244773560, 5099581636]:
        return await callback_query.answer("⛔ Доступ запрещён", show_alert=True)
    await callback_query.answer("⏳ Добавление траффера...", show_alert=False)
    await state.update_data(message_ids=[])
    msg = await callback_query.message.answer("🆕 Введите имя траффера:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.trafer_name)


@router.message(F.text, StateFilter(AddTrafferState.trafer_name))
async def trafer_name_step(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(trafer_name=message.text)
    msg = await message.answer("Введите ID траффера:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.trafer_id)


@router.message(F.text, StateFilter(AddTrafferState.trafer_id))
async def trafer_id_step(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    trafer_id = message.text.strip()
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("SELECT 1 FROM traffers WHERE trafer_id = ?", (trafer_id,)) as cursor:
            if await cursor.fetchone():
                return await message.answer("❌ Такой ID уже используется!")
    await state.update_data(trafer_id=trafer_id)
    msg = await message.answer("Введите промокод траффера:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.trafer_promo)


@router.message(F.text, StateFilter(AddTrafferState.trafer_promo))
async def trafer_promo_step(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(trafer_promo=message.text)
    msg = await message.answer("Введите телефон траффера:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.trafer_telefon)


@router.message(F.text, StateFilter(AddTrafferState.trafer_telefon))
async def trafer_telefon_step(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(trafer_telefon=message.text)
    msg = await message.answer("Введите карту траффера:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.trafer_karta)


@router.message(F.text, StateFilter(AddTrafferState.trafer_karta))
async def trafer_karta_step(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(trafer_karta=message.text)
    msg = await message.answer("Введите криптокошелёк траффера:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.trafer_kripta)


@router.message(F.text, StateFilter(AddTrafferState.trafer_kripta))
async def trafer_kripta_step(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(trafer_kripta=message.text)
    msg = await message.answer("Введите Telegram username траффера (например: @trafman):")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.trafer_username)


@router.message(F.text, StateFilter(AddTrafferState.trafer_username))
async def trafer_username_step(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    username = msg.text.strip()
    if not username.startswith('@'):
        return await msg.answer("❌ Username должен начинаться с @")
    await state.update_data(trafer_username=username)
    m = await msg.answer("Введите название сети криптовалюты (например: TON, TRC20, ERC20):")
    await add_fsm_message_id(state, m.message_id)
    await state.set_state(AddTrafferState.crypto_network)


@router.message(F.text, StateFilter(AddTrafferState.crypto_network))
async def crypto_network_step(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    network = msg.text.strip()
    await state.update_data(crypto_network=network)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📊 % от трат при промокоде", callback_data="model_percent")],
        [types.InlineKeyboardButton(text="👤 ₽ за пользователя в бота", callback_data="model_bot")],
        [types.InlineKeyboardButton(text="📢 ₽ за подписчика в канал", callback_data="model_channel")]
    ])
    msg2 = await msg.answer("Выберите способ выплат:", reply_markup=keyboard)
    await add_fsm_message_id(state, msg2.message_id)
    await state.set_state(AddTrafferState.pay_model)


@router.callback_query(StateFilter(AddTrafferState.pay_model),
                       lambda c: c.data in ['model_percent', 'model_bot', 'model_channel'])
async def choose_pay_model(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(pay_model=cb.data)
    msg = await cb.message.answer("Введите значение N (число процентов или руб.):")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddTrafferState.pay_value)


@router.message(StateFilter(AddTrafferState.pay_value), F.text)
async def input_pay_value(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    try:
        value = int(msg.text.strip())
    except ValueError:
        return await msg.answer("Нужно целое число!")
    await state.update_data(pay_value=value)

    data = await state.get_data()
    if data['pay_model'] == 'model_channel':
        prompt = "Введите числовой chat_id канала (пример: -1002274333553):"
        await state.set_state(AddTrafferState.pay_link)
        msg2 = await msg.answer(prompt)
        await add_fsm_message_id(state, msg2.message_id)
    else:
        prompt = "Нажми «Завершить» для сохранения"
        await state.set_state(AddTrafferState.finish)
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="✅ Завершить", callback_data="finish_add_traffer")]
        ])
        msg2 = await msg.answer(prompt, reply_markup=kb)
        await add_fsm_message_id(state, msg2.message_id)


@router.message(StateFilter(AddTrafferState.pay_link), F.text)
async def input_pay_link(msg: types.Message, state: FSMContext):
    text = msg.text.strip()
    data = await state.get_data()
    try:
        chat_id = int(text)
        invite = await bot.create_chat_invite_link(
            chat_id=chat_id,
            name=f"promo_{data['trafer_promo']}",
            creates_join_request=True
        )
        invite_link = invite.invite_link
        await state.update_data(pay_link=chat_id, invite_link=invite_link)
    except ValueError:
        return await msg.answer("❌ Введите только число, начинающееся с `-100…`")
    await add_fsm_message_id(state, msg.message_id)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Завершить", callback_data="finish_add_traffer")]
    ])
    msg2 = await msg.answer("Нажми «Завершить» для сохранения", reply_markup=kb)
    await add_fsm_message_id(state, msg2.message_id)
    await state.set_state(AddTrafferState.finish)


# 4) Ввод pay_link (только для model_channel)
@router.message(StateFilter(AddTrafferState.pay_link), F.text)
async def input_pay_link(msg: types.Message, state: FSMContext):
    text = msg.text.strip()
    data = await state.get_data()

    try:
        chat_id = int(text)
        invite = await bot.create_chat_invite_link(
            chat_id=chat_id,
            name=f"promo_{data['trafer_promo']}",
            expire_date=None,
            member_limit=0,  # неограниченно
            creates_join_request=True  # чтобы был Join Request
        )
        invite_link = invite.invite_link

        # Сохраняем и chat_id, и invite_link
        await state.update_data(pay_link=chat_id, invite_link=invite_link)
    except ValueError:
        return await msg.answer("❌ Некорректный формат. Введите только число, начинающееся с `-100…`")
    # pay_link теперь — именно chat_id канала
    await state.update_data(pay_link=chat_id)
    await add_fsm_message_id(state, msg.message_id)
    await state.update_data(pay_link=msg.text.strip())
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Завершить", callback_data="finish_add_traffer")]
    ]
    )
    msg2 = await msg.answer("Нажми «Завершить» для сохранения", reply_markup=kb)
    await add_fsm_message_id(state, msg2.message_id)
    await state.set_state(AddTrafferState.finish)


@router.callback_query(F.data == "finish_add_traffer")
async def finish_traffer(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await add_traffer(
    data["trafer_name"], data["trafer_id"], data["trafer_promo"],
    data["trafer_telefon"], data["trafer_karta"], data["trafer_kripta"],
    data["pay_model"], data["pay_value"], data.get("pay_link"), data.get("invite_link"),
    data.get("trafer_username"), data.get("crypto_network")
    )
    await callback.answer("✅ Траффер успешно добавлен!", show_alert=True)
    await delete_fsm_messages(callback.message.chat.id, state)
    await state.clear()

    # Добавляем задержку, чтобы все сообщения успели сохраниться/удалиться
    await asyncio.sleep(1)  # задержка в 1 секунду (можно увеличить)

    # Перенаправляем пользователя в панель управления трафферами,
    # вызываем функцию, которая отображает список трафферов
    await show_traffers(callback)


# ============================================
# обновление панели с траферами
# ============================================

@router.callback_query(lambda c: c.data == 'baza_traferov')
async def show_traffers(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Запрос всех траферов из базы данных traffers.db
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("SELECT trafer_name FROM traffers") as cursor:
            traffers_list = await cursor.fetchall()

    # Формирование динамической клавиатуры
    buttons = []
    for row in traffers_list:
        trafer_name = row[0]
        # callback_data можно формировать по своему усмотрению, например, добавив префикс и имя
        buttons.append([types.InlineKeyboardButton(text=trafer_name, callback_data=f"trafer_{trafer_name}")])

    # Добавляем кнопку "Назад" для возврата в предыдущее меню
    buttons.append([types.InlineKeyboardButton(text='↩️ Назад', callback_data='traferi')])
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await send_photo_with_delete(user_id, photo_admin_panel, "Список траферов:", reply_markup=markup)


@router.callback_query(lambda c: c.data.startswith('trafer_'))
async def show_trafer_details(cb: types.CallbackQuery):
    # 1) Извлекаем имя и данные из БД
    user_id = cb.from_user.id
    trafer_name = cb.data[len('trafer_'):]
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("""
            SELECT trafer_name, trafer_id, trafer_promo, trafer_telefon, trafer_karta, trafer_kripta,
                   pay_model, pay_value, pay_link, invite_link, trafer_username, crypto_network
            FROM traffers
            WHERE trafer_name = ?
        """, (trafer_name,)) as cursor:
            row = await cursor.fetchone()
    if not row:
        return await cb.answer("Траффер не найден.", show_alert=True)

    (t_name, t_id, t_promo, t_telefon, t_karta, t_kripta,
     pay_model, pay_value, pay_link, invite_link, trafer_username, crypto_network) = row

    # 2) Считаем лидов и список юзеров
    async with aiosqlite.connect('users.db') as udb:
        async with udb.execute(
                "SELECT COUNT(*), GROUP_CONCAT(user_id) FROM used_promocodes WHERE promokod = ?",
                (f"trafer:{t_promo}",)
        ) as cur:
            leads, users_csv = await cur.fetchone()
    users = list(map(int, users_csv.split(','))) if users_csv else []

    # 3) Вызываем общую функцию
    await _show_traffer_profile(
        user_id=user_id,
        trafer_name=t_name,
        t_id=t_id,
        trafer_username=trafer_username,
        t_promo=t_promo,
        t_telefon=t_telefon,
        t_karta=t_karta,
        t_kripta=t_kripta,
        crypto_network=crypto_network,
        pay_model=pay_model,
        pay_value=pay_value,
        pay_link=pay_link,
        invite_link=invite_link,
        leads=leads,
        users=users,
        dst=cb,
        is_admin=True
    )


from aiogram import F  # убедитесь, что F уже импортирован вверху файла
import time


# @router.callback_query(F.data.startswith("update_channel:"))
# async def update_channel(cb: types.CallbackQuery):
#     trafer_id = int(cb.data.split(":", 1)[1])
#
#     # 1. Получаем pay_value, trafer_promo и последний подсчёт
#     async with aiosqlite.connect('traffers.db') as db:
#         async with db.execute(
#                 "SELECT pay_value, trafer_promo, last_subscribers FROM traffers WHERE trafer_id = ?",
#                 (str(trafer_id),)
#         ) as cur:
#             row = await cur.fetchone()
#     if not row:
#         return await cb.answer("Траффер не найден.", show_alert=True)
#     pay_value, promo, last = row
#
#     # 2. Считаем текущее число пришедших по ссылке
#     async with aiosqlite.connect('users.db') as udb:
#         async with udb.execute(
#                 "SELECT COUNT(*) FROM used_promocodes WHERE promokod = ?",
#                 (f"trafer:{promo}",)
#         ) as cur:
#             current = (await cur.fetchone())[0] or 0
#
#     # 3. Вычисляем дельту
#     delta = current - (last or 0)
#     if delta <= 0:
#         return await cb.answer("Новых подписчиков нет.", show_alert=True)
#     amount = delta * pay_value
#
#     # 4. Обновляем last_subscribers и логируем платёж
#     async with aiosqlite.connect('traffers.db') as db:
#         await db.execute(
#             "UPDATE traffers SET last_subscribers = ? WHERE trafer_id = ?",
#             (current, str(trafer_id))
#         )
#         await db.commit()
#
#     async with aiosqlite.connect('payments.db') as pdb:
#         await pdb.execute(
#             "INSERT INTO payments (user_id, type, amount, count, timestamp) VALUES (?, ?, ?, ?, ?)",
#             (trafer_id, 'channel_sub', amount, delta, int(time.time()))
#         )
#         await pdb.commit()
#
#     # 5. Ответ админу
#     await cb.answer(f"Новых подписчиков: {delta}\nНачислено: {amount} ₽", show_alert=True)


from aiogram.types import ChatJoinRequest


@router.chat_join_request()
async def on_join_request(req: ChatJoinRequest):
    # 1) Определяем трафера по invite_link
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute(
                "SELECT trafer_promo FROM traffers WHERE invite_link = ?",
                (req.invite_link.invite_link,)
        ) as cur:
            row = await cur.fetchone()

    if not row:
        # неизвестная ссылка — отклоняем заявку
        return await bot.decline_chat_join_request(req.chat.id, req.from_user.id)

    promo = row[0]
    # 2) Одобряем заявку
    await bot.approve_chat_join_request(req.chat.id, req.from_user.id)
    # 3) Фиксируем в базе лид
    async with aiosqlite.connect('users.db') as udb:
        await udb.execute(
            "INSERT OR IGNORE INTO used_promocodes(user_id, promokod) VALUES (?, ?)",
            (req.from_user.id, f"trafer:{promo}")
        )
        await udb.commit()


# @router.callback_query(lambda c: c.data.startswith("update_channel:"))
# async def update_channel(cb: types.CallbackQuery):
#     await cb.answer()
#     trafer_id = int(cb.data.split(":", 1)[1])
#
#     # 1) Читаем из traffers.db: promo, pay_value, last_subscribers
#     async with aiosqlite.connect('traffers.db') as db:
#         async with db.execute(
#                 "SELECT trafer_promo, pay_value, last_subscribers FROM traffers WHERE trafer_id = ?",
#                 (str(trafer_id),)
#         ) as cur:
#             row = await cur.fetchone()
#     if not row:
#         return await cb.answer("Трафер не найден.", show_alert=True)
#     promo, price, last = row
#
#     # 2) Считаем общее число лидов по этому промокоду
#     async with aiosqlite.connect('users.db') as udb:
#         async with udb.execute(
#                 "SELECT COUNT(*) FROM used_promocodes WHERE promokod = ?",
#                 (f"trafer:{promo}",)
#         ) as cur2:
#             total = (await cur2.fetchone())[0] or 0
#
#     # 3) Дельта новых лидов
#     new_leads = total - (last or 0)
#     if new_leads <= 0:
#         return await cb.answer("Новых подписчиков нет.", show_alert=True)
#
#     # 4) Обновляем last_subscribers и логируем платёж
#     async with aiosqlite.connect('traffers.db') as db:
#         await db.execute(
#             "UPDATE traffers SET last_subscribers = ? WHERE trafer_id = ?",
#             (total, str(trafer_id))
#         )
#         await db.commit()
#     payout = new_leads * price
#     # здесь ваша логика выплаты...
#
#     await cb.answer(f"✅ Новых подписчиков: {new_leads}\nНачислено: {payout} ₽", show_alert=True)


@router.callback_query(lambda c: c.data.startswith('delete_trafer_'))
async def delete_trafer(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    admin_ids = [2122289037, 1244773560, 5099581636]
    if user_id not in admin_ids:
        return await callback_query.answer("⛔ Доступ запрещён", show_alert=True)

    trafer_name = callback_query.data[len('delete_trafer_'):]

    # Получаем trafer_id и промокод
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("SELECT trafer_id, trafer_promo FROM traffers WHERE trafer_name = ?",
                              (trafer_name,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return await callback_query.answer("❌ Траффер не найден", show_alert=True)
            trafer_id, trafer_promo = row
        await db.execute("DELETE FROM traffers WHERE trafer_name = ?", (trafer_name,))
        await db.commit()

    # Удаление только связанных с траффером данных
    async with aiosqlite.connect('users.db') as db:
        await db.execute("DELETE FROM used_promocodes WHERE promokod = ?", (f"trafer:{trafer_promo}",))
        await db.commit()

    async with aiosqlite.connect('traffer_payouts.db') as db:
        await db.execute("DELETE FROM traffer_payouts WHERE trafer_id = ?", (trafer_id,))
        await db.execute("DELETE FROM withdraw_notifications WHERE trafer_id = ?", (trafer_id,))
        await db.commit()

    async with aiosqlite.connect('payments.db') as db:
        await db.execute("DELETE FROM payments WHERE user_id = ?", (trafer_id,))
        await db.commit()

    await callback_query.answer("✅ Траффер и связанные данные удалены", show_alert=True)
    await show_traffers(callback_query)


# ============================================
# FSM для добавления промокодов
# ============================================

class AddPromocodeState(StatesGroup):
    promokod = State()
    ob_prognoz = State()
    rach_prognoz = State()
    subscription = State()
    usage_count = State()  # новое состояние для количества использований
    finish = State()


@router.callback_query(lambda c: c.data == 'promo')
async def show_promocodes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Получаем список промокодов из базы
    async with aiosqlite.connect('promocodes.db') as db:
        async with db.execute("SELECT promokod FROM promocodes") as cursor:
            promocodes_list = await cursor.fetchall()

    buttons = []
    # Если промокодов нет, добавляем только кнопку "Добавить промокод"
    if promocodes_list:
        for row in promocodes_list:
            code = row[0]
            buttons.append([types.InlineKeyboardButton(text=code, callback_data=f"promocode_{code}")])
        # Добавляем кнопку для добавления нового промокода
        buttons.append([types.InlineKeyboardButton(text='➕ Добавить промокод', callback_data='new_promocode')])
    else:
        buttons.append([types.InlineKeyboardButton(text='➕ Добавить промокод', callback_data='new_promocode')])

    # Добавляем кнопку "↩️ Назад" для возврата в админ панель
    buttons.append([types.InlineKeyboardButton(text='↩️ Назад', callback_data='back_admin_panel')])
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await send_photo_with_delete(user_id, photo_admin_panel, "Список промокодов:", reply_markup=markup)
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith('promocode_'))
async def show_promocode_details(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data[len('promocode_'):]
    async with aiosqlite.connect('promocodes.db') as db:
        async with db.execute("""
            SELECT promokod, ob_prognoz, rach_prognoz, subscription, kolichestvo_ispolzovaniy
            FROM promocodes
            WHERE promokod = ?
        """, (code,)) as cursor:
            row = await cursor.fetchone()
    if not row:
        await callback_query.answer("Промокод не найден", show_alert=True)
        return
    promokod, ob_prognoz, rach_prognoz, subscription, usage_count = row
    text = f"""
➖➖➖➖➖➖➖➖➖

🔑 Промокод - {promokod}

*Функции:*
🔹 Обычные прогнозы - {ob_prognoz}
💠 Расширенные прогнозы - {rach_prognoz}
🎫 Подписка: {subscription}
🔓 Активаций - {usage_count}

➖➖➖➖➖➖➖➖➖
    """
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Удалить промокод', callback_data=f"delete_promocode_{promokod}")],
        [types.InlineKeyboardButton(text='↩️ Назад', callback_data='promo')]
    ])
    await send_photo_with_delete(user_id, photo_promo, text, parse_mode="Markdown", reply_markup=markup)
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith('delete_promocode_'))
async def delete_promocode(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Только админы могут удалять
    admin_ids = [2122289037, 1244773560, 5099581636]
    if user_id not in admin_ids:
        return await callback_query.answer("⛔ Доступ запрещён", show_alert=True)
    code = callback_query.data[len('delete_promocode_'):]
    async with aiosqlite.connect('promocodes.db') as db:
        await db.execute("DELETE FROM promocodes WHERE promokod = ?", (code,))
        await db.commit()
    await callback_query.answer("Промокод удалён", show_alert=True)
    # Возвращаемся в список промокодов
    await show_promocodes(callback_query)


@router.callback_query(F.data == 'new_promocode')
async def new_promocode_start(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id not in [2122289037, 1244773560, 5099581636]:
        return await callback_query.answer("⛔ Доступ запрещён", show_alert=True)
    await callback_query.answer("⏳ Добавление промокода...", show_alert=False)
    await state.update_data(message_ids=[])
    msg = await callback_query.message.answer("🆕 Введите название промокода:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddPromocodeState.promokod)


@router.message(F.text, StateFilter(AddPromocodeState.promokod))
async def promo_step_1(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(promokod=message.text)
    msg = await message.answer("Введите количество обычных прогнозов:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddPromocodeState.ob_prognoz)


@router.message(F.text, StateFilter(AddPromocodeState.ob_prognoz))
async def promo_step_2(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    try:
        await state.update_data(ob_prognoz=int(message.text))
    except ValueError:
        msg = await message.answer("Введите число!")
        await add_fsm_message_id(state, msg.message_id)
        return
    msg = await message.answer("Введите количество расширенных прогнозов:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddPromocodeState.rach_prognoz)


@router.message(F.text, StateFilter(AddPromocodeState.rach_prognoz))
async def promo_step_3(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    try:
        await state.update_data(rach_prognoz=int(message.text))
    except ValueError:
        msg = await message.answer("Введите число!")
        await add_fsm_message_id(state, msg.message_id)
        return
    msg = await message.answer("Введите название подписки (Standart, Medium, Premium) или (-):")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddPromocodeState.subscription)


@router.message(F.text, StateFilter(AddPromocodeState.subscription))
async def promo_step_4(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(subscription=message.text)
    msg = await message.answer("Сколько раз можно использовать:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddPromocodeState.usage_count)


@router.message(F.text, StateFilter(AddPromocodeState.usage_count))
async def promo_step_5(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    try:
        await state.update_data(usage_count=int(message.text))
    except ValueError:
        msg = await message.answer("Введите число!")
        await add_fsm_message_id(state, msg.message_id)
        return
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Завершить", callback_data="finish_add_promocode")]
    ])
    msg = await message.answer("📌 Нажми \"Завершить\" для сохранения.", reply_markup=keyboard)
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AddPromocodeState.finish)


@router.callback_query(F.data == "finish_add_promocode")
async def finish_promocode(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await add_promocode(
        data["promokod"], data["ob_prognoz"], data["rach_prognoz"],
        data["subscription"], data["usage_count"]
    )
    await callback.answer("✅ Промокод успешно добавлен!", show_alert=True)
    await delete_fsm_messages(callback.message.chat.id, state)
    await state.clear()

    # Задержка для корректной обработки сообщений
    await asyncio.sleep(1)

    # Перенаправляем пользователя в список промокодов
    await show_promocodes(callback)


# ============================================
# FSM для ввода промокода пользователем
# ============================================
class EnterUserPromocodeState(StatesGroup):
    code = State()
    finish = State()


@router.callback_query(F.data == 'promokod')
async def ask_promocode(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lang = await get_user_lang(user_id)
    await callback_query.answer(text=translations_2.translations[lang]['vvevite_promocod_1'], show_alert=False)
    await state.update_data(message_ids=[])
    msg = await callback_query.message.answer(text=translations_2.translations[lang]['vvevite_promocod_2'])
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(EnterUserPromocodeState.code)


@router.message(F.text, StateFilter(EnterUserPromocodeState.code))
async def process_user_promocode_input(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    await state.update_data(input_code=message.text.strip())
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['primenit_promocod'], callback_data="finish_apply_promocode")]
    ])
    msg = await message.answer(text=translations_2.translations[lang]['najmi_primenit_promocod'], reply_markup=keyboard)
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(EnterUserPromocodeState.finish)


@router.message(StateFilter(EnterUserPromocodeState.code), F.text)
async def process_user_promocode(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass
    await add_fsm_message_id(state, message.message_id)
    code = message.text.strip()
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)

    # [Обработка кода: проверка в базах, начисление бонусов и т.п.]
    # Пример для ветки, где промокод из базы трафферов найден:
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute("SELECT trafer_promo FROM traffers WHERE trafer_promo = ?", (code,)) as cursor:
            traffer_row = await cursor.fetchone()

    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM used_promocodes WHERE user_id = ? AND promokod LIKE 'trafer:%'",
                              (user_id,)) as cursor:
            used_trafer = await cursor.fetchone()

    if traffer_row is not None and used_trafer is None:
        await update_ob_prognoz(user_id, 1)
        async with aiosqlite.connect('users.db') as db:
            await db.execute("INSERT OR IGNORE INTO used_promocodes (user_id, promokod) VALUES (?, ?)",
                             (user_id, f"trafer:{code}"))
            await db.commit()
        final_msg = await message.answer(text=translations_2.translations[lang]['yes_promocod_ot_traffera'])
        await add_fsm_message_id(state, final_msg.message_id)
        await delete_fsm_messages(message.chat.id, state)
        await state.clear()
        return

    # Обработка поиска промокода в базе промокодов
    async with aiosqlite.connect('promocodes.db') as db:
        async with db.execute(
                "SELECT promokod, ob_prognoz, rach_prognoz, subscription, kolichestvo_ispolzovaniy FROM promocodes WHERE promokod = ?",
                (code,)) as cursor:
            promo_row = await cursor.fetchone()
    if promo_row is not None:
        promokod, add_ob_prognoz, add_rach_prognoz, subscription, usage_count = promo_row
        async with aiosqlite.connect('users.db') as db:
            async with db.execute("SELECT * FROM used_promocodes WHERE user_id = ? AND promokod = ?",
                                  (user_id, promokod)) as cursor:
                used_promo = await cursor.fetchone()
        if used_promo is not None:
            final_msg = await message.answer(text=translations_2.translations[lang]['ispolzovan_promocod'])
            await add_fsm_message_id(state, final_msg.message_id)
            await delete_fsm_messages(message.chat.id, state)
            await state.clear()
            return

        if usage_count <= 0:
            final_msg = await message.answer(text=translations_2.translations[lang]['nedeistvitelen_promocod'])
            await add_fsm_message_id(state, final_msg.message_id)
            await delete_fsm_messages(message.chat.id, state)
            await state.clear()
            return

        await update_ob_prognoz(user_id, add_ob_prognoz)
        await update_rach_prognoz(user_id, add_rach_prognoz)
        if subscription != '-' and subscription:
            async with aiosqlite.connect('users.db') as db:
                await db.execute("UPDATE users SET subscription = ? WHERE id = ?", (subscription, user_id))
                await db.commit()
        async with aiosqlite.connect('users.db') as db:
            await db.execute("INSERT OR IGNORE INTO used_promocodes (user_id, promokod) VALUES (?, ?)",
                             (user_id, promokod))
            await db.commit()
        async with aiosqlite.connect('promocodes.db') as db:
            await db.execute(
                "UPDATE promocodes SET kolichestvo_ispolzovaniy = kolichestvo_ispolzovaniy - 1 WHERE promokod = ?",
                (promokod,))
            await db.commit()
            async with db.execute("SELECT kolichestvo_ispolzovaniy FROM promocodes WHERE promokod = ?",
                                  (promokod,)) as cursor:
                result = await cursor.fetchone()
            if result is None or result[0] <= 0:
                await db.execute("DELETE FROM promocodes WHERE promokod = ?", (promokod,))
                await db.commit()
        final_msg = await message.answer(text=translations_2.translations[lang]['vvevite_promocod_2'].format(
            add_ob_prognoz=add_ob_prognoz,
            add_rach_prognoz=add_rach_prognoz,
            subscription=subscription))
        await add_fsm_message_id(state, final_msg.message_id)
        await delete_fsm_messages(message.chat.id, state)
        await state.clear()
        return

    final_msg = await message.answer(text=translations_2.translations[lang]['promocod_ne_nayden'])
    await add_fsm_message_id(state, final_msg.message_id)
    await delete_fsm_messages(message.chat.id, state)
    await state.clear()


@router.callback_query(F.data == "finish_apply_promocode")
async def finish_user_promocode(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    code = data.get("input_code", "").strip()
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)

    message_text = "" # Переменная для хранения текста ответа пользователю
    should_redirect = True # Флаг для контроля перенаправления

    try:
        # Проверка промокода от траффера
        async with aiosqlite.connect('traffers.db') as db:
            async with db.execute("SELECT trafer_promo FROM traffers WHERE trafer_promo = ?", (code,)) as cursor:
                traffer_row = await cursor.fetchone()

        if traffer_row is not None:
            async with aiosqlite.connect('users.db') as db:
                async with db.execute("SELECT * FROM used_promocodes WHERE user_id = ? AND promokod LIKE 'trafer:%'",
                                      (user_id,)) as cursor:
                    used_trafer = await cursor.fetchone()

            if used_trafer is None:
                await update_ob_prognoz(user_id, 1) # Предполагается, что для траффера всегда +1 ob_prognoz
                async with aiosqlite.connect('users.db') as db:
                    await db.execute("INSERT OR IGNORE INTO used_promocodes (user_id, promokod) VALUES (?, ?)",
                                     (user_id, f"trafer:{code}"))
                    await db.commit()
                message_text = translations_2.translations[lang]['promocod_ot_traffera_YES']
            else:
                message_text = translations_2.translations[lang]['ispolzovan_promocod'] # Промокод от траффера уже использован
                should_redirect = False # Не перенаправляем, если промокод от траффера уже использован
        else:
            # Если не промокод траффера, ищем в общей базе промокодов
            async with aiosqlite.connect('promocodes.db') as db:
                async with db.execute("SELECT promokod, ob_prognoz, rach_prognoz, subscription, kolichestvo_ispolzovaniy FROM promocodes WHERE promokod = ?", (code,)) as cursor:
                    promo_row = await cursor.fetchone()

            if not promo_row:
                message_text = translations_2.translations[lang]['promocod_ne_nayden']
                should_redirect = False
            else:
                promokod, add_ob_prognoz, add_rach_prognoz, subscription, usage_count = promo_row

                async with aiosqlite.connect('users.db') as db:
                    async with db.execute("SELECT * FROM used_promocodes WHERE user_id = ? AND promokod = ?",
                                          (user_id, promokod)) as cursor:
                        used_promo = await cursor.fetchone()

                if used_promo is not None:
                    message_text = translations_2.translations[lang]['ispolzovan_promocod']
                    should_redirect = False
                elif usage_count <= 0:
                    message_text = translations_2.translations[lang]['nedeistvitelen_promocod']
                    should_redirect = False
                else:
                    # Промокод действителен и не использован
                    await update_ob_prognoz(user_id, add_ob_prognoz)
                    await update_rach_prognoz(user_id, add_rach_prognoz)

                    if subscription and subscription != '-':
                        async with aiosqlite.connect('users.db') as db:
                            await db.execute("UPDATE users SET subscription = ? WHERE id = ?", (subscription, user_id))
                            await db.commit()

                    async with aiosqlite.connect('users.db') as db:
                        await db.execute("INSERT OR IGNORE INTO used_promocodes (user_id, promokod) VALUES (?, ?)", (user_id, promokod))
                        await db.commit()

                    async with aiosqlite.connect('promocodes.db') as db:
                        await db.execute(
                            "UPDATE promocodes SET kolichestvo_ispolzovaniy = kolichestvo_ispolzovaniy - 1 WHERE promokod = ?",
                            (promokod,))
                        await db.commit()
                        async with db.execute("SELECT kolichestvo_ispolzovaniy FROM promocodes WHERE promokod = ?",
                                              (promokod,)) as cursor:
                            result = await cursor.fetchone()
                        if result is None or result[0] <= 0:
                            await db.execute("DELETE FROM promocodes WHERE promokod = ?", (promokod,))
                            await db.commit()
                    message_text = translations_2.translations[lang]['vvevite_promocod_2'].format(
                        add_ob_prognoz=add_ob_prognoz,
                        add_rach_prognoz=add_rach_prognoz,
                        subscription=subscription if subscription and subscription != '-' else 'N/A' # Учитываем случай, если подписка неактивна
                    )

    except Exception as e:
        # logging.error(f"Error in finish_user_promocode: {e}\n{traceback.format_exc()}")
        message_text = translations_2.translations[lang].get('error_occured', 'Произошла непредвиденная ошибка.')
        should_redirect = False # В случае ошибки, возможно, не стоит перенаправлять сразу

    finally:
        # Отправка ответа пользователю
        if message_text:
            await callback.answer(text=message_text, show_alert=True) # Использовать show_alert для всех ответов для лучшего UX
        await delete_fsm_messages(callback.message.chat.id, state)
        await state.clear()

        # Перенаправление в профиль, если это необходимо
        if should_redirect:
            await asyncio.sleep(1) # Небольшая задержка перед перенаправлением
            await process_profile_redirect(user_id)

@router.callback_query(F.data == "close_trafer_panel")
async def close_trafer_panel(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    try:
        await callback.message.delete()
    except Exception as e:
        await callback.answer(text=translations_2.translations[lang]['error_close_panel'], show_alert=True)
        return
    await callback.answer()


@router.callback_query(F.data == "back_admin")
async def back_admin(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    try:
        await callback.message.delete()
    except Exception as e:
        await callback.answer(text=translations_2.translations[lang]['error_close_panel'], show_alert=True)
        return
    await callback.answer()

# ===================================================================
# FSM и хендлеры для РЫНОЧНОГО (Крипта/Акции) прогноза
# ===================================================================

# Вставьте этот словарь в начало блока FSM для рыночного прогноза (перед class MarketPrognozState)
tf_to_code = {
    "5 мин": "5m",
    "1 час": "1h",
    "1 день": "1d",
    "1 неделя": "1w",
    "1 месяц": "1m",
    "Полгода": "6m",
    "1 год": "1y"
}

class MarketPrognozState(StatesGroup):
    asset_type = State()    # 'crypto' или 'stock'
    asset_name = State()    # Тикер (BTC, AAPL и т.д.)
    network = State()       # Новая: сеть для крипты (USDT, USD, BTC, Spot)
    timeframe = State()     # '5 мин', '1 час', '1 день', '1 неделя', '1 месяц', 'Полгода', '1 год'
    confirm = State()       # Подтверждение данных
    prog_type = State()     # 'ob' или 'rach' (обычный или VIP)

# --- Запуск FSM ---
@router.callback_query(F.data.in_({'new_ob_prognoz', 'new_rach_prognoz'}))
@require_subscription("start")  # Проверка подписки на партнеров остается
async def market_prognoz_start(cb: types.CallbackQuery, state: FSMContext):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)
    prog_type = 'ob' if cb.data == 'new_ob_prognoz' else 'rach'

    # Проверка наличия прогнозов у пользователя
    user = await get_user(user_id)
    if prog_type == 'ob':
        if user[6] <= 0 and user[4] <= 0:
            return await cb.answer(translations_2.translations[lang]['NOT_od_prognoz'], show_alert=True)
    else:  # 'rach'
        if user[7] <= 0 and user[5] <= 0:
            return await cb.answer(translations_2.translations[lang]['NOT_VIP_prognoz'], show_alert=True)

    await cb.answer()
    await state.clear()
    await state.update_data(prog_type=prog_type, message_ids=[])

    # Шаг 1: Выбор типа актива
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🪙 Криптовалюта", callback_data="asset_crypto")],
        [types.InlineKeyboardButton(text="📈 Акция", callback_data="asset_stock")]
    ])
    msg = await cb.message.answer("Выберите тип актива для анализа:", reply_markup=markup)
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(MarketPrognozState.asset_type)

# --- Шаг 2: Получение типа и запрос названия ---
@router.callback_query(StateFilter(MarketPrognozState.asset_type), F.data.startswith("asset_"))
async def asset_type_step(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    asset_type = cb.data.split("_")[1]  # 'crypto' or 'stock'
    await state.update_data(asset_type=asset_type)

    prompt_text = "Введите тикер криптовалюты (например, BTC, ETH, SOL):" if asset_type == 'crypto' else "Введите тикер акции (например, AAPL, GOOGL, TSLA):"

    msg = await cb.message.edit_text(prompt_text)  # Редактируем прошлое сообщение
    await state.set_state(MarketPrognozState.asset_name)

# --- Шаг 3: Получение названия и проверка/выбор сети (для крипты) или timeframe (для stocks) ---
@router.message(StateFilter(MarketPrognozState.asset_name), F.text)
async def asset_name_step(msg: types.Message, state: FSMContext):
    await add_fsm_message_id(state, msg.message_id)
    asset_name = msg.text.strip().upper()
    data = await state.get_data()
    asset_type = data['asset_type']

    if asset_type == 'crypto':
        # Проверяем существование крипты через CoinGecko
        coin_id = get_coin_id(asset_name)
        if not coin_id:
            await msg.answer("❌ Криптовалюта не найдена. Попробуйте другой тикер (e.g., BTC, ETH, SOL) или введите правильно.")
            return  # Остаемся в state asset_name

        # Получаем доступные сети (pairs) с Bybit
        try:
            available_networks = []
            available_categories = {}
            session = httpx.Client()
            for category in ['linear', 'inverse', 'spot']:
                params = {"category": category}
                response = session.get(f"{BASE_URL}/v5/market/tickers", params=params).json()
                tickers = response.get('result', {}).get('list', [])
                for ticker in tickers:
                    if ticker['symbol'].startswith(asset_name) and ticker['symbol'] != asset_name:  # e.g., SOLUSDT, SOLUSD
                        network = ticker['symbol'][len(asset_name):]  # USDT, USD, etc.
                        if any(char.isdigit() for char in network): continue  # Skip dated
                        if network in ['USDT', 'USDC', 'USD', 'BTC', 'ETH', 'TRY', 'FDUSD']:
                            # Check if kline available (limit=1)
                            test_params = {"category": category, "symbol": ticker['symbol'], "interval": "D", "limit": 1}
                            test_response = session.get(f"{BASE_URL}/v5/market/kline", params=test_params).json()
                            if test_response.get("retCode") == 0 and test_response["result"]["list"]:
                                available_networks.append(network)
                                available_categories[network] = category

            if not available_networks:
                await msg.answer(f"❌ Нет доступных сетей с данными для торговли {asset_name}. Попробуйте другую крипту.")
                return

            await state.update_data(asset_name=asset_name, available_networks=available_networks, available_categories=available_categories)
            markup = types.InlineKeyboardMarkup(inline_keyboard=[])
            row = []
            for net in available_networks:
                row.append(types.InlineKeyboardButton(text=net, callback_data=f"network_{net}"))
                if len(row) == 2:
                    markup.inline_keyboard.append(row)
                    row = []
            if row:
                markup.inline_keyboard.append(row)
            await msg.answer(f"Выберите сеть для торговли {asset_name}:", reply_markup=markup)
            await state.set_state(MarketPrognozState.network)
        except Exception as e:
            logging.error(f"Ошибка проверки сетей: {e}")
            await msg.answer("❌ Ошибка при проверке сетей. Попробуйте позже.")
            await state.clear()
    else:  # stock
        await state.update_data(asset_name=asset_name)
        # Переходим сразу к timeframe
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="5 мин", callback_data="tf_5min"),
             types.InlineKeyboardButton(text="1 час", callback_data="tf_1h")],
            [types.InlineKeyboardButton(text="1 день", callback_data="tf_1d"),
             types.InlineKeyboardButton(text="1 неделя", callback_data="tf_1w")],
            [types.InlineKeyboardButton(text="1 месяц", callback_data="tf_1m"),
             types.InlineKeyboardButton(text="Полгода", callback_data="tf_6m")],
            [types.InlineKeyboardButton(text="1 год", callback_data="tf_1y")]
        ])
        out = await msg.answer("Выберите горизонт прогноза:", reply_markup=markup)
        await add_fsm_message_id(state, out.message_id)
        await state.set_state(MarketPrognozState.timeframe)

# --- Новый шаг: Выбор сети для крипты (inline) ---
@router.callback_query(StateFilter(MarketPrognozState.network), F.data.startswith("network_"))
async def network_inline_step(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    network = cb.data.split("_")[1].upper()
    data = await state.get_data()
    available_networks = data.get('available_networks', [])

    if network not in available_networks:
        await cb.message.edit_text(f"❌ {network} не доступна. Выберите из кнопок.")
        return

    category = data.get('available_categories', {}).get(network, 'linear')
    await state.update_data(network=network, category=category)

    # Proceed to timeframe
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="5 мин", callback_data="tf_5min"),
         types.InlineKeyboardButton(text="1 час", callback_data="tf_1h")],
        [types.InlineKeyboardButton(text="1 день", callback_data="tf_1d"),
         types.InlineKeyboardButton(text="1 неделя", callback_data="tf_1w")],
        [types.InlineKeyboardButton(text="1 месяц", callback_data="tf_1m"),
         types.InlineKeyboardButton(text="Полгода", callback_data="tf_6m")],
        [types.InlineKeyboardButton(text="1 год", callback_data="tf_1y")]
    ])
    await cb.message.edit_text("Выберите горизонт прогноза:", reply_markup=markup)
    await state.set_state(MarketPrognozState.timeframe)

# --- Шаг 4: Получение срока и подтверждение ---
@router.callback_query(StateFilter(MarketPrognozState.timeframe), F.data.startswith("tf_"))
async def timeframe_step(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()

    timeframe_map = {
        "tf_5min": "5 мин", "tf_1h": "1 час", "tf_1d": "1 день",
        "tf_1w": "1 неделя", "tf_1m": "1 месяц", "tf_6m": "Полгода", "tf_1y": "1 год"
    }
    timeframe = timeframe_map.get(cb.data)
    timeframe_code = tf_to_code.get(timeframe)
    await state.update_data(timeframe=timeframe, timeframe_code=timeframe_code)

    data = await state.get_data()
    asset_type_map = {"crypto": "Криптовалюта", "stock": "Акция"}

    summary = (
        f"📋 Проверьте данные:\n"
        f"Тип: {asset_type_map.get(data['asset_type'])}\n"
        f"Актив: {data['asset_name']}\n"
        f"Сеть: {data.get('network', 'N/A')}\n"  # Добавляем сеть, если есть
        f"Срок: {data['timeframe']}"
    )

    buttons = [
        [types.InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_market_prognoz")],
        [types.InlineKeyboardButton(text="🔄 Начать заново", callback_data="restart_market_prognoz")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await cb.message.edit_text(summary, reply_markup=markup)
    await state.set_state(MarketPrognozState.confirm)

# --- Перезапуск FSM ---
@router.callback_query(F.data == 'restart_market_prognoz', StateFilter(MarketPrognozState.confirm))
async def restart_market_prognoz(cb: types.CallbackQuery, state: FSMContext):
    # Просто вызываем стартовый хендлер заново
    data = await state.get_data()
    cb.data = 'new_ob_prognoz' if data.get('prog_type') == 'ob' else 'new_rach_prognoz'
    await market_prognoz_start(cb, state)

@router.callback_query(F.data == 'confirm_market_prognoz', StateFilter(MarketPrognozState.confirm))
async def confirm_market_prognoz(cb: types.CallbackQuery, state: FSMContext):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)

    await cb.message.edit_text("⏳ Собираю и анализирую рыночные данные... Это может занять до 30 секунд.")
    await cb.answer()

    data = await state.get_data()
    prog_type = data['prog_type']

    # --- Списание прогнозов ---
    user = await get_user(user_id)
    ob_cnt, rach_cnt, ob_vr, rach_vr = user[4], user[5], user[6], user[7]
    if prog_type == 'ob':
        if ob_vr <= 0 and ob_cnt <= 0:
            await bot.send_message(user_id, translations_2.translations[lang]['NOT_od_prognoz'])
            return await process_profile_redirect(user_id)
    else:
        if rach_vr <= 0 and rach_cnt <= 0:
            await bot.send_message(user_id, translations_2.translations[lang]['NOT_VIP_prognoz'])
            return await process_profile_redirect(user_id)
    async with aiosqlite.connect('users.db') as udb:
        if prog_type == 'ob':
            await udb.execute(
                "UPDATE users SET ob_vr_prognoz = ob_vr_prognoz - 1 WHERE id = ?" if ob_vr > 0 else "UPDATE users SET ob_prognoz = ob_prognoz - 1 WHERE id = ?",
                (user_id,))
        else:
            await udb.execute(
                "UPDATE users SET rach_vr_prognoz = rach_vr_prognoz - 1 WHERE id = ?" if rach_vr > 0 else "UPDATE users SET rach_prognoz = rach_prognoz - 1 WHERE id = ?",
                (user_id,))
        await udb.commit()
    forecast_type = 'forecast_ob' if prog_type == 'ob' else 'forecast_vip'
    usage_type = 'usage_ob' if prog_type == 'ob' else 'usage_vip'
    async with aiosqlite.connect('payments.db') as pdb:
        await pdb.execute("INSERT INTO payments (user_id, type, amount, count, timestamp) VALUES (?, ?, ?, ?, ?)",
                          (user_id, forecast_type, 0, -1, int(time.time())))
        await pdb.execute("INSERT INTO payments (user_id, type, amount, count, timestamp) VALUES (?, ?, ?, ?, ?)",
                          (user_id, usage_type, 0, 1, int(time.time())))
        await pdb.commit()

    try:
        # 1. Получаем РАСШИРЕННЫЕ данные с помощью обновленной функции
        asset_name = data['asset_name']
        timeframe_code = data['timeframe_code']
        network = data.get('network', '')  # Для крипты, если есть

        # Динамический limit для TF (меньше для длинных, чтобы избежать ошибок API)
        if timeframe_code in ['5m', '1h']:
            limit = 500
        elif timeframe_code in ['1d', '1w']:
            limit = 365  # 1 год дней или ~7 лет недель
        elif timeframe_code in ['1m']:
            limit = 120  # 10 лет месяцев
        else:  # '6m', '1y'
            limit = 240  # 20 лет месяцев для аггрегации

        is_vip = (prog_type != 'ob')  # True для VIP, False для обычного - идеально подходит под логику

        if data['asset_type'] == 'stock':
            market_data = await get_stock_data(asset_name, interval=timeframe_code, limit=limit)
            logging.info(f"Market data for {asset_name}: {market_data}")  # Для просмотра в консоли full data
            if market_data is None:
                await cb.message.edit_text(
                    "❌ Монета не найдена. Попробуйте другой тикер (e.g., BTCUSDT, ETHUSDT) или напишите по-другому.")
                await state.clear()
                return
        else:
            # Для крипты: формируем full symbol = asset_name + network
            full_symbol = asset_name + network
            category = data.get('category', 'linear')
            market_data = await get_market_data(full_symbol, timeframe_code, limit=limit, is_vip=is_vip, category=category)  # Добавили category
            logging.info(f"Market data for {full_symbol}: {market_data}")  # Для просмотра в консоли
            if not market_data or not market_data.get('kline_data'):
                await cb.message.edit_text(f"❌ No historical data for {full_symbol} on this timeframe. Try another network or shorter TF.")
                await state.clear()
                return

        if not market_data or "atr" not in market_data or len(market_data['kline_data']) == 0:
            logging.error(f"No data or empty kline for {asset_name}")
            error_text = f"❌ Не удалось получить полные данные для актива {asset_name}. Возможно, тикер указан неверно или актив неликвиден. Попробуйте другой."
            await cb.message.edit_text(error_text)
            await state.clear()
            return

        # 2. Форматируем ВСЕ данные для промпта (расширили для новых полей)
        market_data_string = (
            f"- Asset: {market_data.get('symbol', 'N/A')}\n"
            f"- Current Price: {market_data.get('current_price', 0)}\n"
            f"- 24h Change: {market_data.get('price_change_24h_percent', 0):.2f}%\n"
            f"--- Technicals ---\n"
            f"- Trend (EMA20 vs EMA50): {market_data.get('trend_condition', 'N/A')}\n"
            f"- EMA20: {market_data.get('ema_20', 0):.2f}\n"
            f"- EMA50: {market_data.get('ema_50', 0):.2f}\n"
            f"- RSI(14): {market_data.get('rsi', 0):.2f}\n"
            f"- Volatility (ATR % of Price): {market_data.get('volatility_percent', 0):.2f}%\n"
            f"- Bollinger High: {market_data.get('bollinger_high', 0):.2f}\n"
            f"- Bollinger Low: {market_data.get('bollinger_low', 0):.2f}\n"
            f"- Support: {market_data.get('support_level', 0):.2f}\n"
            f"- Resistance: {market_data.get('resistance_level', 0):.2f}\n"
            f"- MACD Trend: {market_data.get('macd_trend', 'N/A')}\n"
            f"- VWAP: {market_data.get('vwap', 0):.2f}\n"
            f"--- Derivatives ---\n"
            f"- Open Interest: ${market_data.get('open_interest_value', 0):,.0f}\n"
            f"- Funding Rate: {market_data.get('funding_rate', 0):.4f}%\n"
            f"--- On-Chain ---\n"
            f"- Netflow: {market_data['onchain']['netflow'].get('value', 0):,.0f} ({market_data['onchain']['netflow'].get('interpretation', 'N/A')})\n"
            f"- LTH SOPR: {market_data['onchain']['sopr'].get('value', 0):.3f} ({market_data['onchain']['sopr'].get('interpretation', 'N/A')})\n"
            f"- MVRV: {market_data['onchain']['mvrv'].get('value', 0):.3f} ({market_data['onchain']['mvrv'].get('interpretation', 'N/A')})\n"
            f"- Puell: {market_data['onchain']['puell'].get('value', 0):.3f} ({market_data['onchain']['puell'].get('interpretation', 'N/A')})\n"
            f"--- Macro ---\n"
            f"- S&P Corr: {market_data['macro'].get('sp500_corr', 0):.2f}\n"
            f"- ETF Inflows: {market_data['macro'].get('etf_inflows', 0):,.0f}\n"
            f"--- Backtest Probs ---\n"
            f"- Up: {market_data['backtest_probs'].get('up', 50)}%\n"
            f"- Base: {market_data['backtest_probs'].get('base', 30)}%\n"
            f"- Down: {market_data['backtest_probs'].get('down', 20)}%"
        )

        # 3. Выбираем нужный промпт
        timeframe_code = data['timeframe_code']
        kit_key = 'REGULAR' if prog_type == 'ob' else 'VIP'
        kit = PROMPT_TF_KIT['ru'][timeframe_code][kit_key]
        system_role = kit['ROLE']
        prompt_task = kit['TASK']

        # Дополнительные параметры для промптов (расширили для новых данных)
        funding_rate = market_data.get('funding_rate', 0)
        params = {
            'symbol': market_data.get('symbol', 'N/A'),
            'current_price': market_data.get('current_price', 0),
            'price_change_24h_percent': market_data.get('price_change_24h_percent', 0),
            'bollinger_high': market_data.get('bollinger_high', 0),
            'bollinger_low': market_data.get('bollinger_low', 0),
            'ema_20': market_data.get('ema_20', 0),
            'ema_50': market_data.get('ema_50', 0),
            'vwap': market_data.get('vwap', 0),
            'rsi': market_data.get('rsi', 50),
            'rsi_zone': 'overbought' if market_data.get('rsi', 50) > 70 else 'oversold' if market_data.get('rsi', 50) < 30 else 'neutral',
            'trend_condition': market_data.get('trend_condition', 'N/A'),
            'macd_trend': market_data.get('macd_trend', 'N/A'),
            'funding_rate': funding_rate,
            'open_interest_value': market_data.get('open_interest_value', 0),
            'volatility_percent': market_data.get('volatility_percent', 0),
            'support_level': market_data.get('support_level', 0),
            'resistance_level': market_data.get('resistance_level', 0),
            'market_data_string': market_data_string,
            # Ручные интерпретации
            'bias': 'бычий' if funding_rate > 0 else 'медвежий' if funding_rate < 0 else 'нейтральный',
            'interpret': market_data['onchain']['netflow'].get('interpretation', 'N/A'),
            # On-chain
            'netflow_interpretation': market_data['onchain']['netflow'].get('interpretation', 'N/A'),
            'sopr_value': market_data['onchain']['sopr'].get('value', 1.0),
            'sopr_interpretation': market_data['onchain']['sopr'].get('interpretation', 'N/A'),
            'mvrv_value': market_data['onchain']['mvrv'].get('value', 0),
            'mvrv_interpretation': market_data['onchain']['mvrv'].get('interpretation', 'N/A'),
            'puell_value': market_data['onchain']['puell'].get('value', 0),
            'puell_interpretation': market_data['onchain']['puell'].get('interpretation', 'N/A'),
            # Macro
            'sp500_corr': market_data['macro'].get('sp500_corr', 0),
            'etf_inflows': market_data['macro'].get('etf_inflows', 0),
            # Probs
            'prob_up': market_data['backtest_probs'].get('up', 50),
            'prob_base': market_data['backtest_probs'].get('base', 30),
            'prob_down': market_data['backtest_probs'].get('down', 20),
            # R/R example calc (simple)
            'rr_ratio': round((market_data.get('resistance_level', 0) - market_data.get('current_price', 0)) / (market_data.get('current_price', 0) - market_data.get('support_level', 0)), 1) if market_data.get('current_price', 0) > market_data.get('support_level', 0) else 1
        }

        final_task = prompt_task.format(**params)

        messages = [
            {"role": "system", "content": system_role},
            {"role": "system", "content": PROMPT_MARKET_KIT_RU["INSTRUCTIONS"]},
            {"role": "user", "content": final_task}
        ]

        # 5. Выполняем запрос к LLM
        resp = client.chat.completions.create(
            model="gemini-2.5-pro-preview",
            messages=messages,
            temperature=0.4
        )

        final_html_response = resp.choices[0].message.content.strip()
        final_html_response = sanitize_telegram_html(final_html_response)

        # 6. Генерация графика с обработкой ошибок
        try:
            kline_len = len(market_data['kline_data'])
            if kline_len < 2:
                raise ValueError(f"Insufficient data: only {kline_len} candles")
            elif kline_len < 14:
                logging.warning(f"Limited data ({kline_len} candles), plotting basic chart")
            chart_buf = plot_chart(market_data, timeframe_code, is_vip=is_vip)
            chart_buf.seek(0)
            photo_input = BufferedInputFile(file=chart_buf.read(), filename='chart.png')
            await bot.send_photo(chat_id=user_id, photo=photo_input, parse_mode="HTML")
            await bot.send_message(user_id, text=final_html_response, parse_mode="HTML")
        except ValueError as ve:
            logging.error(f"График error: {ve}")
            await bot.send_message(user_id, text="⚠️ График недоступен (недостаточно исторических данных). Вот текстовый анализ:")
            await bot.send_message(user_id, text=final_html_response, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Unexpected graph error: {e}\n{traceback.format_exc()}")
            await bot.send_message(user_id, text=final_html_response, parse_mode="HTML")

    except Exception as e:
        logging.error(f"Ошибка при генерации рыночного прогноза: {e}\n{traceback.format_exc()}")
        error_message = "❌ Произошла ошибка при генерации прогноза. Попробуйте позже или обратитесь в поддержку."
        await cb.message.edit_text(error_message)
    finally:
        await delete_fsm_messages(cb.message.chat.id, state)
        await state.clear()
        await asyncio.sleep(1)
        await process_profile_redirect(user_id)

# ============================================
# Основные обработчики команд и сообщений
# ============================================
@router.message(Command("start"))
async def cmd_start(msg: types.Message):
    args = msg.text.removeprefix('/start').strip()
    referrer_id = None
    if args and args.startswith("referral_"):
        try:
            potential_referrer_id = int(args.split("_")[1])
            if potential_referrer_id != msg.from_user.id:
                async with aiosqlite.connect('users.db') as db:
                    async with db.execute("SELECT id FROM users WHERE id = ?", (potential_referrer_id,)) as cursor:
                        if await cursor.fetchone():
                            referrer_id = potential_referrer_id
                        else:
                            logging.warning(f"Неверный ID реферала: {potential_referrer_id}")
        except (IndexError, ValueError) as e:
            logging.warning(f"Неверный формат реферала: {args}, ошибка: {e}")

    user_id = msg.from_user.id

    await add_user(msg.from_user.id, msg.from_user.full_name, referred_by=referrer_id)
    lang = await get_user_lang(user_id)
    if not lang:
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="leng_ru")],
            [types.InlineKeyboardButton(text="🇬🇧 English", callback_data="leng_en")],
            [types.InlineKeyboardButton(text="🇸🇦 العربية", callback_data="leng_ar")],
            [types.InlineKeyboardButton(text="🇪🇸 Español", callback_data="leng_es")],
            [types.InlineKeyboardButton(text="🇨🇳 中文", callback_data="leng_zh")],
            [types.InlineKeyboardButton(text="🇫🇷 Français", callback_data="leng_fr")],
        ])
        await msg.answer_photo(caption="🌐 Please select a language", photo=photo_iaziki, reply_markup=markup)
    else:
        await send_welcome(msg)


@require_subscription("start")
async def send_welcome(message: types.Message):

    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    await setup_bot_commands(lang)
    referral_link = f"https://t.me/{BOT_USERNAME}?start=referral_{user_id}"
    # logging.info(f"Generating referral link for user {user_id}: {referral_link}")
    user_name = message.from_user.full_name
    current_timestamp = int(time.time())
    async with aiosqlite.connect('users.db') as db:
        await db.execute("UPDATE users SET last_active = ? WHERE id = ?", (current_timestamp, user_id))
        await db.commit()
    user = await get_user(user_id)
    if user is None:
        await add_user(user_id, user_name)
        user = await get_user(user_id)
    if user is None:
        await message.answer("Ошибка при получении данных профиля.")
        return

    referred_count = await get_referred_count(user_id)
    current_time = int(time.time())
    remaining = user[3] - current_time
    remaining_str = format_remaining_time(remaining, lang) if user[3] > current_time else "-"
    await setup_bot_commands(lang)
    profile_text = translations_2.translations[lang]['profile_text'].format(
        user_name=user[1],
        user_id=user[0],
        subscription=user[2],
        remaining=remaining_str,
        ob_prognoz=user[4],
        rach_prognoz=user[5],
        ob_vr_prognoz=user[6],
        rach_vr_prognoz=user[7],
        referral_link=referral_link,
        referred_count=referred_count
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['katalog'], callback_data='katalog')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['sozdat_prognoz'], callback_data='prognoz')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['iazik'], callback_data="change_lang"),
         types.InlineKeyboardButton(text=translations_2.translations[lang]['otzivi'], callback_data='otzivi')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['promokod'], callback_data='promokod'),
         types.InlineKeyboardButton(text=translations_2.translations[lang]['support'], callback_data='support_menu')],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['instruction'], callback_data='instruction_menu')]
    ])
    photo_path = translations_2.translations[lang]['photo_profil']
    await send_photo_with_delete(user_id, FSInputFile(photo_path), profile_text, parse_mode="Markdown", reply_markup=markup)



@router.message(Command("admin"))
async def admin_message(message: types.Message):
    admin_ids = [2122289037, 1244773560, 5099581636]  # замените на реальные ID админов
    if message.from_user.id not in admin_ids:
        return await message.answer("⛔ Доступ запрещён")
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='👤 Траферы', callback_data='traferi'),
         types.InlineKeyboardButton(text='#️⃣️ Промокоды', callback_data='promo')],
        [types.InlineKeyboardButton(text='📢 Рассылка', callback_data='start_broadcast'),
         types.InlineKeyboardButton(text='🤝 Партнёры', callback_data='partners')],
        [types.InlineKeyboardButton(text='📊 Статистика бота', callback_data='statistika')],
        [types.InlineKeyboardButton(text='🔙 Выйти из Ад.панели', callback_data='back_admin')]

    ])
    await send_photo_with_delete(user_id, photo_admin_panel, '''
➖➖➖➖➖➖➖➖➖

👨‍💻 *АДМИН ПАНЕЛЬ*

➖➖➖➖➖➖➖➖➖
    ''', parse_mode="Markdown", reply_markup=markup)


@router.message(Command("traffer"))
async def show_my_trafer_data(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)

    # Получаем данные траффера
    async with aiosqlite.connect('traffers.db') as db:
        async with db.execute(
                """
                SELECT trafer_name, trafer_id, trafer_promo, trafer_username, trafer_telefon, trafer_karta, trafer_kripta,
                       pay_model, crypto_network, pay_value, pay_link, invite_link
                FROM traffers 
                WHERE trafer_id = ?
                """,
                (str(user_id),)
        ) as cursor:
            row = await cursor.fetchone()

    if not row:
        await message.answer(text=translations_2.translations[lang]['no_registr_traffera'])
        return

    (t_name, t_id, t_promo, trafer_username, t_telefon, t_karta, t_kripta, pay_model, crypto_network, pay_value, pay_link, invite_link) = row

    # Считаем лидов и пользователей
    # Считаем лидов и пользователей (ИСПРАВЛЕННАЯ ВЕРСИЯ)
    async with aiosqlite.connect('users.db') as udb:
        async with udb.execute(
                "SELECT COUNT(*), GROUP_CONCAT(user_id) FROM used_promocodes WHERE promokod = ?",
                (f"trafer:{t_promo}",)
        ) as cur:
            leads_data = await cur.fetchone()

    # Надежно обрабатываем случай, когда лидов еще нет
    if leads_data:
        leads = leads_data[0]
        users_csv = leads_data[1]
    else:
        leads = 0
        users_csv = None

    users = list(map(int, users_csv.split(','))) if users_csv else []

    # Используем общую функцию для отображения карточки
    await _show_traffer_profile(
        user_id=user_id,
        trafer_name=t_name,
        t_id=t_id,
        trafer_username=trafer_username,
        t_promo=t_promo,
        t_telefon=t_telefon,
        t_karta=t_karta,
        t_kripta=t_kripta,
        crypto_network=crypto_network,
        pay_model=pay_model,
        pay_value=pay_value,
        pay_link=pay_link,
        invite_link=invite_link,
        leads=leads,
        users=users,
        dst=message,
        is_admin=False
    )


# ============================================
# Выплата трафферу
# ============================================
@router.callback_query(lambda c: c.data == 'withdraw')
async def withdraw_start(cb: types.CallbackQuery, state: FSMContext):
    user_id = cb.from_user.id
    total, paid, balance = await get_traffer_balance(user_id)
    lang = await get_user_lang(user_id)

    # Если на балансе меньше 1000 — сообщаем
    if balance < 1000:
        return await cb.answer(
            text=translations_2.translations[lang]['balans_menche_1000'],
            show_alert=True
        )

    # Сохраняем баланс в состояние
    await state.update_data(balance=balance)

    # Убираем всплывающее окно
    await cb.answer()

    # Сообщение от бота — добавить в FSM-сообщения
    msg = await cb.message.answer(
        text=translations_2.translations[lang]['ot_1000_do_balans'].format(balance=balance)
    )
    await add_fsm_message_id(state, msg.message_id)

    # Установка состояния
    await state.set_state(WithdrawState.amount)



@router.message(StateFilter(WithdrawState.amount), F.text)
async def withdraw_amount(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    lang = await get_user_lang(user_id)
    try:
        amt = int(msg.text.strip())
    except:
        return await msg.answer(text=translations_2.translations[lang]['vvedite_celoe_chislo'])
    await add_fsm_message_id(state, msg.message_id)
    data = await state.get_data()
    if amt < 1000:
        return await msg.answer(text=translations_2.translations[lang]['summa_bolche_1000'])
    if amt > data['balance']:
        return await msg.answer(text=translations_2.translations[lang]['summa_bolche_balansa'])
    await add_fsm_message_id(state, msg.message_id)
    await state.update_data(requested=amt)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['redactirovat'], callback_data="withdraw_edit")],
        [types.InlineKeyboardButton(text=translations_2.translations[lang]['podtverdit'], callback_data="withdraw_confirm")]
    ])
    await msg.answer(text=translations_2.translations[lang]['proverka_summi'].format(amt=amt), reply_markup=kb)
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(WithdrawState.confirm)


@router.callback_query(lambda c: c.data.startswith('paid:'))
async def paid_handler(cb: types.CallbackQuery):
    _, user_id, amt = cb.data.split(':')
    user_id, amt = int(user_id), int(amt)
    lang = await get_user_lang(user_id)
    # обновляем БД: помечаем выплату
    async with aiosqlite.connect('traffer_payouts.db') as db:
        await db.execute(
            "INSERT INTO traffer_payouts(trafer_id, amount, timestamp, status) VALUES(?,?,?,?)",
            (user_id, amt, int(time.time()), 'done')
        )
        await db.commit()
    # уведомляем траффера, если он начал чат
    try:
        await bot.send_message(user_id, text=translations_2.translations[lang]['yes_viplata'].format(amt=amt))
    except TelegramForbiddenError:
        # не начинал диалог — можно залогировать или пропустить
        pass
    # удаляем сообщение у админа
    async with aiosqlite.connect('traffer_payouts.db') as db:
        async with db.execute(
                "SELECT admin_id, message_id FROM withdraw_notifications WHERE trafer_id = ? AND amount = ?",
                (user_id, amt)
        ) as cursor:
            rows = await cursor.fetchall()
        for admin_id, message_id in rows:
            try:
                await bot.delete_message(chat_id=admin_id, message_id=message_id)
            except Exception as e:
                print(f"❌ Не удалось удалить сообщение у админа {admin_id}: {e}")
        # Удаляем записи из таблицы
        await db.execute(
            "DELETE FROM withdraw_notifications WHERE trafer_id = ? AND amount = ?",
            (user_id, amt)
        )
        await db.commit()

    await cb.message.delete()


@router.callback_query(lambda c: c.data.startswith('decline:'))
async def decline_handler(cb: types.CallbackQuery):
    _, user_id, amt = cb.data.split(':')
    user_id, amt = int(user_id), int(amt)
    lang = await get_user_lang(user_id)
    # логируем отказ
    async with aiosqlite.connect('traffer_payouts.db') as db:
        await db.execute(
            "INSERT INTO traffer_payouts(trafer_id, amount, timestamp, status) VALUES(?,?,?,?)",
            (user_id, amt, int(time.time()), 'declined')
        )
        await db.commit()
    # уведомляем траффера, если он начал чат
    try:
        await bot.send_message(user_id, text=translations_2.translations[lang]['no_viplata'].format(amt=amt))
    except TelegramForbiddenError:
        pass
    await cb.message.delete()


@router.callback_query(lambda c: c.data == 'withdraw_edit', StateFilter(WithdrawState.confirm))
async def withdraw_edit(cb: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await cb.answer()
    await cb.message.delete()
    await delete_fsm_messages(cb.from_user.id, state)
    return await withdraw_start(cb, state)


@router.callback_query(
    lambda c: c.data == 'withdraw_confirm',
    StateFilter(WithdrawState.confirm)
)
async def withdraw_confirm(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.delete()
    data = await state.get_data()
    amt = data.get('requested')
    user_id = cb.from_user.id
    await delete_fsm_messages(user_id, state)

    # 1) Попробуем отправить сообщение администраторам
    admin_ids = [2122289037, 1244773560, 5099581636]
    sent_to_someone = False

    for aid in admin_ids:
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Сделал выплату", callback_data=f"paid:{user_id}:{amt}")
            ],
            [
                types.InlineKeyboardButton(text="Выплата не принята", callback_data=f"decline:{user_id}:{amt}")
            ]
        ])
        try:
            msg = await bot.send_message(
                chat_id=aid,
                text=(
                    f"🟡 Запрос выплаты от "
                    f"{cb.from_user.full_name} ({user_id}): {amt}₽"
                ),
                reply_markup=kb
            )
            # Сохраняем message_id
            async with aiosqlite.connect('traffer_payouts.db') as db:
                await db.execute(
                    "INSERT INTO withdraw_notifications (trafer_id, amount, admin_id, message_id) VALUES (?, ?, ?, ?)",
                    (user_id, amt, aid, msg.message_id)
                )
                await db.commit()
            sent_to_someone = True
        except TelegramForbiddenError:
            print(f"❌ Не удалось отправить админу {aid} (возможно, не писал боту)")
            continue

    # 2) Если хотя бы одному админу отправили — подтверждаем трафферу
    if sent_to_someone:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"ℹ️ Ваш запрос на вывод {amt}₽ отправлен и будет обработан."
            )
        except TelegramForbiddenError:
            # fallback — не пишем ничего
            pass
        await cb.answer("✅ Запрос отправлен администраторам.", show_alert=True)
    else:
        # 3) Ни одному админу не удалось отправить — говорим трафферу
        await cb.answer("⚠️ Не удалось связаться с администрацией.\nНапишите в поддержку: @suportneyroteam",
                        show_alert=True)

    # 4) Чистим FSM
    await state.clear()


# ============================================
# Статистика бота — полностью заменяет старый блок
# ============================================
def get_period_start(period: str) -> datetime:
    """Возвращает datetime начала периода (UTC, timezone-aware)."""
    now = datetime.now(timezone.utc)
    if period == 'week':
        start = now - timedelta(days=now.isoweekday() - 1)
        return start.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == 'month':
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if period == 'year':
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # all time
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def stats_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="За неделю", callback_data="stats:week"),
                types.InlineKeyboardButton(text="За месяц", callback_data="stats:month"),
            ],
            [
                types.InlineKeyboardButton(text="За год", callback_data="stats:year"),
                types.InlineKeyboardButton(text="За все время", callback_data="stats:all"),
            ],
            [
                types.InlineKeyboardButton(text="↩️ Назад в админ-панель", callback_data="back_admin_panel")
            ]
        ]
    )


@router.callback_query(F.data == 'statistika')
async def cmd_stats(callback: types.CallbackQuery):
    """Показываем кнопки выбора периода."""
    await callback.message.edit_caption(  # Используем edit_caption, так как работаем с фото
        caption="📊 Статистика бота\nВыберите период:",
        reply_markup=stats_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('stats:'))
async def process_stats_callback(callback: types.CallbackQuery):
    period = callback.data.split(':', 1)[1]
    start_dt = get_period_start(period)
    # Конвертируем datetime в Unix timestamp для сравнения в БД
    start_ts = int(start_dt.timestamp()) if period != 'all' else 0

    # --- Сбор данных ---

    # 1. Пользователи (из users.db)
    # ПРИМЕЧАНИЕ: В таблице 'users' нет даты регистрации, поэтому статистика по
    # новым пользователям за период невозможна. Здесь показано общее число.
    users_total = 0
    users_by_lang_rows = []
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            users_total = (await cur.fetchone())[0] or 0
        async with db.execute("SELECT lang, COUNT(*) as cnt FROM users GROUP BY lang") as cur:
            users_by_lang_rows = await cur.fetchall()

    # 2. Прогнозы и подписки (из payments.db)
    normal_used = 0
    vip_used = 0
    normal_issued = 0
    vip_issued = 0
    gross = 0
    subs = {'standart': 0, 'medium': 0, 'premium': 0} # Исправлено 'Medium' на 'medium' для консистентности
    async with aiosqlite.connect('payments.db') as db:
        # Использованные прогнозы
        async with db.execute("SELECT COUNT(*) FROM payments WHERE type = 'usage_ob' AND timestamp >= ?",
                              (start_ts,)) as cur:
            normal_used = (await cur.fetchone())[0] or 0
        async with db.execute("SELECT COUNT(*) FROM payments WHERE type = 'usage_vip' AND timestamp >= ?",
                              (start_ts,)) as cur:
            vip_used = (await cur.fetchone())[0] or 0

        # Выданные (купленные) прогнозы
        async with db.execute("SELECT SUM(count) FROM payments WHERE type = 'forecast_ob' AND timestamp >= ?",
                              (start_ts,)) as cur:
            normal_issued = (await cur.fetchone())[0] or 0
        async with db.execute("SELECT SUM(count) FROM payments WHERE type = 'forecast_vip' AND timestamp >= ?",
                              (start_ts,)) as cur:
            vip_issued = (await cur.fetchone())[0] or 0

        # Валовая прибыль (все пополнения и покупки)
        async with db.execute("SELECT SUM(amount) FROM payments WHERE amount > 0 AND timestamp >= ?",
                              (start_ts,)) as cur:
            gross = (await cur.fetchone())[0] or 0

        # Покупки подписок (считаем по цене, так как в 'payments' нет названия плана)
        async with db.execute(
                "SELECT COUNT(*) FROM payments WHERE type = 'subscription' AND amount = ? AND timestamp >= ?",
                (PRICES['standart'], start_ts)) as cur:
            subs['standart'] = (await cur.fetchone())[0] or 0
        async with db.execute(
                "SELECT COUNT(*) FROM payments WHERE type = 'subscription' AND amount = ? AND timestamp >= ?",
                (PRICES['medium'], start_ts)) as cur:
            subs['medium'] = (await cur.fetchone())[0] or 0
        async with db.execute(
                "SELECT COUNT(*) FROM payments WHERE type = 'subscription' AND amount = ? AND timestamp >= ?",
                (PRICES['premium'], start_ts)) as cur:
            subs['premium'] = (await cur.fetchone())[0] or 0

    # 3. Выплаты трафферам (из traffer_payouts.db)
    paid_out = 0
    async with aiosqlite.connect('traffer_payouts.db') as db:
        async with db.execute("SELECT SUM(amount) FROM traffer_payouts WHERE status = 'done' AND timestamp >= ?",
                              (start_ts,)) as cur:
            paid_out = (await cur.fetchone())[0] or 0

    # ============================================
    # НОВЫЕ РАСЧЕТЫ РАСХОДОВ
    # ============================================

    # Расчет расхода на прогнозы (использованные прогнозы перемножаютсмя на соответствующую им цену)
    expenses_on_predictions = (normal_used * REGULAR_PREDICTION_PRICE) + \
                              (vip_used * VIP_PREDICTION_PRICE)

    # Общие расходы (ЗП трафферам + расход на прогнозы)
    total_expenses = paid_out + expenses_on_predictions

    # --- Форматирование текста ---

    # Формируем блок по языкам
    flags = {'ru': '🇷🇺', 'en': '🇬🇧', 'ar': '🇸🇦', 'es': '🇪🇸', 'zh': '🇨🇳', 'fr': '🇫🇷'}
    lang_stats = ''.join(
        f"   • {flags.get(lang, '❓')} {(lang or 'N/A').capitalize()} – {cnt}\n"
        for lang, cnt in users_by_lang_rows
    ) if users_by_lang_rows else "   • Данных нет\n"

    # Метки периода и информация о сбросе
    labels = {'week': 'За неделю', 'month': 'За месяц', 'year': 'За год', 'all': 'За все время'}
    label = labels[period]

    reset_info_msg = ""
    # Для статистики "за всё время" дата сброса не нужна
    if period != 'all':
        if period == 'week':
            next_dt = start_dt + timedelta(days=7)
        elif period == 'month':
            # Корректный расчет следующего месяца
            next_dt = (start_dt.replace(day=28) + timedelta(days=4)).replace(day=1)
        else:  # year
            next_dt = start_dt.replace(year=start_dt.year + 1, month=1, day=1)
        reset_info_msg = f"(Cброс {next_dt.strftime('%d.%m.%Y')})"

    # Итоговый текст
    text = (
        "📊 *Статистика бота*\n"
        "➖➖➖➖➖➖➖➖➖\n\n"
        f"⏰ *{label}* {reset_info_msg}:\n\n"
        f"👥 *Всего пользователей:* {users_total}\n\n"
        f"🌐 *Пользователи по языкам:*\n{lang_stats}\n"
        f"🔹 *Обычные прогнозы*\n"
        f"   • Выдано (куплено) – {normal_issued}\n"
        f"   • Использовано – {normal_used}\n\n"
        f"💠 *VIP‑прогнозы*\n"
        f"   • Выдано (куплено) – {vip_issued}\n"
        f"   • Использовано – {vip_used}\n\n"
        f"🎫 *Покупки подписок*\n"
        f"   • Standart – {subs.get('standart', 0)}\n"
        f"   • Medium – {subs.get('medium', 0)}\n"
        f"   • Premium – {subs.get('premium', 0)}\n\n"
        f"💸 *Финансы:*\n\n"
        f"💰 Валовая прибыль – {gross}₽\n\n"
        f"💸 _ЗП трафферам – {paid_out}₽_\n"
        f"📈 _Расход на прогнозы – {expenses_on_predictions}₽_\n" # НОВАЯ СТРОКА
        f"📉 *Итого расходов – {total_expenses}₽*\n\n" # НОВАЯ СТРОКА
        f"🏦 *Чистая прибыль – {gross - total_expenses}₽*\n\n" # ОБНОВЛЕННЫЙ РАСЧЕТ
        "➖➖➖➖➖➖➖➖➖"
    )

    # Редактируем сообщение с фото, изменяя caption
    await callback.message.edit_caption(
        caption=text,
        reply_markup=stats_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

# ============================================
# Рассылка
# ============================================

# 2. Словарь доступных кнопок (ключ → spec)
BUTTONS = {
    "Поддержка": {"text": "support", "url": "https://t.me/suportneyroteam"},
    "Создать прогноз": {"text": "sozdat_prognoz", "callback_data": "prognoz"},
    "Каталог": {"text": "katalog", "callback_data": "katalog"},
    "Прогнозы": {"text": "prognozi", "callback_data": "prognozi"},
    "Подписки": {"text": "podpiski", "callback_data": "subscriptions"},
    "Промокод": {"text": "promokod", "callback_data": "promokod"},
    "Отзывы": {"text": "otzivi", "callback_data": "otzivi"},
    "Инструкция": {"text": "instruction", "url": "https://telegra.ph/Instrukciya-SPORT-ANALITIK-BOT-04-02"},
}

class AdminStates(StatesGroup):
    waiting_for_language_choice = State()
    waiting_for_broadcast = State()
    waiting_for_row_count = State()
    waiting_for_row_buttons = State()
    waiting_for_custom_text = State()
    waiting_for_custom_url = State()
    waiting_for_media_choice = State()
    collecting_photo = State()
    collecting_video = State()
    waiting_for_broadcast_confirmation = State()

@router.callback_query(F.data == "start_broadcast")
async def start_broadcast(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(message_ids=[])
    lang_map = {
        'ru': '🇷🇺 Русский', 'en': '🇬🇧 English', 'ar': '🇸🇦 العربية',
        'es': '🇪🇸 Español', 'zh': '🇨🇳 中文', 'fr': '🇫🇷 Français'
    }
    buttons = [
        types.InlineKeyboardButton(text=name, callback_data=f"bcast_lang_{code}")
        for code, name in lang_map.items()
    ]
    rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    rows.append([types.InlineKeyboardButton(text="🌍 Всем пользователям", callback_data="bcast_lang_all")])
    rows.append([types.InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_broadcast")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=rows)
    msg = await callback.message.answer("📢 Выберите аудиторию для рассылки:", reply_markup=markup)
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.waiting_for_language_choice)

@router.callback_query(StateFilter(AdminStates.waiting_for_language_choice), F.data.startswith("bcast_lang_"))
async def process_language_choice(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    lang = callback.data.split("_")[-1]
    data = await state.get_data()
    await state.update_data(target_lang=lang, photos=[], videos=[], message_ids=data["message_ids"])
    msg = await callback.message.edit_text("✉️ Теперь введите текст рассылки (HTML разрешён):")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.waiting_for_broadcast)

@router.callback_query(F.data == "cancel_broadcast", StateFilter(AdminStates))
async def cancel_broadcast(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_fsm_messages(callback.message.chat.id, state)
    await state.clear()

@router.message(StateFilter(AdminStates.waiting_for_broadcast), F.text)
async def process_broadcast_text(message: types.Message, state: FSMContext):
    # трекаем сообщение админа
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(broadcast_message=message.html_text)
    msg = await message.answer("❓ Сколько рядов кнопок будет под сообщением? Введите целое число (0 - если без кнопок):")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.waiting_for_row_count)

@router.message(StateFilter(AdminStates.waiting_for_row_count), F.text)
async def process_row_count(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    if not message.text.isdigit() or int(message.text) < 0:
        return await message.answer("⚠ Введите корректное неотрицательное число рядов:")
    rows = int(message.text)
    await state.update_data(row_count=rows, current_row=1, rows_buttons=[])
    if rows == 0:
        msg = await message.answer("Нет кнопок, переходим к медиавыбору.")
        await add_fsm_message_id(state, msg.message_id)
        return await ask_for_media(message, state)
    keys = "\n".join(f"— {k}" for k in BUTTONS) + "\n— link"
    msg = await message.answer(f"📋 Введите через запятую метки кнопок для ряда №1:\n\n{keys}")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.waiting_for_row_buttons)

@router.message(StateFilter(AdminStates.waiting_for_row_buttons), F.text)
async def process_row_buttons(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    data = await state.get_data()
    labels = [l.strip() for l in message.text.split(",")]
    invalid = [l for l in labels if l not in BUTTONS and l != "link"]
    if invalid:
        return await message.answer(f"⚠ Некорректные метки: {', '.join(invalid)}.")
    btns = [{"type":"predefined","label":l} if l in BUTTONS else {"type":"custom"} for l in labels]
    rows = data["rows_buttons"] + [btns]
    await state.update_data(rows_buttons=rows, current_row=data["current_row"]+1)
    if data["current_row"] < data["row_count"]:
        keys = "\n".join(f"— {k}" for k in BUTTONS) + "\n— link"
        msg = await message.answer(f"📋 Ряд №{data['current_row']+1}: {keys}")
        await add_fsm_message_id(state, msg.message_id)
    else:
        # кастомные?
        custom = [(i,j) for i,row in enumerate(rows) for j,b in enumerate(row) if b["type"]=="custom"]
        if custom:
            await state.update_data(custom_positions=custom, current_custom_index=0)
            i,j = custom[0]
            msg = await message.answer(f"Введите текст для кастомной кнопки в ряду {i+1}, позиции {j+1}:")
            await add_fsm_message_id(state, msg.message_id)
            await state.set_state(AdminStates.waiting_for_custom_text)
        else:
            await ask_for_media(message, state)

@router.message(StateFilter(AdminStates.waiting_for_custom_text))
async def process_custom_text(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    data = await state.get_data()
    i,j = data["custom_positions"][data["current_custom_index"]]
    rows = data["rows_buttons"]
    rows[i][j]["text"] = message.text
    await state.update_data(rows_buttons=rows)
    msg = await message.answer(f"Введите URL для кастомной кнопки в ряду {i+1}, позиции {j+1}:")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.waiting_for_custom_url)

@router.message(StateFilter(AdminStates.waiting_for_custom_url))
async def process_custom_url(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    data = await state.get_data()
    idx = data["current_custom_index"]
    i,j = data["custom_positions"][idx]
    rows = data["rows_buttons"]
    rows[i][j]["url"] = message.text
    await state.update_data(rows_buttons=rows)
    if idx+1 < len(data["custom_positions"]):
        await state.update_data(current_custom_index=idx+1)
        ni,nj = data["custom_positions"][idx+1]
        msg = await message.answer(f"Введите текст для кастомной кнопки в ряду {ni+1}, позиции {nj+1}:")
        await add_fsm_message_id(state, msg.message_id)
        await state.set_state(AdminStates.waiting_for_custom_text)
    else:
        await ask_for_media(message, state)

async def ask_for_media(message: types.Message, state: FSMContext):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📸 Добавить фото", callback_data="add_photo")],
        [types.InlineKeyboardButton(text="🎥 Добавить видео", callback_data="add_video")],
        [types.InlineKeyboardButton(text="⏩ Пропустить", callback_data="skip_media")]
    ])
    msg = await message.answer("Добавить ещё медиа к рассылке?", reply_markup=kb)
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.waiting_for_media_choice)

@router.callback_query(StateFilter(AdminStates.waiting_for_media_choice), F.data=="add_photo")
async def start_collecting_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    msg = await callback.message.edit_text("📸 Отправьте одно фото для рассылки.")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.collecting_photo)

@router.message(StateFilter(AdminStates.collecting_photo), F.photo)
async def add_photo(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(photo=message.photo[-1].file_id)
    msg = await message.answer("✅ Фото добавлено.")
    await add_fsm_message_id(state, msg.message_id)
    await preview_broadcast(message, state)

@router.callback_query(StateFilter(AdminStates.waiting_for_media_choice), F.data=="add_video")
async def start_collecting_video(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    msg = await callback.message.edit_text("🎥 Отправьте одно видео для рассылки.")
    await add_fsm_message_id(state, msg.message_id)
    await state.set_state(AdminStates.collecting_video)

@router.message(StateFilter(AdminStates.collecting_video), F.video)
async def add_video(message: types.Message, state: FSMContext):
    await add_fsm_message_id(state, message.message_id)
    await state.update_data(video=message.video.file_id)
    msg = await message.answer("✅ Видео добавлено.")
    await add_fsm_message_id(state, msg.message_id)
    await preview_broadcast(message, state)

@router.callback_query(StateFilter(AdminStates.waiting_for_media_choice), F.data=="skip_media")
async def skip_media(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await preview_broadcast(callback.message, state)

async def preview_broadcast(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data["broadcast_message"]
    rows = data.get("rows_buttons", [])
    lang = data["target_lang"] if data["target_lang"] != "all" else "ru"

    kb = types.InlineKeyboardMarkup(inline_keyboard=[])
    for row in rows:
        btns = []
        for b in row:
            if b["type"] == "predefined":
                spec = BUTTONS[b["label"]]
                tkey = spec["text"]
                txt = translations_2.translations[lang].get(tkey, tkey)
                btns.append(types.InlineKeyboardButton(
                    text=txt,
                    url=spec.get("url"),
                    callback_data=spec.get("callback_data")
                ))
            else:
                btns.append(types.InlineKeyboardButton(
                    text=b.get("text", "Кастом"), url=b.get("url")
                ))
        kb.inline_keyboard.append(btns)

    media_info = "📸 Фото прикреплено" if data.get("photo") else \
                 "🎥 Видео прикреплено" if data.get("video") else "📄 Без медиа"
    caption = f"👀 Предпросмотр рассылки:\n\n{text}\n\n{media_info}"
    if data.get("photo"):
        msg = await message.answer_photo(photo=data["photo"], caption=caption,
                                         reply_markup=kb, parse_mode=ParseMode.HTML)
    elif data.get("video"):
        msg = await message.answer_video(video=data["video"], caption=caption,
                                         reply_markup=kb, parse_mode=ParseMode.HTML)
    else:
        msg = await message.answer(caption, reply_markup=kb, parse_mode=ParseMode.HTML)
    await add_fsm_message_id(state, msg.message_id)

    confirm_kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_broadcast"),
        types.InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_broadcast")
    ]])
    msg2 = await message.answer("Выберите действие:", reply_markup=confirm_kb)
    await add_fsm_message_id(state, msg2.message_id)
    await state.update_data(preview_kb=kb)
    await state.set_state(AdminStates.waiting_for_broadcast_confirmation)

@router.callback_query(StateFilter(AdminStates.waiting_for_broadcast_confirmation), F.data=="confirm_broadcast")
async def confirm_and_send_broadcast(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # сразу удаляем ВСЕ накопленные FSM‑сообщения, включая текущее
    await delete_fsm_messages(callback.message.chat.id, state)

    # показываем toast вместо edit_text
    await callback.answer(f"⏳ Начинаю рассылку для аудитории: {data['target_lang']}", show_alert=False)

    # собираем список пользователей
    async with aiosqlite.connect('users.db') as db:
        sql = "SELECT id FROM users" if data["target_lang"]=="all" else "SELECT id FROM users WHERE lang=?"
        params = () if data["target_lang"]=="all" else (data["target_lang"],)
        cursor = await db.execute(sql, params)
        user_ids = [r[0] for r in await cursor.fetchall()]

    # рассылаем
    sent = failed = 0
    text, kb = data["broadcast_message"], data["preview_kb"]
    photo, video = data.get("photo"), data.get("video")
    for uid in user_ids:
        try:
            if photo:
                await bot.send_photo(chat_id=uid, photo=photo, caption=text[:1024],
                                     reply_markup=kb, parse_mode=ParseMode.HTML)
            elif video:
                await bot.send_video(chat_id=uid, video=video, caption=text[:1024],
                                     reply_markup=kb, parse_mode=ParseMode.HTML)
            else:
                await bot.send_message(chat_id=uid, text=text,
                                       reply_markup=kb, parse_mode=ParseMode.HTML)
            sent += 1
        except:
            failed += 1
        await asyncio.sleep(0.05)

    # отчет о завершении
    await bot.send_message(callback.message.chat.id,
                           f"✅ Рассылка завершена!\n\n👍 Отправлено: {sent}\n👎 Не удалось доставить: {failed}")
    await state.clear()


@router.callback_query(StateFilter(AdminStates.waiting_for_broadcast_confirmation), F.data=="edit_broadcast")
async def edit_broadcast(callback: types.CallbackQuery, state: FSMContext):
    # удаляем ВСЁ, включая сообщение с кнопками действия
    await delete_fsm_messages(callback.message.chat.id, state)
    await state.clear()
    # запуск заново
    await callback.answer()
    await start_broadcast(callback, state)



@router.callback_query(F.data.startswith("leng_"))
async def set_language_handler(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    lang_code = cb.data.split("_")[1]  # 'ru', 'en', 'ar', 'es', 'zh', 'fr'
    await set_user_lang(user_id, lang_code)
    await cb.answer(text=translations_2.translations[lang_code]['iazik_yes'])
    await cb.message.delete()
    await send_partners_list(user_id, next_action="start")


@router.callback_query(F.data == "change_lang")
async def change_lang_menu(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="leng_ru")],
        [types.InlineKeyboardButton(text="🇬🇧 English", callback_data="leng_en")],
        [types.InlineKeyboardButton(text="🇸🇦 العربية", callback_data="leng_ar")],
        [types.InlineKeyboardButton(text="🇪🇸 Español", callback_data="leng_es")],
        [types.InlineKeyboardButton(text="🇨🇳 中文", callback_data="leng_zh")],
        [types.InlineKeyboardButton(text="🇫🇷 Français", callback_data="leng_fr")],
    ])

    await send_photo_with_delete(user_id, photo_iaziki, translations_2.translations[lang]['vibr_iazik'], parse_mode="Markdown",
                                 reply_markup=markup)
    await cb.answer()


# ============================================
# НОВЫЙ БЛОК: Обработчики для Инструкции
# ============================================
@router.callback_query(F.data == 'instruction_menu')
async def show_instruction_menu(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)
    trans = translations_2.translations[lang]

    # Создаем кнопки для каждого блока инструкции
    buttons = []
    for key, value in trans['instruction_blocks'].items():
        buttons.append([types.InlineKeyboardButton(text=value['title'], callback_data=f"instruction_block_{key}")])

    # Добавляем кнопку для полной инструкции и кнопку "Назад"
    buttons.append([types.InlineKeyboardButton(text=trans['full_instruction_button'], url=trans['instruction_link'])])
    buttons.append([types.InlineKeyboardButton(text=trans['back'], callback_data='back')])

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    photo_path = translations_2.translations[lang]['photo_instruction']
    # Используем плейсхолдер для фото
    await send_photo_with_delete(user_id, FSInputFile(photo_path), trans['instruction_menu_header'],
                                 parse_mode=ParseMode.HTML, reply_markup=markup)
    await cb.answer()


@router.callback_query(F.data.startswith('instruction_block_'))
async def show_instruction_block(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)
    block_key = cb.data.split('_')[-1]

    trans = translations_2.translations[lang]
    block = trans['instruction_blocks'].get(block_key)

    if not block:
        await cb.answer("Block not found!", show_alert=True)
        return

    text = f"<b>{block['title']}</b>\n\n➖➖➖➖➖➖➖➖➖\n{block['text']}\n➖➖➖➖➖➖➖➖➖"
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=trans['back'], callback_data='instruction_menu')]
    ])

    photo_path = translations_2.translations[lang]['photo_instruction']
    await send_photo_with_delete(user_id, FSInputFile(photo_path), text, parse_mode=ParseMode.HTML,
                                 reply_markup=markup)
    await cb.answer()


# ============================================
# НОВЫЙ БЛОК: Обработчики для Поддержки и FAQ
# ============================================
@router.callback_query(F.data == 'support_menu')
async def show_support_menu(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)
    trans = translations_2.translations[lang]

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=trans['faq_button'], callback_data='faq_menu')],
        [types.InlineKeyboardButton(text=trans['contact_support_button'], url='https://t.me/suportneyroteam')],
        [types.InlineKeyboardButton(text=trans['back'], callback_data='back')]
    ])

    photo_path = translations_2.translations[lang]['photo_support']
    await send_photo_with_delete(user_id, FSInputFile(photo_path), trans['support_menu_header'],
                                 parse_mode=ParseMode.HTML, reply_markup=markup)
    await cb.answer()


@router.callback_query(F.data == 'faq_menu')
async def show_faq_menu(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)
    trans = translations_2.translations[lang]

    buttons = []
    for key, value in trans['faq_items'].items():
        buttons.append([types.InlineKeyboardButton(text=value['question'], callback_data=f"faq_question_{key}")])

    buttons.append([types.InlineKeyboardButton(text=trans['back'], callback_data='support_menu')])

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    photo_path = translations_2.translations[lang]['photo_faq']
    await send_photo_with_delete(user_id, FSInputFile(photo_path), trans['faq_menu_header'], parse_mode=ParseMode.HTML,
                                 reply_markup=markup)
    await cb.answer()


@router.callback_query(F.data.startswith('faq_question_'))
async def show_faq_answer(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    lang = await get_user_lang(user_id)
    question_key = cb.data.replace('faq_question_', '')

    trans = translations_2.translations[lang]
    item = trans['faq_items'].get(question_key)

    if not item:
        await cb.answer("Question not found!", show_alert=True)
        return

    text = f"<b>{item['question']}</b>\n\n➖➖➖➖➖➖➖➖➖\n{item['answer']}\n➖➖➖➖➖➖➖➖➖"
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=trans['back'], callback_data='faq_menu')]
    ])

    photo_path = translations_2.translations[lang]['photo_faq']
    await send_photo_with_delete(user_id, FSInputFile(photo_path), text, parse_mode=ParseMode.HTML, reply_markup=markup)
    await cb.answer()


# Убедись, что этот обработчик зарегистрирован в твоем диспетчере (dp.include_router(router))
@router.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data
    lang = await get_user_lang(user_id)

    if data == 'standart':
        # Обновляем подписку
        await update_subscription(user_id, "Standart", add_ob_vr=5, add_rach_vr=0, duration_seconds=7 * 24 * 3600)

        # Берём цену из PRICES
        price_for_sub = PRICES.get('standart', 0)

        # Записываем оплату в payments.db с реальной суммой
        async with aiosqlite.connect('payments.db') as db:
            await db.execute(
                "INSERT INTO payments (user_id, type, amount, timestamp) VALUES (?, ?, ?, ?)",
                (user_id, 'subscription', price_for_sub, int(time.time()))
            )
            await db.commit()

        # Отправляем ответ пользователю
        await callback_query.answer(text=translations_2.translations[lang]['standart'], show_alert=False)

        await give_referral_reward(user_id)

        await process_profile_redirect(user_id)



    elif data == 'medium':
        # Обновляем подписку
        await update_subscription(user_id, "Medium", add_ob_vr=12, add_rach_vr=6, duration_seconds=7 * 24 * 3600)

        # Берём цену из PRICES
        price_for_sub = PRICES.get('medium', 0)

        # Записываем оплату в payments.db с реальной суммой
        async with aiosqlite.connect('payments.db') as db:
            await db.execute(
                "INSERT INTO payments (user_id, type, amount, timestamp) VALUES (?, ?, ?, ?)",
                (user_id, 'subscription', price_for_sub, int(time.time()))
            )
            await db.commit()

        # Отправляем ответ пользователю
        await callback_query.answer(text=translations_2.translations[lang]['medium'], show_alert=False)

        await give_referral_reward(user_id)

        # Обновляем профиль (как было в оригинальном коде)
        await process_profile_redirect(user_id)



    elif data == 'premium':
        # Обновляем подписку
        await update_subscription(user_id, "Premium", add_ob_vr=30, add_rach_vr=15, duration_seconds=14 * 24 * 3600)

        # Берём цену из PRICES
        price_for_sub = PRICES.get('premium', 0)

        # Записываем оплату в payments.db с реальной суммой
        async with aiosqlite.connect('payments.db') as db:
            await db.execute(
                "INSERT INTO payments (user_id, type, amount, timestamp) VALUES (?, ?, ?, ?)",
                (user_id, 'subscription', price_for_sub, int(time.time()))
            )
            await db.commit()

        # Отправляем ответ пользователю
        await callback_query.answer(text=translations_2.translations[lang]['premium'], show_alert=False)

        await give_referral_reward(user_id)

        # Обновляем профиль (как было в оригинальном коде)
        await process_profile_redirect(user_id)


    # Пример обработки показа профиля с информацией о подписке
    elif data == 'profile' or data == 'back':
        user_id = callback_query.from_user.id
        await process_profile_redirect(user_id)
        await callback_query.answer()


    elif data == 'subskribes':
        # подставляем цены из PRICES
        price_standart = PRICES['standart']
        price_medium = PRICES['medium']
        price_premium = PRICES['premium']

        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=f'{price_standart}₽ - Standart',
                        callback_data='standart'
                    ),
                    types.InlineKeyboardButton(
                        text=f'{price_medium}₽ - Medium',
                        callback_data='medium'
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text=f'{price_premium}₽ - Premium',
                        callback_data='premium'
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text='↩️ Назад',
                        callback_data='back_k'
                    )
                ]
            ]
        )
        photo_path = translations_2.translations[lang]['photo_katalog_subscriptions']
        await send_photo_with_delete(
            user_id,
            FSInputFile(photo_path), translations_2.translations[lang]['katalog_podpisok'].format(
                price_standart=price_standart,
                price_medium=price_medium,
                price_premium=price_premium
            ),
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif data == 'katalog' or data == 'back_k':

        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=translations_2.translations[lang]['podpiski'], callback_data='subskribes'),
                    types.InlineKeyboardButton(text=translations_2.translations[lang]['prognozi'], callback_data='prognozi')
                ],
                [
                    types.InlineKeyboardButton(text=translations_2.translations[lang]['back'], callback_data='back')
                ]
            ]
        )

        photo_path = translations_2.translations[lang]['photo_katalog']
        await send_photo_with_delete(user_id, FSInputFile(photo_path), translations_2.translations[lang]['catalog_text'], reply_markup=markup)


    elif data == 'prognozi':

        # подставляем цены из PRICES
        price_1_ob = PRICES['1_ob_prognoz']
        price_5_ob = PRICES['5_ob_prognoz']
        price_15_ob = PRICES['15_ob_prognoz']
        price_1_vip = PRICES['1_rach_prognoz']
        price_5_vip = PRICES['5_rach_prognoz']
        price_15_vip = PRICES['15_rach_prognoz']

        markup = types.InlineKeyboardMarkup(

            inline_keyboard=[
                [types.InlineKeyboardButton(text=translations_2.translations[lang]['1_ob_prognoz'].format(price_1_ob=price_1_ob), callback_data='1_ob_prognoz'),
                 types.InlineKeyboardButton(text=translations_2.translations[lang]['1_rach_prognoz'].format(price_1_vip=price_1_vip), callback_data='1_rach_prognoz')],
                [types.InlineKeyboardButton(text=translations_2.translations[lang]['5_ob_prognoz'].format(price_5_ob=price_5_ob), callback_data='5_ob_prognoz'),
                 types.InlineKeyboardButton(text=translations_2.translations[lang]['5_rach_prognoz'].format(price_5_vip=price_5_vip), callback_data='5_rach_prognoz')],
                [types.InlineKeyboardButton(text=translations_2.translations[lang]['15_ob_prognoz'].format(price_15_ob=price_15_ob), callback_data='15_ob_prognoz'),
                 types.InlineKeyboardButton(text=translations_2.translations[lang]['15_rach_prognoz'].format(price_15_vip=price_15_vip), callback_data='15_rach_prognoz')],
                [types.InlineKeyboardButton(text=translations_2.translations[lang]['back'], callback_data='back_k')]
            ]
        )
        photo_path = translations_2.translations[lang]['photo_katalog_prognoz']
        await send_photo_with_delete(user_id, FSInputFile(photo_path), translations_2.translations[lang]['katalog_prognozov'].format(

                price_1_ob=price_1_ob, price_5_ob=price_5_ob, price_15_ob=price_15_ob,

                price_1_vip=price_1_vip, price_5_vip=price_5_vip, price_15_vip=price_15_vip

            ),

            reply_markup=markup,

            parse_mode="Markdown"

        )

        # main_2_updated.py (НАЙТИ И ЗАМЕНИТЬ ЭТОТ elif)

    elif data == 'prognoz':
        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    # Эти кнопки теперь будут запускать новую FSM
                    types.InlineKeyboardButton(text=translations_2.translations[lang]['ob_prognoz'],
                                               callback_data='new_ob_prognoz'),
                    types.InlineKeyboardButton(text=translations_2.translations[lang]['vip_prognoz'],
                                               callback_data='new_rach_prognoz')
                ],
                [
                    types.InlineKeyboardButton(text=translations_2.translations[lang]['profile'],
                                               callback_data='profile')
                ],
                [
                    types.InlineKeyboardButton(text=translations_2.translations[lang]['instruction'],
                                               url=translations_2.translations[lang]['instruction_link'])
                ]
            ]
        )
        photo_path = translations_2.translations[lang]['photo_tip_prognoza']
        await send_photo_with_delete(user_id, FSInputFile(photo_path),
                                     translations_2.translations[lang]['vibirite_tip_prognoza'], parse_mode="Markdown",
                                     reply_markup=markup)

    # elif data == 'prognoz':
    #     markup = types.InlineKeyboardMarkup(
    #         inline_keyboard=[
    #             [
    #                 types.InlineKeyboardButton(text=translations_2.translations[lang]['ob_prognoz'], callback_data='new_ob_prognoz'),
    #                 types.InlineKeyboardButton(text=translations_2.translations[lang]['vip_prognoz'], callback_data='new_rach_prognoz')
    #             ],
    #             [
    #                 types.InlineKeyboardButton(text=translations_2.translations[lang]['profile'], callback_data='profile')
    #             ],
    #             [
    #                 types.InlineKeyboardButton(text=translations_2.translations[lang]['instruction'],
    #                                            url=translations_2.translations[lang]['instruction_link'])
    #             ]
    #         ]
    #     )
    #     photo_path = translations_2.translations[lang]['photo_tip_prognoza']
    #     await send_photo_with_delete(user_id, FSInputFile(photo_path), translations_2.translations[lang]['vibirite_tip_prognoza'], parse_mode="Markdown", reply_markup=markup)

    elif data == 'otzivi':
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=translations_2.translations[lang]['read_otzivi'], url='https://t.me/OTZIVISPORTANALITIK'),
             types.InlineKeyboardButton(text=translations_2.translations[lang]['ostvit_otziv'], url='https://t.me/OtzivNeyroTeambot')],
            [types.InlineKeyboardButton(text=translations_2.translations[lang]['back'], callback_data='back')]
        ])
        photo_path = translations_2.translations[lang]['photo_otzivi']
        await send_photo_with_delete(user_id, FSInputFile(photo_path), reply_markup=markup)

    # Пример для кнопок прогнозов
    # ── INSERT INTO your process_callback() HANDLER ──
    elif data in ['1_ob_prognoz', '5_ob_prognoz', '15_ob_prognoz', '1_rach_prognoz', '5_rach_prognoz',
                  '15_rach_prognoz']:
        # determine VIP vs ordinary
        is_vip = data.endswith('rach_prognoz')
        # map button → count
        count_map = {
            '1_ob_prognoz': 1, '5_ob_prognoz': 5, '15_ob_prognoz': 15,
            '1_rach_prognoz': 1, '5_rach_prognoz': 5, '15_rach_prognoz': 15,
        }
        count = count_map[data]
        user_id = callback_query.from_user.id

        # 1) Credit the user
        if not is_vip:
            await update_ob_prognoz(user_id, count)
        else:
            await update_rach_prognoz(user_id, count)

        # 2) Log the “purchase” в payments.db: динамическая цена из PRICES
        purchase_type = 'forecast_ob' if not is_vip else 'forecast_vip'
        price_for_button = PRICES.get(data, 0)
        async with aiosqlite.connect('payments.db') as pay_db:
            await pay_db.execute(
                "INSERT INTO payments (user_id, type, amount, count, timestamp) VALUES (?, ?, ?, ?, ?)",
                (user_id, purchase_type, price_for_button, count, int(time.time()))
            )
            await pay_db.commit()

        # 3) Feedback & refresh profile
        label = translations_2.translations[lang]['vip_prognozov'] if is_vip else translations_2.translations[lang]['ob_progozov']
        await callback_query.answer(text=translations_2.translations[lang]['dobavleno_prognozov'].format(count=count, label=label), show_alert=True)

        await give_referral_reward(user_id)

        await process_profile_redirect(user_id)




    elif data == 'traferi':
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='👥 Список траферов', callback_data='baza_traferov')],
            [types.InlineKeyboardButton(text='🆕 Добавить трафера', callback_data='new_trafer')],
            [types.InlineKeyboardButton(text='↩️ Назад', callback_data='back_admin_panel')]
        ])
        await send_photo_with_delete(user_id, photo_admin_panel, '''
➖➖➖➖➖➖➖➖➖

⚙️ *Управление траферами*

➖➖➖➖➖➖➖➖➖
            ''', parse_mode="Markdown", reply_markup=markup)

    elif data == 'back_admin_panel':
        markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text='👤 Траферы', callback_data='traferi'),
             types.InlineKeyboardButton(text='#️⃣️ Промокоды', callback_data='promo')],
            [types.InlineKeyboardButton(text='📢 Рассылка', callback_data='start_broadcast'),
             types.InlineKeyboardButton(text='🤝 Партнёры', callback_data='partners')],
            [types.InlineKeyboardButton(text='📊 Статистика бота', callback_data='statistika')],
            [types.InlineKeyboardButton(text='🔙 Выйти из Ад.панели', callback_data='back_admin')]
        ])
        await send_photo_with_delete(user_id, photo_admin_panel, '''
➖➖➖➖➖➖➖➖➖

👨‍💻 *АДМИН ПАНЕЛЬ*

➖➖➖➖➖➖➖➖➖
            ''', parse_mode="Markdown", reply_markup=markup)


# ============================================
# Основная точка входа
# ============================================
async def on_startup():
    logging.basicConfig(level=logging.ERROR, filename='bot.log', format='%(asctime)s - %(levelname)s - %(message)s')
    await init_databases()
    # await init_partners_db()
    # await remove_invalid_partners()
    # await init_db()
    # await init_traffers_db()
    # await init_promocodes_db()
    # await init_used_promocodes_db()
    asyncio.create_task(check_expired_subscriptions())
    # await setup_bot_commands()
    # await init_payments_db()  # ✅ добавь вот эту строку
    # await init_payouts_db()
    load_coins_list()


async def main():

    await init_databases()
    # await init_db()
    # await init_partners_db()
    # await init_payments_db()
    # await init_traffers_db()
    # await init_promocodes_db()
    # await init_payouts_db()
    # await setup_bot_commands()
    # 2) Регистрируем роутеры
    dp.include_router(router)
    # 3) Запускаем polling
    await polling_with_retry(dp, bot)

if __name__ == '__main__':
    asyncio.run(main())

