import irbis
from environs import Env


async def check_user_repo(id):
    env = Env()
    # Подключаемся к серверу
    client = irbis.Connection()
    client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                   f'database={env("IRBIS_USER_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
    client.connect()

    if not client.connected:
        print('Невозможно подключиться!')
        exit(1)
    else:
        print(client)
    print('id = ', id)
    user_data = []
    # found = client.search_all('"A=$"')
    found = client.search_all(f'"U={id}"')
    print(f'Найдено записей: {len(found)}')
    try:  # Если нашелся id
        record = client.read_record(found[0])
        if record.fm(33) == str(id):
            user_id = record.fm(33)
            print(user_id)
            user_lastname = record.fm(10)
            user_name = record.fm(11)
            user_otchestvo = record.fm(12)
            print('user_id_:', user_id, user_lastname, user_name, user_otchestvo)
            #user_data.append(user_id)
            user_data.append(user_lastname)
            user_data.append(user_name)
            user_data.append(user_otchestvo)

        else:
            client.disconnect()
            return False
    except:
        client.disconnect()
        return False
    client.disconnect()
    if len(user_data) > 1:
        print("len(user_data)", len(user_data))
        return user_data
    else:
        return False
