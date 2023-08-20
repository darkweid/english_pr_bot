from aiogram.fsm.context import FSMContext
import asyncio, random, json, csv, time

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
# from keyboards.kb_utils import create_inline_kb, create_reply_kb
from keyboards.keyboards import (kb_training_or_new_words, kb_training_go, kb_training_in_game, kb_rules)
from states.states import FSMtraining
from files.dicts import (dict_dicts, list_right_answers)
from sqlite_db import create_profile, edit_hw_done, check_hw, dict_hw, update_progress, get_progress, \
    update_last_sentence, get_last_sentence

user_router: Router = Router()
main_dict = {}
done_lst = []
flag = False


@user_router.message(F.text == '[Сбросить машину состояний]')
async def training_new(message: Message, state: FSMContext):
    await message.answer('Сброшено!')
    await state.clear()


@user_router.message(F.text == ('Новые слова [В разработке]'))
async def new_words_pass(message: Message):
    await message.answer(
        f'Извини, {message.from_user.full_name}, тренажер для запоминания слов находится в разработке 😊')


@user_router.message(Command(commands=["rules"]))
async def process_start_command(message: Message):
    await message.answer(
        f"""Весь прогресс сохраняется в памяти бота\nРегистр введенных предложений/слов не имеет значения.\nНе используйте сокращения «don't», «it's», используйте полные формы «do not», «it is»\nВ любой непонятной ситуации нажимай команду /start и выбирай чем хочешь заниматься 😊""",
        reply_markup=kb_rules)


# Этот хэндлер будет срабатывать на команду "/start" -
@user_router.message(Command(commands=["start"]), StateFilter(default_state))
@user_router.message(F.text == 'Ок, понятно', StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await create_profile(message.from_user.id, message.from_user.username,
                         message.from_user.full_name)
    with open('log.csv', 'a', encoding='utf-8') as log_file:
        log_data = [
            str(message.from_user.id).ljust(16), str(message.from_user.full_name).ljust(20),
            str(message.from_user.username).ljust(15), str(message.from_user.is_bot).ljust(6),
            time.strftime('%H:%M :: %d/%m/%Y'), time.tzname]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    await message.answer(f"""Привет,{message.from_user.full_name}! Я бот от Оли Прус : )
\nПомогаю людям изучать английский.
Пока что у меня две функции:
– тренажер по грамматике
– запоминание новых слов
\n⬇️ Выбери, с чего начнём сегодня ⬇️""",
                         reply_markup=kb_training_or_new_words)


# Этот хэндлер будет срабатывать на команду "/start" -
@user_router.message(Command(commands=['start']), ~StateFilter(default_state))
@user_router.message(F.text == 'Выход', ~StateFilter(default_state))
@user_router.message(F.text == 'Ок, понятно', ~StateFilter(default_state))
async def process_start_command_patron(message: Message, state: FSMContext):
    global flag
    flag = True
    await message.answer(f"""⬇️ Чем займёмся сегодня? ⬇️""",
                         reply_markup=kb_training_or_new_words)
    await create_profile(message.from_user.id, message.from_user.username,
                         message.from_user.full_name)


@user_router.message(
    (F.text == 'Тренажер по грамматике'),
    StateFilter(default_state))  # Показываем правила тренажера новому пользователю
async def training_new(message: Message, state: FSMContext):
    await message.answer(
        f"""Окей, правила простые: я пишу на русском, ты переводишь на английский.
Если ответы не совпадут, можешь сразу подглядеть ответ или попробовать ещё раз""",
        reply_markup=kb_training_go)
    await state.set_state(FSMtraining.in_process)


# Кнопку нажал пользователь, знающий правила
@user_router.message(F.text == ('Тренажер по грамматике'),
                     ~StateFilter(default_state))
@user_router.message(F.text == ('Ок, начинаем'), ~StateFilter(default_state))
async def training_old(message: Message, state: FSMContext):
    global main_dict, level, word, done_lst, flag
    flag = True
    done_lst = await get_progress(message.from_user.id)  # подгружаем данные по прогрессу из БД
    level = await check_hw(message.from_user.id)  # проверяем уровень из БД
    main_dict = dict_dicts[level]  # ставим нужный словарь
    await message.answer(f"""Ты находишься на уровне {level}\nПереведено {len(done_lst)}\nВсего {len(main_dict)}""",
                         reply_markup=ReplyKeyboardRemove())
    word = random.choice(
        [s for s in list(main_dict.values()) if s not in done_lst])
    await message.answer(f'Переводи следующее:\n{word}')
    await update_last_sentence(message.from_user.id, word)
    await state.set_state(FSMtraining.in_process)


@user_router.message(F.text == 'Покажи ответ',
                     StateFilter(FSMtraining.in_process))
async def show_answer(message: Message, state: FSMContext):
    global word
    inv_dict = {value: key for key, value in main_dict.items()}
    await message.answer(inv_dict[word])
    word = random.choice(
        [s for s in list(main_dict.values()) if s not in done_lst])
    await update_last_sentence(message.from_user.id, word)
    await message.answer(
        f'На ошибках учатся, так что продолжаем 😊\nПереводи следующее:\n{word}', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Переводи следующее:\n{word}', reply_markup=ReplyKeyboardRemove())
    await update_last_sentence(message.from_user.id, word)


@user_router.message(StateFilter(FSMtraining.in_process))
async def check_translation(message: Message, state: FSMContext):
    global word, done_lst, main_dict, level, flag
    done_lst = await get_progress(message.from_user.id)  # подгружаем прогресс из БД

    msg = message.text.lower()
    try:
        if main_dict[msg].lower() == word.lower():
            done_lst.append(word)
            await update_progress(message.from_user.id, done_lst)
            await message.answer(random.choice(list_right_answers))
            if len(done_lst) == len(
                    main_dict
            ):  # Все предложения переведены, переход на следующий уровень
                await message.answer(
                    'Поздравляю! Ты перевел все предложения из этого уровня!')
                await edit_hw_done(message.from_user.id, dict_hw[level]
                                   )  # отправляем в БД инфу, что уровень выполнен
                level = await check_hw(message.from_user.id
                                       )  # загружаем номер невыполненного задания
                done_lst = []  # обнуляем список переведенных предложений
                await update_progress(message.from_user.id
                                      )  # обнуляем список переведенных в БД
                main_dict = dict_dicts[level]  # меняем словарь на новый уровень
                await message.answer(f"""Теперь ты находишься на уровне {level}""")
                word = random.choice(
                    [s for s in list(main_dict.values()) if s not in done_lst])
                await message.answer(f'Переводи следующее:\n{word}')
                await update_last_sentence(message.from_user.id, word)
            else:  # переведены не все предложения, переводим следующее
                word = random.choice([
                    s for s in list(main_dict.values()) if s not in done_lst
                ])  # Выбираем случайное предложение, которое еще не было использовано
                await message.answer(f'Переведи:\n{word}',
                                     reply_markup=ReplyKeyboardRemove())
                await update_last_sentence(message.from_user.id, word)

        else:
            await message.answer(
                '❌ Хм, у меня другой ответ 🤔\nПопробуй ещё раз или попроси меня подсказать ответ 😉',
                reply_markup=kb_training_in_game)
    except KeyError:
        if flag == True:
            await message.answer(
                '❌ Хм, у меня другой ответ 🤔\nПопробуй ещё раз или попроси меня подсказать ответ 😉',
                reply_markup=kb_training_in_game)
        if flag == False:  # если был перезапуск бота и пользователь не совершал никаких действий
            word = await get_last_sentence(message.from_user.id)
            level = await check_hw(message.from_user.id)  # проверяем уровень из БД
            main_dict = dict_dicts[level]  # ставим нужный словарь
            done_lst = await get_progress(message.from_user.id)  # подгружаем прогресс из БД
            try:
                if main_dict[message.text.lower()].lower() == word.lower():
                    done_lst.append(word)
                    await update_progress(message.from_user.id, done_lst)
                    await message.answer(random.choice(list_right_answers))
                    word = random.choice([
                        s for s in list(main_dict.values()) if s not in done_lst
                    ])  # Выбираем случайное предложение, которое еще не было использовано
                    await message.answer(f'Переведи:\n{word}',
                                         reply_markup=ReplyKeyboardRemove())
                    flag = True
            except:
                await message.answer(
                    '❌ Хм, у меня другой ответ 🤔\nПопробуй ещё раз или попроси меня подсказать ответ 😉',
                    reply_markup=kb_training_in_game)


@user_router.message()
async def send_idontknow(message: Message):
    await message.reply(
        f'{message.from_user.first_name}, я всего лишь бот, я не знаю, что на это ответить🤷🏼‍♀'
    )
