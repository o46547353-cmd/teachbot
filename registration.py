from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class RegistrationFSM(StatesGroup):
    age_group = State()
    english_level = State()
    universe = State()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Kids (7-11)"), KeyboardButton(text="Teens (12-17)")],
        [KeyboardButton(text="Adults (18+)")]
    ], resize_keyboard=True)
    await message.answer("Привет! Выбери свою возрастную группу:", reply_markup=kb)
    await state.set_state(RegistrationFSM.age_group)

@router.message(RegistrationFSM.age_group)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age_group=message.text)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="A1"), KeyboardButton(text="A2"), KeyboardButton(text="B1")],
        [KeyboardButton(text="B2"), KeyboardButton(text="C1")]
    ], resize_keyboard=True)
    await message.answer("Супер! Какой у тебя уровень английского?", reply_markup=kb)
    await state.set_state(RegistrationFSM.english_level)

@router.message(RegistrationFSM.english_level)
async def process_level(message: Message, state: FSMContext):
    await state.update_data(english_level=message.text)
    # Здесь в реальном проекте мы тянем вселенные из БД в зависимости от возраста и уровня
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Гарри Поттер"), KeyboardButton(text="Marvel")],
        [KeyboardButton(text="Cyberpunk 2077")]
    ], resize_keyboard=True)
    await message.answer("Выбери вселенную для своего квеста:", reply_markup=kb)
    await state.set_state(RegistrationFSM.universe)

@router.message(RegistrationFSM.universe)
async def process_universe(message: Message, state: FSMContext):
    await state.update_data(universe=message.text)
    user_data = await state.get_data()
    
    # Здесь логика сохранения в БД (SQLAlchemy)
    
    await message.answer(
        f"Профиль создан! Ты в категории {user_data['age_group']}, уровень {user_data['english_level']}. "
        f"Добро пожаловать во вселенную {user_data['universe']}! Готов к первому заданию?", 
        reply_markup=None
    )
    await state.clear()