import irbis
from environs import Env


async def check_user_logpass_repo(user_form, user_id):
    # Подключаемся к серверу
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

    found = client.search_all('"A=$"')
    print(f'Найдено записей: {len(found)}')
    user_data = []
    for mfn in found:
        # Получаем запись из базы данных
        record = client.read_record(mfn)
        if record.fm(30) == str(user_form['login']) and record.fm(130) == str(user_form['password']):
            # # Извлекаем из записи интересующее нас поле и подполе
            if not record.fm(33):
                record.add(33, str(user_id))
                # Сохраняем запись обратно на сервер
                client.write_record(record)
                user_lastname = record.fm(10)
                user_name = record.fm(11)
                user_otchestvo = record.fm(12)
                user_data.append(user_lastname)
                user_data.append(user_name)
                user_data.append(user_otchestvo)
            else:
                user_lastname = record.fm(10)
                user_name = record.fm(11)
                user_otchestvo = record.fm(12)
                user_data.append(user_lastname)
                user_data.append(user_name)
                user_data.append(user_otchestvo)
        else:
            continue
    client.disconnect()
    if len(user_data) > 1:
        print(len(user_data))
        return user_data
    else:
        return False
