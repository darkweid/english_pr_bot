from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, URLInputFile
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType

# Создаем кнопки Reply

btn_FSM_zero: KeyboardButton = KeyboardButton(
    text='[Сбросить машину состояний]')

# Создаем объекты Reply–клавиатуры


# Создаем кнопки Inline
btn_training_rules: InlineKeyboardButton = InlineKeyboardButton(
    text='🙋‍♀️ Посмотреть правила 🙋', callback_data='Посмотреть правила тренажера')
btn_training_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='Тренажер по грамматике', callback_data='Тренажер по грамматике')
btn_new_words_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='Новые слова[в разработке]', callback_data='Новые слова')
btn_show_answer_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='🔎 Показать ответ 🔍', callback_data='Показать ответ')
btn_main_menu: InlineKeyboardButton = InlineKeyboardButton(
    text='Главное меню', callback_data='Главное меню')

# Создаем объекты Inline–клавиатуры
kb_training_rules_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_training_rules]])
kb_training_or_new_words_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_training_inl], [btn_new_words_inl]])
kb_training_in_game_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_show_answer_inl]])
kb_main_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_main_menu]])
