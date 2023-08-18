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
from states.states import FSMadmin
from files.dicts import (dict_dicts, list_right_answers)
from sqlite_db import (create_profile, edit_hw_done, edit_hw_undone, check_hw, dict_hw, update_progress,
                       get_progress,
                       get_users_dict, see_user_hw_progress)


# Функция для формирования инлайн-клавиатуры на лету
# Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     last_btn: str | None = None,
                     **kwargs: dict) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=text))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data=last_btn))

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
    text='Посмотреть прогресс ученика', callback_data='see_progress')
button_edit_hw: InlineKeyboardButton = InlineKeyboardButton(
    text='Изменить выполненные ДЗ', callback_data='edit_hw')
button_see_done_words: InlineKeyboardButton = InlineKeyboardButton(
    text='Посмотреть выученные группы слов', callback_data='Посмотреть выученные слова')
button_exit: InlineKeyboardButton = InlineKeyboardButton(text='Выход', callback_data='Выход')

keyboard_adm: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_see_progress], [button_edit_hw], [button_see_done_words]])

keyboard_exit: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_exit]])


# admin_handlers
@admin_router.message(Command(commands=["admin"]))
async def process_admin_command(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Что будем делать, хозяин?', reply_markup=keyboard_adm)
        await state.set_state(FSMadmin.admin)
    else:
        await message.answer('Вам сюда нельзя')


@admin_router.callback_query(F.data == 'see_progress', StateFilter(FSMadmin.admin))
async def see_progress(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMadmin.see_progress_hw)
    DICT = await get_users_dict()
    await callback.message.edit_text(text='Чей прогресс будем смотреть?',
                                     reply_markup=create_inline_kb(1, last_btn='Выход', **DICT))


@admin_router.callback_query(F.data == 'edit_hw', StateFilter(FSMadmin.admin))
async def edit_hw(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMadmin.edit_hw)
    DICT = await get_users_dict()
    await callback.message.edit_text(text='Чей прогресс по ДЗ изменить?',
                                     reply_markup=create_inline_kb(1, last_btn='Выход', **DICT))


@admin_router.callback_query(F.data == 'Посмотреть выученные слова', StateFilter(FSMadmin.admin))
async def see_done_words(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMadmin.progress_words)
    DICT = await get_users_dict()
    await callback.message.edit_text(text='Чей прогресс по выученным словам будем смотреть?',
                                     reply_markup=create_inline_kb(1, last_btn='Выход', **DICT))


@admin_router.callback_query(F.data == 'Выход', StateFilter(FSMadmin.see_progress_hw))
@admin_router.callback_query(F.data == 'Выход', StateFilter(FSMadmin.edit_hw))
@admin_router.callback_query(F.data == 'Выход', StateFilter(FSMadmin.progress_words))
@admin_router.callback_query(F.data == 'Выход', StateFilter(FSMadmin.edit_hw))
@admin_router.callback_query(F.data == 'Выход',StateFilter(FSMadmin.edit_hw_got_user_id))
@admin_router.callback_query(F.data == 'Выход',StateFilter(FSMadmin.edit_hw_got_user_id_and_hw_number))
async def exit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Что будем делать, хозяин?', reply_markup=keyboard_adm)
    await state.set_state(FSMadmin.admin)


@admin_router.callback_query(StateFilter(FSMadmin.see_progress_hw))
async def edit_hw_process1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=await see_user_hw_progress(callback.data.split(':')[0]),
                                     reply_markup=keyboard_exit)


@admin_router.callback_query(StateFilter(FSMadmin.edit_hw))
async def edit_hw_process2(callback: CallbackQuery, state: FSMContext):
    global user_id
    DICT = {str(value): str(key) for key, value in dict_hw.items()}
    user_id = (callback.data.split(':')[0])
    await state.set_state(FSMadmin.edit_hw_got_user_id)
    await callback.message.edit_text(text='Какое ДЗ изменить?',
                                     reply_markup=create_inline_kb(4, last_btn='Выход', **DICT))


@admin_router.callback_query(StateFilter(FSMadmin.edit_hw_got_user_id))
async def edit_hw_process3(callback: CallbackQuery, state: FSMContext):
    global hw_number
    hw_number = int(callback.data)
    await callback.message.edit_text(text='Какое состояние установить?',
                                     reply_markup=create_inline_kb(2, btn_done='✅ Выполнено ✅',
                                                                   btn_undone='❌ Не выполнено ❌', last_btn='Выход'))
    await state.set_state(FSMadmin.edit_hw_got_user_id_and_hw_number)
    print(type(callback.from_user.id))


@admin_router.callback_query(StateFilter(FSMadmin.edit_hw_got_user_id_and_hw_number))
async def edit_hw_process4(callback: CallbackQuery, state: FSMContext):
    global hw_number, user_id
    if callback.data == '✅ Выполнено ✅':
        await edit_hw_done((user_id), dict_hw[hw_number])
        await callback.answer('Изменено успешно!', show_alert=True)
        await update_progress(user_id)              #сбрасываем предложения "в процессе"

    elif callback.data == '❌ Не выполнено ❌':
        await edit_hw_undone((user_id), dict_hw[hw_number])
        await callback.answer('Изменено успешно!', show_alert=True)
        await update_progress(user_id)              #сбрасываем предложения "в процессе"
