import irbis
from environs import Env

async def get_statistics():
    repo_stata = 0
    rdr_stata = 0
    env = Env()
    client = irbis.Connection()
    client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                   f'database={env("IRBIS_REPO_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
    client.connect()
    if not client.connected:
        print('Невозможно подключиться!')
        exit(1)
    else:
        client.connect()

        found = client.search_all('"A=$"')
        repo_stata = len(found)
        client.disconnect()

    client = irbis.Connection()
    client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                   f'database={env("IRBIS_USER_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
    client.connect()
    if not client.connected:
        print('Невозможно подключиться!')
        exit(1)
    else:
        client.connect()

        found = client.search_all('"A=$"')
        rdr_stata = len(found)
        client.disconnect()

    return f'Всего работ: {repo_stata}\nВсего пользователей: {rdr_stata}'