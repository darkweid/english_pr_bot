from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, URLInputFile
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType

# Создаем кнопки Reply
btn_training: KeyboardButton = KeyboardButton(
    text='Тренажер по грамматике')
btn_new_words: KeyboardButton = KeyboardButton(
    text='Новые слова')
btn_exit: KeyboardButton = KeyboardButton(
    text='Выход')
btn_ok_go: KeyboardButton = KeyboardButton(
    text='Ок, начинаем')
btn_FSM_zero: KeyboardButton = KeyboardButton(
    text='[Сбросить машину состояний]')
btn_show_answer: KeyboardButton = KeyboardButton(
    text='Покажи ответ')

btn_lvl1: KeyboardButton = KeyboardButton(
    text='Уровень 1')
btn_lvl2: KeyboardButton = KeyboardButton(
    text='Уровень 2')
btn_lvl3: KeyboardButton = KeyboardButton(
    text='Уровень 3')

# Создаем объекты Reply–клавиатуры

kb_training_or_new_words: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[btn_training, btn_new_words], [btn_FSM_zero]],
    resize_keyboard=True)
kb_training_go: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[btn_ok_go], [btn_FSM_zero]],
    resize_keyboard=True)
kb_training_in_game: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[btn_show_answer],[btn_exit], [btn_FSM_zero]],
    resize_keyboard=True)
kb_training_choise_lvl: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[btn_lvl1, btn_lvl2, btn_lvl3], [btn_exit], [btn_FSM_zero]],
    resize_keyboard=True)

# Создаем кнопки Inline
# button: InlineKeyboardButton = InlineKeyboardButton(
#    text='---', url=url_blabla)


# Создаем объекты Inline–клавиатуры
