from datetime import datetime

import irbis
from environs import Env
from datetime import datetime, timedelta
async def get_maxi_statistics(date_nachalo, date_konec):
    repo_stata = []
    print('date_nachalo',date_nachalo)
    print('date_konec', date_konec)
    env = Env()
    client = irbis.Connection()
    client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                   f'database={env("IRBIS_REPO_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
    client.connect()
    if not client.connected:
        print('Невозможно подключиться!')
        exit(1)

    else:
        # Быстрый алгоритм поиска записей
        # info = client.get_database_info(env("IRBIS_REPO_BASE"))
        time_difference = date_konec - date_nachalo
        days_difference = ((time_difference.total_seconds() / 60) / 60) / 24 + 1
        print(days_difference)
        data_all = []
        result_serch = []
        for i in range(int(days_difference)):
            data_all.append(date_nachalo + timedelta(days=i))
        print(data_all)
        for i in data_all:
            found = client.search(f'"DP={datetime.strftime(i, "%Y%m%d")}$"')
            result_serch.extend(found)

        print("result_serch =",result_serch)

        for mfn in result_serch:
            # Получаем запись из базы данных
            # record = client.read_record(mfn)
            #
            # # Извлекаем из записи интересующее нас поле и подполе
            # title = record.fm(200, 'a')
            # print('Заглавие:', title)

            # Форматируем запись средствами сервера
            repo_stata.append(client.format_record(irbis.BRIEF, mfn))
            print('Биб. описание:', client.format_record(irbis.BRIEF, mfn))
            print()  # Добавляем пустую строку
        # Медленный алгоритм поиска записей
        # data_all = []
        # result_serch = []
        # last_mfn = info.max_mfn - 1
        # print(f"Последний mfn: {last_mfn}")
        # print(f"Последний mfn: {type(last_mfn)}")
        #
        # found = client.search('"A=$"')
        # print(f'Найдено записей: {len(found)}')
        # print(found)
        # for mfn in found:
        #     # Получаем запись из базы данных
        #     record = client.read_record(mfn)
        #     date_in_irbis = datetime.strptime(record.fm(907, "a"), "%Y%m%d")
        #     if date_nachalo <= date_in_irbis <=date_konec:
        #         print(f"{record.fm(700, 'a')} {record.fm(700, 'b')}")
        #         #repo_stata.append(f"{record.fm(700, 'a')} {record.fm(700, 'b')}, {record.fm(200, 'a')}, {record.fm(200, 'e')}")
        #         repo_stata.append(client.format_record(irbis.BRIEF, mfn))

        client.disconnect()

    return len(result_serch),repo_stata