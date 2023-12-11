from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import bot
import irbis
from environs import Env

async def serch_new_users():

    env = Env()
    client = irbis.Connection()
    client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                   f'database={env("IRBIS_RDRV_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
    client.connect()

    found = client.search_all('"A=$"')
    print(f'Найдено записей: {len(found)}')
    user_data = []
    unreg_users_dicts_list = []
    for mfn in found:
        unreg_users_dict = []
        # Получаем запись из базы данных
        record = client.read_record(mfn)
        if record.fm((30))==None:
            unreg_users_dict.append(record.fm(10))
            unreg_users_dict.append(record.fm(11))
            if record.fm(12) != None:
                unreg_users_dict.append(record.fm(12))
            unreg_users_dict.append(record.fm(32))
            unreg_users_dict.append(mfn)
            unreg_users_dicts_list.append(unreg_users_dict)

    client.disconnect()
    await send_message_to_admins_group(unreg_users_dicts_list)

async def send_message_to_admins_group(unreg_users):
    env = Env()
    print(unreg_users)
    if unreg_users:
        print()
        for i in unreg_users:
            print(i)
            button_add_user = InlineKeyboardButton(
                text='Добавить',
                callback_data=f'!_ye_add_!{i[-1]}'
            )
            button_no_add_user = InlineKeyboardButton(
                text='Отклонить',
                callback_data=f'!_no_add_!{i[-1]}'
            )
            keyboards_add_no_user = InlineKeyboardMarkup(inline_keyboard=[[button_add_user, button_no_add_user]])
            await bot.bot.send_message(env("GROUP_TG_ADMINS"), text=f"{', '.join(i[:-1])}",reply_markup=keyboards_add_no_user)

