from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Создаем кнопки Reply
btn_training: KeyboardButton = KeyboardButton(text='Тренажер по грамматике')
btn_new_words: KeyboardButton = KeyboardButton(
  text='Новые слова [В разработке]')
btn_exit: KeyboardButton = KeyboardButton(text='Выход')
btn_ok_go: KeyboardButton = KeyboardButton(text='Ок, начинаем')
btn_ok_got_it: KeyboardButton = KeyboardButton(text='Ок, понятно')
btn_FSM_zero: KeyboardButton = KeyboardButton(
  text='[Сбросить машину состояний]')
btn_show_answer: KeyboardButton = KeyboardButton(text='Покажи ответ')

# Создаем объекты Reply–клавиатуры

kb_rules: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_ok_got_it]],
                                                    resize_keyboard=True)

kb_training_or_new_words: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  keyboard=[[btn_training, btn_new_words]], resize_keyboard=True)
kb_training_go: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  keyboard=[[btn_ok_go]], resize_keyboard=True)
kb_training_in_game: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  keyboard=[[btn_show_answer], [btn_exit]], resize_keyboard=True)

# Создаем кнопки Inline
# button: InlineKeyboardButton = InlineKeyboardButton(
#    text='---', url=url_blabla)

# Создаем объекты Inline–клавиатуры
