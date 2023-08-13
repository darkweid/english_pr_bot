from aiogram.fsm.context import FSMContext
import asyncio, random, json

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
# from keyboards.kb_utils import create_inline_kb, create_reply_kb
from keyboards.keyboards import (kb_training_or_new_words, kb_training_go, kb_training_choise_lvl, kb_training_in_game)
from states.states import FSMtraining, FSMdict
from files.dicts import (dict_training_words1, dict_training_words2, dict_training_words3, dict_dicts,
                         list_right_answers)
from sqlite_db import create_profile, edit_profile, edit_hw_done, check_hw, dict_hw, update_progress, get_progress

user_router: Router = Router()
main_dict = {}
done_lst = []


@user_router.message(F.text == '[Сбросить машину состояний]')
async def training_new(message: Message, state: FSMContext):
    await message.answer('Сброшено!')
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/start" -
@user_router.message(Command(commands=["start"]), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await create_profile(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(f"""Привет! Я бот от Оли Прус : )
\nПомогаю людям изучать английский.
Пока что у меня две функции:
– тренажер по грамматике
– запоминание новых слов
\n⬇️ Выбери, с чего начнём сегодня ⬇️""", reply_markup=kb_training_or_new_words)


# Этот хэндлер будет срабатывать на команду "/start" -
@user_router.message(Command(commands=['start']), ~StateFilter(default_state))
@user_router.message(F.text == 'Выход', ~StateFilter(default_state))
async def process_start_command_patron(message: Message, state: FSMContext):
    await message.answer(f"""⬇️ Чем займёмся сегодня? ⬇️""", reply_markup=kb_training_or_new_words)


@user_router.message((F.text == 'Тренажер по грамматике'),
                     StateFilter(default_state))  # Показываем правила новому пользователю
async def training_new(message: Message, state: FSMContext):
    await message.answer(f"""Окей, правила простые: я пишу на русском, ты переводишь на английский.
Если ответы не совпадут, можешь сразу подглядеть ответ или попробовать ещё раз""", reply_markup=kb_training_go)
    await state.set_state(FSMtraining.in_process)


# Кнопку нажал пользователь, знающий правила
@user_router.message(F.text == ('Тренажер по грамматике'),
                     ~StateFilter(default_state))
@user_router.message(F.text == ('Ок, начинаем'),
                     ~StateFilter(default_state))
async def training_old(message: Message, state: FSMContext):
    global main_dict, level, word, done_lst
    print(done_lst)
    done_lst = await get_progress(message.from_user.id)
    await update_progress(message.from_user.id)
    level = await check_hw(message.from_user.id)
    main_dict = dict_dicts[level]
    await message.answer(f"""Ты находишься на уровне {level}""")
    word = random.choice([s for s in list(main_dict.values()) if s not in done_lst])
    await message.answer(f'Переводи следующее:\n{word}', reply_markup=ReplyKeyboardRemove)
    await state.set_state(FSMtraining.in_process)


@user_router.message(F.text == 'Покажи ответ', StateFilter(FSMtraining.in_process))
async def show_answer(message: Message, state: FSMContext):
    global word
    inv_dict = {value: key for key, value in main_dict.items()}
    await message.answer(inv_dict[word])
    word = random.choice([s for s in list(main_dict.values()) if s not in done_lst])
    await message.answer(f'На ошибках учатся, так что продолжаем 😊\nПереводи следующее:\n{word}')


@user_router.message(StateFilter(FSMtraining.in_process))
async def check_translation(message: Message, state: FSMContext):
    global word, done_lst, main_dict, level
    print('1', done_lst)

    await update_progress(message.from_user.id)
    msg = message.text.lower()
    try:
        if main_dict[msg].lower() == word.lower():
            done_lst.append(word)
            try:
                await update_progress(message.from_user.id, done_lst)
            except Exception as err:
                print('error')
            await message.answer(random.choice(list_right_answers))
            if len(done_lst) == len(main_dict):  # Все предложения переведены, переход на следующий уровень
                await message.answer('Поздравляю! Ты перевел все предложения из этого уровня!')
                await edit_hw_done(message.from_user.id, dict_hw[level])  # отправляем в БД инфу, что уровень выполнен
                level = await check_hw(message.from_user.id)  # загружаем номер невыполненного задания
                done_lst = []  # обнуляем список переведенных предложений
                await update_progress(message.from_user.id)  # обнуляем список переведенных в БД
                main_dict = dict_dicts[level]  # меняем словарь на новый уровень
                await message.answer(f"""Теперь ты находишься на уровне {level}""")
                word = random.choice([s for s in list(main_dict.values()) if s not in done_lst])
                await message.answer(f'Переводи следующее:\n{word}', reply_markup=ReplyKeyboardRemove)
            else:  # переведены не все предложения, переводим следующее
                word = random.choice([s for s in list(main_dict.values()) if
                                      s not in done_lst])  # Выбираем случайное предложение, которое еще не было использовано
                await message.answer(f'Переведи:\n{word}', reply_markup=ReplyKeyboardRemove)

        else:
            await message.answer('Хм, у меня другой ответ 🤔\nПопробуй ещё раз или попроси меня подсказать ответ 😉',
                                 reply_markup=kb_training_in_game)
    except KeyError:
        await message.answer('Хм, у меня другой ответ 🤔\nПопробуй ещё раз или попроси меня подсказать ответ 😉',
                             reply_markup=kb_training_in_game)


@user_router.message()
async def send_idontknow(message: Message):
    await message.reply(f'{message.from_user.first_name}, я всего лишь бот, я не знаю, что на это ответить🤷🏼‍♀')
