import irbis
from aiogram import F, Router, types
from environs import Env
from aiogram.types import (CallbackQuery, Message)
from random import *

import process.process_send_email

router = Router()


@router.callback_query()
async def callback_unreg_users(callback: CallbackQuery):
    env = Env()
    if callback.data[:9] == '!_ye_add_':
        all_data_in_mfn = {}
        client = irbis.Connection()
        client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                       f'database={env("IRBIS_RDRV_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
        client.connect()
        if not client.connected:
            print('Невозможно подключиться!')
            exit(1)
        else:
            print(client)
        record = client.read_record(int(callback.data[10:]))
        if check_email(record.fm(32)):
            all_data_in_mfn.setdefault(10, record.fm(10))
            all_data_in_mfn.setdefault(11, record.fm(11))
            if record.fm(12) != None:
                all_data_in_mfn.setdefault(12, record.fm(12))
            if record.fm(16) != None:
                all_data_in_mfn.setdefault(16, record.fm(16))
            all_data_in_mfn.setdefault(23, record.fm(23))
            all_data_in_mfn.setdefault(18, record.fm(18))
            all_data_in_mfn.setdefault(32, record.fm(32))
            all_data_in_mfn.setdefault(51, record.fm(51))
            login = all_data_in_mfn[32][:all_data_in_mfn[32].index("@")]

            found_login = client.search_all(f'"K={login}$"')

            if len(found_login) >0:
                await callback.message.edit_reply_markup()
                await callback.message.edit_text(
                    text=f"{callback.message.text}\nПользователь с таким Логином существует, необходимо проверить данную запись вручную")
                client.disconnect()
            else:
                all_data_in_mfn.setdefault(30, login)
                record.add(30, login)
                password = generate_password()
                record.add(130, password)
                all_data_in_mfn.setdefault(130, password)
                # Сохраняем запись обратно на сервер
                client.write_record(record)
                client.disconnect()
                send_user_to_rdr(all_data_in_mfn)
                await process.process_send_email.send_email_ok(all_data_in_mfn)
                await callback.message.edit_reply_markup()
                await callback.message.edit_text(text=f"{callback.message.text} Добавлен")
        else:
            await callback.message.edit_reply_markup()
            client.delete_record(int(callback.data[10:]))  # Удаляем запись
            await callback.message.edit_text(
                text=f"{callback.message.text}\nНе правильно указана электронная почта, запись удална")
            client.disconnect()

    if callback.data[:9] == '!_no_add_':
        all_data_in_mfn = {}
        client = irbis.Connection()
        client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                       f'database={env("IRBIS_RDRV_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
        client.connect()
        if not client.connected:
            print('Невозможно подключиться!')
            exit(1)
        else:
            print(client)
        record = client.read_record(int(callback.data[10:]))
        if check_email(record.fm(32)):
            all_data_in_mfn.setdefault(10, record.fm(10))
            all_data_in_mfn.setdefault(11, record.fm(11))
            all_data_in_mfn.setdefault(23, record.fm(23))
            all_data_in_mfn.setdefault(18, record.fm(18))
            all_data_in_mfn.setdefault(32, record.fm(32))
            client.delete_record(int(callback.data[10:]))  # Удаляем запись
            await process.process_send_email.send_email_no_ok(all_data_in_mfn)
            await callback.message.edit_reply_markup()
            await callback.message.edit_text(text=f"{callback.message.text} удален")
            client.disconnect()
        else:
            await callback.message.edit_reply_markup()
            client.delete_record(int(callback.data[10:]))  # Удаляем запись
            await callback.message.edit_text(
                text=f"{callback.message.text}\nНе правильно указана электронная почта, запись удална")
            client.disconnect()
def check_email(mail):
    try:
        if mail.index('@') > -1 and mail[mail.index('@'):].index('.'):
            return True
        else:
            return False
    except:
        return False


def generate_password():
    passwd = ''
    for _ in range(7):
        passwd = passwd + chr(choice([randint(65, 90), randint(97, 122), randint(48, 57)]))
    return passwd


def send_user_to_rdr(users):
    env = Env()
    client = irbis.Connection()
    client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                   f'database={env("IRBIS_USER_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
    client.connect()
    if not client.connected:
        print('Невозможно подключиться!')
        exit(1)
    else:
        print(client)
    record = irbis.Record()
    record.add(10, users[10])
    record.add(11, users[11])
    try:
        record.add(12, users[12])
    except:
        pass
    try:
        record.add(16, users[16])
    except:
        pass
    record.add(23, users[23])
    record.add(18, users[18])
    record.add(32, users[32])
    record.add(51, users[51])
    record.add(30, users[30])
    record.add(130, users[130])
    client.write_record(record)
    client.disconnect()
