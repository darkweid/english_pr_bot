from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import State, StatesGroup


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMtraining(StatesGroup):
    ####### Создаем экземпляры класса State, перечисляя возможные состояния, в которых будет находиться бот #######
    patron_user = State()  # Старый пользователь
    in_process = State()  # проходит тренажер ДЗ
    in_process_verbs = State() # проходит изучение третьей формы глаголов
    in_process_new_words = State()  # проходит изучение слов


class FSMadmin(StatesGroup):
    admin = State()  # в админке
    see_progress_hw = State()
    seeing_progress_hw = State()

    edit_hw = State()
    edit_hw_got_user_id = State()
    edit_hw_got_user_id_and_hw_number = State()
    progress_words = State()
