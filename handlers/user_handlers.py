import asyncio, random, json, csv, time

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from keyboards.keyboards import (kb_main_menu, kb_training_rules_inline, kb_training_or_verbs_or_new_words_inline,
                                 kb_training_in_game_inline, create_inline_kb_words, kb_verbs_rules_inline,
                                 kb_in_verbs_inline, kb_in_verbs_fail_inline)
from states.states import FSMtraining
from files.dicts import (dict_dicts, list_right_answers)
# from files.words import words_dict
from sqlite_db import (create_profile, edit_hw_done, check_hw, dict_hw, update_progress, update_progress_verbs,
                       get_progress, get_progress_verbs, get_or_edit_verbs_level,
                       update_last_sentence, get_last_sentence, update_last_verb, get_last_verb)
from handlers.admin_handlers import send_message_to_admin, bot

user_router: Router = Router()
main_dict = {}
done_lst = []


@user_router.message(F.text == '[Сбросить машину состояний]')
async def training_new(message: Message, state: FSMContext):
    await message.answer('Сброшено!')
    await state.clear()


@user_router.message(Command(commands=["info"]))
async def process_start_command(message: Message):
    await message.answer(
        f"""\n🟢Весь прогресс сохраняется в памяти бота
\n🔵Регистр введенных предложений/слов не имеет значения.
\n❌Не используй сокращения «don't», «it's»
✅Используй полные формы «do not», «it is»
\n🟠В любой непонятной ситуации нажимай команду /start и бот перезапустится 😊""",
        reply_markup=kb_main_menu)


# 🟣🔵🟢🟡🟠🔴🟤

# Этот хэндлер будет срабатывать на команду "/start" при стандартном состоянии
@user_router.message(Command(commands=["start"]), StateFilter(default_state))
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
Пока что у меня три функции:
– тренажер по грамматике
- запоминание неправильных глаголов
– запоминание новых слов
\n🔻️ Выбери, с чего начнём сегодня 🔻""",
                         reply_markup=kb_training_or_verbs_or_new_words_inline)
    await send_message_to_admin(bot,
                                text=f'Зарегистрирован новый пользователь!\n{message.from_user.full_name}\n@{message.from_user.username}')


# Этот хэндлер будет срабатывать на команду "/start" при НЕстандартном состоянии
@user_router.message(Command(commands=['main_menu']), ~StateFilter(default_state))
@user_router.message(Command(commands=['start']), ~StateFilter(default_state))
async def process_start_command_patron(message: Message, state: FSMContext):
    await message.answer(f"""🔻 Чем займёмся сегодня? 🔻""",
                         reply_markup=kb_training_or_verbs_or_new_words_inline)
    await create_profile(message.from_user.id, message.from_user.username,
                         message.from_user.full_name)


@user_router.callback_query(F.data == 'Главное меню', ~StateFilter(default_state))
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"""🔻 Чем займёмся сегодня? 🔻""",
                                     reply_markup=kb_training_or_verbs_or_new_words_inline)


#################################### ТРЕНАЖЕР ПО ГРАММАТИКЕ ####################################
@user_router.callback_query(F.data == 'Тренажер по грамматике')
async def training_grammar(callback: CallbackQuery, state: FSMContext):
    done_lst = await get_progress(callback.from_user.id)  # подгружаем данные по прогрессу из БД
    level = await check_hw(callback.from_user.id)  # проверяем уровень из БД
    main_dict = dict_dicts[level]  # ставим нужный словарь
    await callback.answer()
    await callback.message.edit_text(
        f'Отличный выбор!\nБудем улучшать твою <b>грамматику</b>\nЕсли нужно - жми кнопку ниже и посмотри правила',
        reply_markup=kb_training_rules_inline)
    await callback.message.answer(
        f'Ты находишься на уровне {level}\nПереведено {len(done_lst)}\nВсего {len(main_dict)}',
        reply_markup=ReplyKeyboardRemove())
    sentence = random.choice(
        [s for s in list(main_dict.values()) if s not in done_lst])
    await callback.message.answer(f'Переводи следующее:\n\n{sentence}')
    await update_last_sentence(callback.from_user.id, sentence)
    await state.set_state(FSMtraining.in_process)


@user_router.callback_query(F.data == 'Посмотреть правила тренажера')
async def see_rules_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text='Правила простые:\nЯ пишу на русском, ты переводишь на английский.\n\nЕсли ответы не совпадут:\n⚪ Можешь попробовать написать предложение ещё раз\n⚪ Можешь поcмотреть ответ, нажав на кнопку «Покажи ответ»')


@user_router.callback_query(F.data == 'Показать ответ')
async def show_answer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    sentence = await get_last_sentence(callback.from_user.id)  # подгружаем последнее предложение из БД
    level = await check_hw(callback.from_user.id)  # проверяем уровень из БД
    main_dict = dict_dicts[level]  # ставим нужный словарь
    inv_dict = {value: key for key, value in main_dict.items()}
    await callback.message.edit_text(f'Ответ:\n\n{(inv_dict[sentence]).capitalize()}')
    sentence = random.choice(
        [s for s in list(main_dict.values()) if s not in done_lst])
    await update_last_sentence(callback.from_user.id, sentence)
    await callback.message.answer(
        f'На ошибках учатся, так что продолжаем 😊')
    await callback.message.answer(f'Переводи следующее:\n\n{sentence}')


@user_router.message(StateFilter(FSMtraining.in_process))
async def check_translation(message: Message, state: FSMContext):
    sentence = await get_last_sentence(message.from_user.id)  # подгружаем последнее предложение из БД
    done_lst = await get_progress(message.from_user.id)  # подгружаем прогресс из БД
    level = await check_hw(message.from_user.id)  # проверяем уровень из БД
    main_dict = dict_dicts[level]  # ставим нужный словарь
    if message.text is not None:
        msg = message.text.lower()
    else:
        msg = ''
    try:
        if main_dict[msg].lower() == sentence.lower():  # перевод верный
            done_lst.append(sentence)  # добавляем переведенное предл в список done
            await update_progress(message.from_user.id, done_lst)  # обновляем выполненные в БД
            await message.answer(random.choice(list_right_answers))  # пишем, что пользователь молодец))
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
                sentence = random.choice(
                    [s for s in list(main_dict.values()) if s not in done_lst])
                await message.answer(f'Переводи следующее:\n{sentence}')
                await update_last_sentence(message.from_user.id, sentence)
            else:  # переведены не все предложения, переводим следующее
                sentence = random.choice([
                    s for s in list(main_dict.values()) if s not in done_lst
                ])  # Выбираем случайное предложение, которое еще не было использовано
                await message.answer(f'Переведи:\n{sentence}',
                                     reply_markup=ReplyKeyboardRemove())
                await update_last_sentence(message.from_user.id, sentence)

        else:
            await message.answer('❌ Хм, у меня другой ответ 🤔')
            await message.answer('<u>Попробуй ещё раз</u> или попроси меня показать ответ 😉',
                                 reply_markup=kb_training_in_game_inline)
    except KeyError:
        await message.answer('❌ Хм, у меня другой ответ 🤔')
        await message.answer('<u>Попробуй ещё раз</u> или попроси меня показать ответ 😉',
                             reply_markup=kb_training_in_game_inline)


#################################### ИЗУЧЕНИЕ НЕПРАВИЛЬНЫХ ГЛАГОЛОВ ####################################
@user_router.callback_query(F.data == 'Изучение неправильных глаголов')
async def verbs_start(callback: CallbackQuery, state: FSMContext):
    done_lst_verbs = await get_progress_verbs(callback.from_user.id)  # подгружаем данные по прогрессу из БД
    level = await get_or_edit_verbs_level(callback.from_user.id)  # проверяем уровень из БД
    main_dict = dict_dicts['verbs']  # ставим нужный словарь
    await callback.answer()
    await callback.message.edit_text(
        f'Отличный выбор!\nБудем учить <b>неправильные глаголы</b>\nЕсли нужно - жми кнопку ниже и посмотри правила',
        reply_markup=kb_verbs_rules_inline)
    await callback.message.answer(
        f'Ты находишься на уровне {level}\nВыучено {len(done_lst_verbs)}\nВсего {len(main_dict)}',
        reply_markup=ReplyKeyboardRemove())
    verb = random.choice(
        [s for s in list(main_dict.values()) if s not in done_lst])
    await callback.message.answer(f'Напиши три формы глагола:\n<b>{verb.capitalize()}</b>',
                                  reply_markup=kb_in_verbs_inline)
    await update_last_verb(callback.from_user.id, verb)
    await state.set_state(FSMtraining.in_process_verbs)


@user_router.message(StateFilter(FSMtraining.in_process_verbs))
async def check_translation_verbs(message: Message, state: FSMContext):
    verb = await get_last_verb(message.from_user.id)
    done_lst_verbs = await get_progress_verbs(message.from_user.id)  # подгружаем данные по прогрессу из БД
    level = await get_or_edit_verbs_level(message.from_user.id)  # проверяем уровень из БД
    main_dict = dict_dicts['verbs']  # ставим нужный словарь
    if message.text is not None:
        msg = message.text.lower()
    else:
        msg = ''
    try:
        if main_dict[msg].lower() == verb.lower():  # перевод верный
            done_lst_verbs.append(verb)  # добавляем переведенное предл в список done
            await update_progress_verbs(message.from_user.id, done_lst_verbs)  # обновляем выполненные в БД
            await message.answer(random.choice(list_right_answers))  # пишем, что пользователь молодец))
            if len(done_lst_verbs) == len(main_dict):  # Все изучено, переход на следующий уровень
                await message.answer(f'Поздравляю! Ты выполнил уровень {level}!')
                level = await get_or_edit_verbs_level(message.from_user.id,
                                                      edited=True)  # отправляем в БД инфу, что уровень выполнен
                done_lst_verbs = []  # обнуляем список переведенных предложений
                await update_progress_verbs(message.from_user.id)  # обнуляем список переведенных в БД
                await message.answer(f"""Теперь ты находишься на уровне {level}""")
                verb = random.choice(
                    [s for s in list(main_dict.values()) if s not in done_lst_verbs])
                await message.answer(f'Переводи следующее:\n<b>{verb.capitalize()}</b>',
                                     reply_markup=kb_in_verbs_inline)
                await update_last_verb(message.from_user.id, verb)
            else:  # переведены не все предложения, переводим следующее
                verb = random.choice([
                    s for s in list(main_dict.values()) if s not in done_lst_verbs
                ])  # Выбираем случайное предложение, которое еще не было использовано
                await message.answer(f'Переведи:\n<b>{verb.capitalize()}</b>', reply_markup=kb_in_verbs_inline)
                await update_last_verb(message.from_user.id, verb)

        else:
            await message.answer('❌ Хм, у меня другой ответ 🤔')
            await message.answer('<u>Попробуй ещё раз</u> или попроси меня показать ответ 😉',
                                 reply_markup=kb_in_verbs_fail_inline)
    except KeyError:
        await message.answer('❌ Хм, у меня другой ответ 🤔')
        await message.answer('<u>Попробуй ещё раз</u> или попроси меня показать ответ 😉',
                             reply_markup=kb_in_verbs_fail_inline)


@user_router.callback_query(F.data == 'Показать глагол')
async def show_answer_verbs(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    done_lst_verbs = await get_progress_verbs(callback.from_user.id)  # подгружаем данные по прогрессу из БД
    verb = await get_last_verb(callback.from_user.id)  # подгружаем последний глагол из БД
    main_dict = dict_dicts['verbs']  # ставим нужный словарь
    inv_dict = {value: key for key, value in main_dict.items()}
    await callback.message.edit_text(f'Ответ:\n\n{(inv_dict[verb]).capitalize()}')
    verb = random.choice(
        [s for s in list(main_dict.values()) if s not in done_lst_verbs])
    await update_last_verb(callback.from_user.id, verb)
    await callback.message.answer('Продолжаем 😊')
    await callback.message.answer(f'Переводи следующее:\n<b>{verb.capitalize()}</b>', reply_markup=kb_in_verbs_inline)


@user_router.callback_query(F.data == 'Показать глагол при ошибке')
async def show_answer_verbs(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    done_lst_verbs = await get_progress_verbs(callback.from_user.id)  # подгружаем данные по прогрессу из БД
    verb = await get_last_verb(callback.from_user.id)  # подгружаем последний глагол из БД
    main_dict = dict_dicts['verbs']  # ставим нужный словарь
    inv_dict = {value: key for key, value in main_dict.items()}
    await callback.message.edit_text(f'Ответ:\n\n{(inv_dict[verb]).capitalize()}')
    verb = random.choice(
        [s for s in list(main_dict.values()) if s not in done_lst_verbs])
    await update_last_verb(callback.from_user.id, verb)
    await callback.message.answer(
        f'На ошибках учатся, так что продолжаем 😊')
    await callback.message.answer(f'Переводи следующее:\n<b>{verb.capitalize()}</b>', reply_markup=kb_in_verbs_inline)


@user_router.callback_query(F.data == 'Посмотреть правила глаголы')
async def see_rules_verbs(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text='''Правила следующие:\nЯ пишу на русском, ты пишешь три формы глагола на английском через пробел.
Если у формы глагола есть два варианта написания, то пиши через slash(/).\nНапример:
<b>take took taken</b>
<b>be was/were been</b>\n<b>spell spelt/spelled spelt/spelled</b>\n\nЕсли ответы не совпадут:
⚪ Можешь попробовать написать ответ ещё раз\n⚪ Можешь поcмотреть правильный ответ, нажав на кнопку «Покажи ответ»''')


#################################### ИЗУЧЕНИЕ НОВЫХ СЛОВ ####################################
@user_router.callback_query(F.data == 'Новые слова')
@user_router.callback_query(F.data == 'Понятно')
async def new_words_main_menu(callback: CallbackQuery, state: FSMContext):
    DICT = {str(key): str(key) for key, value in words_dict.items()}
    await state.set_state(FSMtraining.in_process_new_words)
    await callback.message.edit_text('Выбери группу слов, которую хочешь изучать',
                                     reply_markup=create_inline_kb_words(2, True, True, last_btn='Главное меню',
                                                                         **DICT))


@user_router.message(StateFilter(FSMtraining.in_process_new_words))
async def new_words_main_menu_in_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text()


@user_router.callback_query(F.data == 'Посмотреть правила слова')
async def see_rules_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text=f"""Я использую систему интервальных повторений
\n⚪ Слова, которые ты часто переводишь правильно, я буду показывать с каждым днём всё реже и реже
\n⚪ Слова, которые будут запоминаться тяжело, я буду показывать до тех пор, пока ты их не запомнишь""",
        reply_markup=create_inline_kb_words(1, Понятно='Понятно'))


@user_router.message()
async def send_idontknow(message: Message):
    await message.reply(
        f'{message.from_user.first_name}, я всего лишь бот, я не знаю, что на это ответить🤷🏼‍♀'
    )
