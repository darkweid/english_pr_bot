from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import State, StatesGroup



# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMtraining(StatesGroup):
####### Создаем экземпляры класса State, перечисляя возможные состояния, в которых будет находиться бот #######
    patron_user = State()               # Старый пользователь
    in_process = State()
    in_process_lvl_1 = State()          #Проходит уровень 1 тренажера
    in_process_lvl_2 = State()          #Проходит уровень 2 тренажера
    in_process_lvl_3 = State()          #Проходит уровень 3 тренажера
class FSMwords(StatesGroup):
####### Создаем экземпляры класса State, перечисляя возможные состояния, в которых будет находиться бот #######
    fill_name = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_gender = State()      # Состояние ожидания выбора пола
    upload_photo = State()     # Состояние ожидания загрузки фото
    fill_education = State()   # Состояние ожидания выбора образования
    fill_wish_news = State()   # Состояние ожидания выбора получать ли новости

FSMdict = {1:FSMtraining.in_process_lvl_1, 2:FSMtraining.in_process_lvl_2, 1:FSMtraining.in_process_lvl_3}