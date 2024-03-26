from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import aiogram_calendar
import process.process_get_statistics
from process import check_user
from keyboards.keyboards import keyboard_to_reg, keyboards_start_help, keyboard_add_new_data, keyboards_statistics

from lexicon.lexicon_ru import LEXICON_RU
from aiogram_calendar import DialogCalendar, SimpleCalendar, DialogCalendarCallback, get_user_locale, \
    SimpleCalendarCallback

router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    keyboard_to_delete = types.ReplyKeyboardRemove()  # Удаление Репли кнопок
    if await check_user.check_user_repo(user_id):
        await message.answer(text=LEXICON_RU['reg'], reply_markup=keyboard_add_new_data)
    else:
        await message.answer(text=LEXICON_RU['go_reg'], reply_markup=keyboard_to_delete)
        await message.answer(text='Пройти регистрацию?', reply_markup=keyboard_to_reg)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=keyboards_start_help, parse_mode="Markdown")

# Этот хэндлер срабатывает на команду /statistics
@router.message(Command(commands='statistics'))
async def process_help_command(message: Message):
    keyboard_to_delete = types.ReplyKeyboardRemove() # удаляем кнопки Replykeyboard
    await message.answer(text='Статистика', reply_markup=keyboard_to_delete)
    await message.answer(text='Получить статистику', reply_markup=keyboards_statistics)

    #stata = await process.process_get_statistics.get_statistics()

    #await message.answer("Выбери дату начиная с года: ", reply_markup=await SimpleCalendar().start_calendar())
    #await message.answer(text=stata, reply_markup=keyboard_to_delete)

