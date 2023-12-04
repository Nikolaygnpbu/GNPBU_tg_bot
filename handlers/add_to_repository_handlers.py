import bot
from aiogram import F, Router, types

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (CallbackQuery, Message)
import os

from process import check_fsm_data, process_add_to_irbis_repo
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import keyboards_start_help, keyboards_type_pub, keyboards_yes_no, keyboards_send_yes_no, \
    public_types_list

router = Router()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM

class FSMAddToRepoForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    get_pdf = State()
    author = State()
    author_question = State()  # Состояние ожидания ввода имени
    authors = State()
    zaglavie = State()  # Состояние ожидания ввода возраста
    typ_pub = State()
    year = State()
    annotation = State()
    keywords = State()
    abstract = State()
    keywords_en_question = State()
    keywords_en = State()
    keywords_en_answere = State()
    # check_add_user_data = State()
    end_qestion = State()

    all_data = {}


@router.callback_query(F.data == '!_add_new_data_!', StateFilter(default_state))
async def process_add_to_repo(callback: CallbackQuery, state: FSMContext):
    keyboard_to_delete = types.ReplyKeyboardRemove()  # Удаление Репли кнопок
    await callback.message.answer(text='Прикрепите файл в формате pdf\n\n❗❗❗ Размер не должен превышать 20Мб.❗❗❗\n'
                                       'Если файл весит более 20Мб, заполните шаблон с сайта rid.gnpbu.ru и отправьте '
                                       'на почту repository@gnpbu.ru вместе с файлом pdf',
                                  reply_markup=keyboard_to_delete)
    # Устанавливаем состояние ожидания ввода имени
    await callback.answer()
    await state.set_state(FSMAddToRepoForm.get_pdf)


@router.message(F.document, StateFilter(FSMAddToRepoForm.get_pdf))
async def process_pdf_sent(message: Message, state: FSMContext):
    if message.document.mime_type == 'application/pdf':
        if message.document.file_size <= 20971520:
            file_id = message.document.file_id
            file = await bot.bot.get_file(file_id)
            file_name = message.document.file_name
            file_path = file.file_path
            await bot.bot.download_file(file_path, file_name)
            print(message.document.file_size)
            await state.update_data(get_pdf=message.document.file_name)  # Сохраняем только имя файла
            await message.answer(text=f'Спасибо!\nФайл "{file_name}" принят.\n\n'
                                      f'Введите ФИО автора\n\nв формате - Фамилия Имя Отчество\n\n'
                                      f'Инициалы не принимаются\n\nКоманда /cancel для остановки процесса ввода данных')
            await state.set_state(FSMAddToRepoForm.author)
        else:
            await message.answer(
                text=f'Файл "{message.document.file_name}" имеет размер больше 20Мб.\n'
                     f'Попробуйте уменьшить размер файла или отправьте файл с описанием на почту repository@gnpbu.ru\n'
                     f'Шаблон можно скачать на rid.gnpbu.ru\n\n'
                     f'Прикрепите файл размером до 20Мб или отмените процесс /cancel\n'
                     f'👇 Menu ->  Остановка процесса добавления данных')
    else:
        await message.answer(
            text=f'Файл "{message.document.file_name}" имеет другой формат\nПрикрепите файл в формате pdf')
    print(await state.get_data())


@router.message(StateFilter(FSMAddToRepoForm.author))
async def process_author1_sent(message: Message, state: FSMContext):
    try:
        if await check_fsm_data.check_author(message.text):
            await state.update_data(author=message.text)
            await message.answer(text='Спасибо!\n\nДобавить еще автора или авторов?', reply_markup=keyboards_yes_no)
            # Устанавливаем состояние ожидания ввода возраста
            await state.set_state(FSMAddToRepoForm.author_question)
        else:
            await message.answer(text='То, что вы отправили не похоже на ФИО')
    except:
        await message.answer(text='То, что вы отправили не похоже на ФИО')

    print(await state.get_data())


@router.message(StateFilter(FSMAddToRepoForm.author_question))
# Отлавливаем yes
@router.callback_query(F.data == '!_yes_!', StateFilter(FSMAddToRepoForm.author_question))
async def process_author_question_command_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(text='Спасибо!\n\nА теперь введите авторов через запятую')
    await state.set_state(FSMAddToRepoForm.authors)


# Если no то прыгаем в keywords_en
@router.callback_query(F.data == '!_no_!', StateFilter(FSMAddToRepoForm.author_question))
async def process_author_question_command_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(text='Спасибо!\n\nВведите заглавие')
    await state.set_state(FSMAddToRepoForm.zaglavie)


@router.message(StateFilter(FSMAddToRepoForm.authors))
async def process_author_many_sent(message: Message, state: FSMContext):
    try:
        if await check_fsm_data.check_authors(message.text):
            await state.update_data(authors=message.text)
            await message.answer(text='Спасибо!\n\nВведите заглавие!')
            await state.set_state(FSMAddToRepoForm.zaglavie)
        else:
            await message.answer(text='То, что вы отправили не похоже на список ФИО')
    except:
        await message.answer(text='То, что вы отправили не похоже на список ФИО')
    print(await state.get_data())


@router.message(StateFilter(FSMAddToRepoForm.author))
async def warning_not_author(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на ФИО')


@router.message(StateFilter(FSMAddToRepoForm.zaglavie))
async def process_zaglavie_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "zaglavie"
    await state.update_data(zaglavie=message.text)
    await message.answer(text='Спасибо!\n\nВыберите тип публикации', reply_markup=keyboards_type_pub)
    await state.set_state(FSMAddToRepoForm.typ_pub)
    print(await state.get_data())


@router.callback_query(StateFilter(FSMAddToRepoForm.typ_pub))
async def process_type_pub_sent(callback: CallbackQuery, state: FSMContext):
    await state.update_data(typ_pub=callback.data)
    await callback.message.delete()
    await callback.message.answer(text='Спасибо!\n\nА теперь введите дату публикации в формате ДД.ММ.ГГГГ')
    await state.set_state(FSMAddToRepoForm.year)
    print(await state.get_data())


@router.message(StateFilter(FSMAddToRepoForm.year))
async def process_year_sent(message: Message, state: FSMContext):
    if await check_fsm_data.check_year(message.text):
        await state.update_data(year=message.text)
        await message.answer(text='Спасибо!\n\nВведите аннотацию')
        # Устанавливаем состояние ожидания ввода типа публикации
        await state.set_state(FSMAddToRepoForm.annotation)
    else:
        await message.answer(text='Введите дату корректно\nПример: 17.11.2023')
    print(await state.get_data())


# Если не правильно ввели год
@router.message(StateFilter(FSMAddToRepoForm.year))
async def warning_year_sent(message: Message):
    await message.answer(text='Не похоже на год издания.\nВведите год издания')


@router.message(StateFilter(FSMAddToRepoForm.annotation))
async def process_annotation_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "annotation"
    await state.update_data(annotation=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ключевые слова, разделенные запятой')
    await state.set_state(FSMAddToRepoForm.keywords)
    print(await state.get_data())


@router.message(StateFilter(FSMAddToRepoForm.keywords))
async def process_abstract_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "keywords"
    await state.update_data(keywords=message.text)
    await message.answer(text='Спасибо!\n\nПланируете указать аннотацию на иностранном языке? (Abstract)',
                         reply_markup=keyboards_yes_no)
    # Устанавливаем состояние ожидания ввода типа публикации
    await state.set_state(FSMAddToRepoForm.abstract)
    print(await state.get_data())


# Отлавливае yes
@router.callback_query(F.data == '!_yes_!', StateFilter(FSMAddToRepoForm.abstract))
async def process_abstract_command_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(text='Спасибо!\n\nА теперь введите аннотацию на иностранном языке')
    await state.set_state(FSMAddToRepoForm.keywords_en_question)


# Если no то прыгаем в keywords_en
@router.callback_query(F.data == '!_no_!', StateFilter(FSMAddToRepoForm.abstract))
async def process_abstract_command_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(text='Спасибо!\n\nПланируете указать ключевые слова на иностранном языке?! ',
                                     reply_markup=keyboards_yes_no)
    await state.set_state(FSMAddToRepoForm.keywords_en)


@router.message(StateFilter(FSMAddToRepoForm.keywords_en_question))
async def process_keywords_en_sent(message: Message, state: FSMContext):
    await state.update_data(abstract=message.text)
    await message.answer(text='Спасибо!\n\nПланируете указать ключевые слова на иностранном языке??',
                         reply_markup=keyboards_yes_no)
    await state.set_state(FSMAddToRepoForm.keywords_en)
    print(await state.get_data())


# Отлавливае yes
@router.callback_query(F.data == '!_yes_!', StateFilter(FSMAddToRepoForm.keywords_en))
async def process_keywords_en_command_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(text='Спасибо!\n\nВведите ключевые слова на иностранном языке')
    await state.set_state(FSMAddToRepoForm.keywords_en_answere)


# Если no то прыгаем в pdf
@router.callback_query(F.data == '!_no_!', StateFilter(FSMAddToRepoForm.keywords_en))
async def process_keywords_en_command_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    all_data = await state.get_data()
    await callback.message.edit_text(text=f'Спасибо!\n\nПроверьте введенные данные\n'
                                          f'Автор - {all_data["author"]}\n'
                                          f'Еще авторы - {await check_fsm_data.check_print_authors(all_data)}\n'
                                          f'Заглавие - {all_data["zaglavie"]}\n'
                                          f'Тип публикации - {public_types_list[int(all_data["typ_pub"])]}\n'
                                          f'Год издания - {all_data["year"]}\n'
                                          f'Аннотация - {all_data["annotation"]}\n'
                                          f'Ключевые слова - {all_data["keywords"]}\n'
                                          f'ABSTRACT - {await check_fsm_data.check_print_abstract(all_data)}\n'
                                          f'KEYWORDS - {await check_fsm_data.check_print_keywords_en(all_data)}\n'
                                          f'Название файла - {all_data["get_pdf"]}'
                                          f'\n\n'
                                          f'Отправить?', reply_markup=keyboards_send_yes_no)
    await state.set_state(FSMAddToRepoForm.end_qestion)


@router.message(StateFilter(FSMAddToRepoForm.keywords_en_answere))
async def process_keywords_en_sent(message: Message, state: FSMContext):
    await state.update_data(keywords_en=message.text)
    all_data = await state.get_data()
    await message.answer(text=f'Спасибо!\n\nПроверьте введенные данные\n'
                              f'Автор - {all_data["author"]}\n'
                              f'Еще авторы - {await check_fsm_data.check_print_authors(all_data)}\n'
                              f'Заглавие - {all_data["zaglavie"]}\n'
                              f'Тип публикации - {public_types_list[int(all_data["typ_pub"])]}\n'
                              f'Год издания - {all_data["year"]}\n'
                              f'Аннотация - {all_data["annotation"]}\n'
                              f'Ключевые слова - {all_data["keywords"]}\n'
                              f'ABSTRACT - {await check_fsm_data.check_print_abstract(all_data)}\n'
                              f'KEYWORDS - {await check_fsm_data.check_print_keywords_en(all_data)}\n'
                              f'Название файла - {all_data["get_pdf"]}'
                              f'\n\n'
                              f'Отправить?', reply_markup=keyboards_send_yes_no)
    await state.set_state(FSMAddToRepoForm.end_qestion)



# Отлавливае yes
@router.callback_query(F.data == '!_send_!', StateFilter(FSMAddToRepoForm.end_qestion))
async def process_keywords_en_command_yes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    try:
        send_data = await state.get_data()
        data_returned = await process_add_to_irbis_repo.record_to_repo(send_data)
        await callback.message.answer(text=f'{data_returned}')
        print('send_data = ', send_data)
    except:
        await callback.message.answer(text='Что-то пошло не так. Сообщите об ошибке на почту repository@gnpbu.ru')

    await callback.message.edit_text(text='Спасибо!\nОтправленно в Репозиторий РАО')
    await state.clear()
    await callback.message.answer(text=LEXICON_RU['end_add_to_repo'], reply_markup=keyboards_start_help)


# Если no то прыгаем в pdf
@router.callback_query(F.data == '!_no_send_!', StateFilter(FSMAddToRepoForm.end_qestion))
async def process_keywords_en_command_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    try:
        send_data = await state.get_data()
        os.remove(send_data['get_pdf'])
        await callback.message.edit_text(text=f'Файл "{send_data["get_pdf"]}" удален из буфера')
    except:
        pass
    # await callback.message.answer(keywords_en=callback.message.text)
    await callback.message.edit_text(
        text='Спасибо!\n\nНажмите кнопку "Добавить новую запись 📙", чтобы внести данные Репозиторий РАО')
    await state.clear()
    await callback.message.answer(text=LEXICON_RU['end_add_to_repo'], reply_markup=keyboards_start_help)
