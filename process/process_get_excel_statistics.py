from datetime import datetime
import openpyxl
import irbis
from environs import Env
from datetime import datetime, timedelta
async def get_excel_statistics(date_nachalo, date_konec):
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
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["ФИО", "ФИО", "ЗАГЛАВИЕ", "ТИП ПУБЛИКАЦИИ", "ДАТА СОЗДАНИЯ/ПУБЛИКАЦИИ", "АННОТАЦИЯ"])
        for mfn in result_serch:
            # Получаем запись из базы данных
            record = client.read_record(mfn)
            #
            # # Извлекаем из записи интересующее нас поле и подполе
            type_pub = record.fm(200, 'e').split(',')
            t = ''
            date_pub = ''
            if len(type_pub)<3:
               t = type_pub[0]
               date_pub = type_pub[-1].strip()
            else:
                t = ','.join(type_pub[:-1])
                date_pub = type_pub[-1].strip()

            title = [f"{record.fm(700, 'a')} {record.fm(700, 'g')}",record.fm(200, 'f'), record.fm(200, 'a'),t, date_pub, record.fm(331)]
            ws.append(title)
            #print(title)
        wb.save(f'statistics.xlsx')

        client.disconnect()

    return len(result_serch),repo_stata