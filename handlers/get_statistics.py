import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram_calendar import SimpleCalendarCallback, SimpleCalendar, get_user_locale

import bot
from aiogram import F, Router, types
import process
from process import process_get_maxi_statistics
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (CallbackQuery, Message)
import os
from aiogram.types.input_file import FSInputFile
from environs import Env
from process import check_fsm_data, process_add_to_irbis_repo
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import keyboards_start_help, keyboards_type_pub, keyboards_yes_no, keyboards_send_yes_no, \
    public_types_list, keyboards_date_nachalo
import io

from aiogram.types import InputFile



router = Router()
env = Env()
class FSMGetMaxStatisticsForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    date_nachalo = State()
    date_konec = State()

@router.callback_query(F.data == '!_get_mini_stat_!')
async def process_add_to_repo(callback: CallbackQuery):
    keyboard_to_delete = types.ReplyKeyboardRemove()  # удаляем кнопки Replykeyboard
    stata = await process.process_get_statistics.get_statistics()
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(text=stata)

@router.callback_query(F.data == '!_get_maxi_stat_!', StateFilter(default_state))
async def process_add_to_repo(callback: CallbackQuery, state: FSMContext):
    keyboard_to_delete = types.ReplyKeyboardRemove()  # Удаление Репли кнопок
    await callback.message.edit_text(text='Статистика за период\nДля отмены воспользуйтесь командой /cancel')
    # Устанавливаем состояние ожидания ввода имени
    #await callback.answer()
    await callback.message.edit_text("Выберите дату на начало периода\n❗По порядку - год, месяц, день❗\nДля отмены воспользуйтесь командой /cancel", reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(FSMGetMaxStatisticsForm.date_nachalo)



@router.callback_query(SimpleCalendarCallback.filter(), StateFilter(FSMGetMaxStatisticsForm.date_nachalo))
async def process_simple_calendar_nachalo(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    print(callback_query.data)
    print(type(callback_query.data))

    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    # calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date_nachalo=date)
        print(date)
        await callback_query.message.edit_text(
            f'Дата на начало периода: {date.strftime("%d.%m.%Y")}')
        await state.set_state(FSMGetMaxStatisticsForm.date_konec)
        await callback_query.message.answer(
            f'Отлично! Теперь выберем дату на конец периода\n❗По порядку - год, месяц, день❗\nДля отмены воспользуйтесь командой /cancel', reply_markup=await SimpleCalendar().start_calendar())

@router.callback_query(SimpleCalendarCallback.filter(), StateFilter(FSMGetMaxStatisticsForm.date_konec))
async def process_simple_calendar_konec(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    # calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date_konec=date)
        await callback_query.message.edit_text(
            f'Дата на конец периода: {date.strftime("%d.%m.%Y")}')

        print(await state.get_data())
        stast_data = await state.get_data()
        await callback_query.message.edit_text(text='Идет просчет... Ждите.')
        count, stata = await process_get_maxi_statistics.get_maxi_statistics(stast_data['date_nachalo'], stast_data['date_konec'])

        await callback_query.message.edit_text(text=f"Дата на конец периода: {date.strftime('%d.%m.%Y')}")

        with open('statistics.txt', 'w', encoding='utf-8') as file:
            file.write(f"{datetime.datetime.strftime(stast_data['date_nachalo'], '%d.%m.%Y')} - {datetime.datetime.strftime(stast_data['date_konec'], '%d.%m.%Y')}\n")
            file.write(f"Количество записей =  {count}\n")

            for i in stata:
                file.write(f'{i}\n')
        document = FSInputFile('statistics.txt')
        await bot.bot.send_document(env("GROUP_TG_ADMINS"), document)


        await state.clear()