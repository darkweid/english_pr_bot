from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, URLInputFile
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Создаем кнопки Reply

btn_FSM_zero: KeyboardButton = KeyboardButton(
    text='[Сбросить машину состояний]')

# Создаем объекты Reply–клавиатуры


# Создаем кнопки Inline
btn_training_rules: InlineKeyboardButton = InlineKeyboardButton(
    text='🙋‍♀️ Посмотреть правила 🙋', callback_data='Посмотреть правила тренажера')
btn_training_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='Тренажер по грамматике', callback_data='Тренажер по грамматике')
btn_verbs_rules: InlineKeyboardButton = InlineKeyboardButton(
    text='🙋‍♀️ Посмотреть правила 🙋', callback_data='Посмотреть правила глаголы')
btn_verbs: InlineKeyboardButton = InlineKeyboardButton(
    text='Изучение неправильных глаголов', callback_data='Изучение неправильных глаголов')
btn_new_words_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='Новые слова[в разработке]', callback_data='Новые слова')
btn_show_answer_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='🔎 Показать ответ 🔍', callback_data='Показать ответ')
btn_show_verb_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='🔎 Показать ответ 🔍', callback_data='Показать глагол')
btn_show_verb_fail_inl: InlineKeyboardButton = InlineKeyboardButton(
    text='🔎 Показать ответ 🔍', callback_data='Показать глагол при ошибке')
btn_main_menu: InlineKeyboardButton = InlineKeyboardButton(
    text='Главное меню', callback_data='Главное меню')

# Создаем объекты Inline–клавиатуры
kb_training_rules_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_training_rules]])
kb_verbs_rules_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_verbs_rules]])
kb_training_or_verbs_or_new_words_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_training_inl], [btn_verbs], [btn_new_words_inl]])
kb_training_in_game_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_show_answer_inl]])
kb_in_verbs_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_show_verb_inl]])
kb_in_verbs_fail_inline: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_show_verb_fail_inl]])
kb_main_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[btn_main_menu]])


######              Генератор клавиатур для тренажера по изучению слов                  ######
def create_inline_kb_words(width: int, rules: bool | bool = False, contin: bool | bool = False,
                           last_btn: str | None = None,
                           **kwargs: dict) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()  # Инициализируем билдер
    buttons: list[InlineKeyboardButton] = []  # Инициализируем список для кнопок

    if rules:
        kb_builder.row(InlineKeyboardButton(  # Добавляем в билдер первую кнопку
            text='🙋‍♀️ Посмотреть правила 🙋',
            callback_data='Посмотреть правила слова'))

    if contin:
        kb_builder.row(InlineKeyboardButton(  # Добавляем в билдер первую кнопку
            text='Продолжить последний раздел',
            callback_data='Продолжить'))

    if kwargs:  # Заполняем список кнопками из аргументов args и kwargs
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=text))

    kb_builder.row(*buttons, width=width)  # Распаковываем список с кнопками в билдер методом row c параметром width

    if last_btn:  # Добавляем в билдер последнюю кнопку, если она передана в функцию
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data=last_btn))

    return kb_builder.as_markup()  # Возвращаем объект инлайн-клавиатуры
    kb_builder.row(*buttons, width=width)  # Распаковываем список с кнопками в билдер методом row c параметром width
    return kb_builder.as_markup()  # Возвращаем объект инлайн-клавиатуры


######              Генератор клавиатур для админки                  ######
def create_inline_kb_admin(width: int,
                           last_btn: str | None = None,
                           **kwargs: dict) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()  # Инициализируем билдер
    buttons: list[InlineKeyboardButton] = []  # Инициализируем список для кнопок

    if kwargs:  # Заполняем список кнопками из аргументов args и kwargs
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=text))

    kb_builder.row(*buttons, width=width)  # Распаковываем список с кнопками в билдер методом row c параметром width

    if last_btn:  # Добавляем в билдер последнюю кнопку, если она передана в функцию
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data=last_btn))

    return kb_builder.as_markup()  # Возвращаем объект инлайн-клавиатуры
    kb_builder.row(*buttons, width=width)  # Распаковываем список с кнопками в билдер методом row c параметром width
    return kb_builder.as_markup()  # Возвращаем объект инлайн-клавиатуры
