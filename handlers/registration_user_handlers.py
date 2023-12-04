from aiogram import F, Router

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (CallbackQuery, Message)

from process import register_tg_id_to_server
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import keyboards_start_help

router = Router()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний FSM

class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    login = State()  # Состояние ожидания ввода имени
    password = State()  # Состояние ожидания ввода возраста


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Нажмите /start и вернитесь в начало', reply_markup=keyboards_start_help)


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы отменили ввод данных. Чтобы вернуться в начало нажмите /start', reply_markup=keyboards_start_help)
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Отказ от регистрации
@router.callback_query(F.data == 'cancel_register')
async def process_cancel_register(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Отказ от регистрации')
    await callback.message.answer(
        text=f'Нажмите /start для вызова регистрации',
        reply_markup=keyboards_start_help)


# Этот хэндлер будет срабатывать на fill_register_user
# и переводить бота в состояние ожидания ввода логина
# @router.message(Command(commands='fill_register_user'), StateFilter(default_state))
@router.callback_query(F.data == 'fill_register_user', StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text('Регистрация')
    await callback.message.answer(text='Пожалуйста, введите логин, который получили при регистрации в Репозитории РАО')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.login)


# Этот хэндлер будет срабатывать, если введен логин
@router.message(StateFilter(FSMFillForm.login))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "login"
    await state.update_data(login=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите пароль, который получили при регистрации в Репозитории РАО')
    # Устанавливаем состояние ожидания ввода пароля
    await state.set_state(FSMFillForm.password)


@router.message(StateFilter(FSMFillForm.password))
async def process_password_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "login"
    await state.update_data(password=message.text)

    user_form = await state.get_data()
    user_id = message.from_user.id
    await state.clear()
    reg_data = register_tg_id_to_server.check_user_logpass_repo(user_form, user_id)
    if reg_data:
        s = [i for i in reg_data if i]
        await message.answer(
            text=f'Добро пожаловать, {" ".join(s)}\nРегистрация в Репозитории РАО прошла корректно!\nНажмите /start для продолжения',
            reply_markup=keyboards_start_help)
    else:
        await message.answer(text=LEXICON_RU['unreg'], reply_markup=keyboards_start_help, parse_mode="Markdown")
    # Устанавливаем состояние ожидания ввода возраста
