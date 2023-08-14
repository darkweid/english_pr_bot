from aiogram.fsm.context import FSMContext
import asyncio, random, json, csv, time
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, URLInputFile
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_data.config import Config, load_config
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
# from keyboards.kb_utils import create_inline_kb, create_reply_kb
from keyboards.keyboards import (kb_training_or_new_words, kb_training_go,
                                 kb_training_choise_lvl, kb_training_in_game)
from states.states import FSMtraining
from files.dicts import (dict_dicts, list_right_answers)
from sqlite_db import (create_profile, edit_profile, edit_hw_done, check_hw, dict_hw, update_progress, get_progress, get_users_list)



# Функция для формирования инлайн-клавиатуры на лету
# Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     *args: str,
                     last_btn: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
                            text=last_btn,
                            callback_data='last_btn'))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
admin_router: Router = Router()
config: Config = load_config()
ADMINS: list = config.tg_bot.admin_ids
superadmin = ADMINS[0]

# admin_keyboards

button_see_progress: InlineKeyboardButton = InlineKeyboardButton(
    text='Посмотреть прогресс ученика', callback_data='progress')
button_edit_hw: InlineKeyboardButton = InlineKeyboardButton(
    text='Изменить выполненные ДЗ', callback_data='Изменить ДЗ')
button_see_done_words: InlineKeyboardButton = InlineKeyboardButton(
    text='Посмотреть выученные группы слов', callback_data='Посмотреть выученные слова')
big_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 1',
    callback_data='big_button_1_pressed')

keyboard_adm: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_see_progress],[ button_edit_hw], [button_see_done_words]])

# admin_handlers
@admin_router.message(Command(commands=["admin"]),F.from_user.id == superadmin)
async def process_admin_command(message: Message, state: FSMContext):
    await message.answer('Что будем делать, хозяин?', reply_markup= keyboard_adm)
    print(superadmin)
    await state.set_state(FSMtraining.admin)


#@admin_router.callback_query(Text(text=['progress']))
#async def see_progress(callback: CallbackQuery):
#    await callback.message.answer('Прогресс ученика')
@admin_router.callback_query((F.data=='Изменить ДЗ'), StateFilter(FSMtraining.admin))
async def edit_hw(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Изменить ДЗ')
@admin_router.callback_query(F.data == 'Посмотреть выученные слова')
async def see_done_words(callback: CallbackQuery):
    await callback.message.answer('Посмотреть выученные слова')
    await callback.answer()

@admin_router.callback_query(F.data=='progress')
async def process_button_2_press(callback: CallbackQuery):
    #await callback.message.edit_text(
     #   text='Была нажата КНОПКА ',
     #   reply_markup=callback.message.reply_markup)
    await callback.message.answer('printed')
    await get_users_list()

