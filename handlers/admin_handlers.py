from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
#from keyboards.kb_utils import create_inline_kb, create_reply_kb
#from lexicon.lexicon import LEXICON
#from states.states import FSMStartQuest, FSMEngineeringCompartment
admin_router: Router = Router()