import irbis
import time

from environs import Env

from process import check_process_add_to_repo
from process import send_pdf
from keyboards import keyboards

SF = irbis.SubField  # для краткости


async def record_to_repo(all_data) -> str:
    # Подключаемся к серверу
    env = Env()
    client = irbis.Connection()
    client.parse_connection_string(f'host={env("IRBIS_SERVER_HOST")};port={env("IRBIS_SERVER_PORT")};' +
                                   f'database={env("IRBIS_REPO_BASE")};user={env("IRBIS_SERVER_USER")};password={env("IRBIS_SERVER_PASSWORD")};')
    client.connect()
    if not client.connected:
        print('Невозможно подключиться!')
        exit(1)
    else:
        pole_955 = await send_pdf.process_send_pdf(all_data['get_pdf'])  #
        # Создаём запись и наполняем её полями
        record = irbis.Record()
        fio = await check_process_add_to_repo.check_fio_author(all_data['author'])
        try:  # Ес есть вторые вообще авторы, хоть одит
            fio_authors = await check_process_add_to_repo.check_fio_authors(
                all_data['authors'])  # Получаем список словарей ФИО Авторов
            print('fio_authors =', fio_authors)
            fio_authors_for_200 = await check_process_add_to_repo.create_authors_string_pole_200(fio_authors)
            print('fio_authors_for_200 =', fio_authors_for_200)
            if fio_authors_for_200[0]:
                try:  # если есть отчество у главного автора
                    glav_author_try = f'{fio["i"][0]}. {fio["o"][0]}. {fio["f"]}'  # Не удалять вынесен отдельно, чтобы если У главного автора нет отчества, процесс валился сразу, иначе поля все равно добавляются
                    record.add(200) \
                        .add('A', all_data['zaglavie']) \
                        .add('E', f'{keyboards.public_types_list[int(all_data["typ_pub"])]}, {all_data["year"]}') \
                        .add('F', f'{glav_author_try}, {fio_authors_for_200[1]}')
                    for author_ in fio_authors:
                        if len(author_) == 3:  # Если длинна =3 то значит есть отчество
                            otchestvo = author_['o']
                            record.add(701) \
                                .add('A', author_['f']) \
                                .add('B', f"{author_['i'][0]}. {author_['o'][0]}.") \
                                .add('G', f"{author_['i']} {otchestvo}")
                        else:
                            record.add(701) \
                                .add('A', author_['f']) \
                                .add('B', f"{author_['i'][0]}.") \
                                .add('G', f"{author_['i']}.")

                except:  # если нет отчества у Главного автора
                    record.add(200) \
                        .add('A', all_data['zaglavie']) \
                        .add('E', f'{keyboards.public_types_list[int(all_data["typ_pub"])]}, {all_data["year"]}') \
                        .add('F', f'{fio["i"]}. {fio["f"]}, {fio_authors_for_200[1]}')
                    for author in fio_authors:
                        try:  # Пробуем что у второстепенных авторов есть отчество
                            otchestvo = author['o']
                            record.add(701) \
                                .add('A', author['f']) \
                                .add('B', f"{author['i'][0]}. {author['o'][0]}.") \
                                .add('G', f"{author['i']} {otchestvo}")
                        except:
                            record.add(701) \
                                .add('A', author['f']) \
                                .add('B', f"{author['i'][0]}.") \
                                .add('G', f"{author['i']}.")
        except:  # если нет ни одного соавтора
            try:  # если есть отчество
                glav_author = f'{fio["i"][0]}. {fio["o"][0]}. {fio["f"]}'  # вынесен отдельно, чтобы если У главногоавтора  нет отчества, процесс валился сразу, иначе поля все равно добавляются
                record.add(200) \
                    .add('A', all_data['zaglavie']) \
                    .add('E', f'{keyboards.public_types_list[int(all_data["typ_pub"])]}, {all_data["year"]}') \
                    .add('F', glav_author)
            except:  # если нет отчества
                record.add(200) \
                    .add('A', all_data['zaglavie']) \
                    .add('E', f'{keyboards.public_types_list[int(all_data["typ_pub"])]}, {all_data["year"]}') \
                    .add('F', f'{fio["i"][0]}. {fio["f"]}')

        print('700')
        try:  # Проверяем есть ли отчество
            imya_otchestvo = f'{fio["i"]} {fio["o"]}'  # вынесен отдельно, чтобы если нет отчества, процесс валился сразу, иначе поля все равно добавляются
            record.add(700) \
                .add('A', fio['f']) \
                .add('B', f'{fio["i"][0]}.{fio["o"][0]}.') \
                .add('G', f'{imya_otchestvo}')
        except:
            record.add(700) \
                .add('A', fio['f']) \
                .add('B', f'{fio["i"][0]}.') \
                .add('G', f'{fio["i"]}')
        year = all_data["year"].split('.')
        record.add(210, SF('D', year[-1]))
        record.add(920, ('PAZK'))
        record.add(900, SF('B', '05'))
        record.add(102, ('RU'))
        record.add(101, ('rus'))
        record.add(919) \
            .add('a', 'rus') \
            .add('N', '02') \
            .add('K', 'PSBO')
        record.add(905, SF('2', '1'))
        file_name = all_data['get_pdf']

        # pole_955 =pole_955.replace('й', 'й') #Это не простые й ё, тут составные символы, которые пприлетели от сотрудника. Видимо выбрана не та кодировка
        # pole_955 =pole_955.replace('ё', 'ё')# Чтоб не воняли сотрудники, меняем на нормальные символы

        record.add(955) \
            .add('a', pole_955)  # \

        try:  # если несколько ключевых слов, пробуем разделить по ","
            keyboards_in_all_data = all_data['keywords'].replace('\n', ' ')
            keyboards_in_all_data = keyboards_in_all_data.split(',')
            for keyword in keyboards_in_all_data:
                record.add(610, (keyword.strip()))
        except:
            record.add(610, (all_data['keywords'].strip()))
        print("keywords_en")
        try:  # Проверяем на наличие аннотации на иностранном языке
            try:  # если несколько ключевых слов На иностранном языке, пробуем разделить по ","
                keyboards_in_all_data = all_data['keywords_en'].replace('\n', ' ')
                keyboards_in_all_data = keyboards_in_all_data.split(',')
                for keyword in keyboards_in_all_data:
                    record.add(610, (keyword.strip()))
            except:
                record.add(610, (all_data['keywords_en'].strip()))
        except:
            pass

        annotation = all_data['annotation']
        annotation = annotation.replace('\n', ' ')
        record.add(331, annotation)
        try:  # Пробуем аннотацию на иностранном языке
            annot_en = all_data['abstract']
            annot_en = annot_en.replace('\n', ' ')
            record.add(331, annot_en)
        except:
            pass
        record.add(182, SF('A', 'n'))
        record.add(203) \
            .add('a', 'Текст') \
            .add('C', 'непосредственный')

        # Отправляем запись на сервер
        # Запись попадёт в текущую базу данных
        client.write_record(record)
        info = client.get_database_info(env("IRBIS_REPO_BASE"))
        last_mfn = info.max_mfn - 1
        print(f"Последний mfn: {last_mfn}")
    time.sleep(
        1)  # Добавлена пауза, так как Ирбис слишком медленно думает и выдает ошибочный номер max_mfn = -1, если добавлять без пауз
    info = client.get_database_info(env("IRBIS_REPO_BASE"))
    last_mfn = info.max_mfn - 1
    print(f"Последний mfn: {last_mfn}")
    record = client.read_record(last_mfn)
    exit_text = f"Запись добавлена\n" \
                f"Краткий отчет:\n" \
                f"{record.fm(700, 'a')} {record.fm(700, 'g')}\n" \
                f"{record.fm(200, 'a')} : {record.fm(200, 'e')}, {record.fm(200, 'f')}\n" \
                f"Год издания - {record.fm(210, 'd')}\n" \
                f"{(f'❗❗❗Файл на сервере не найден. Сообщите об ошибке на почту repository@gnpbu.ru', f'Файл на сервер добавлен')[await send_pdf.process_verify_pdf_on_server(record.fm(955, 'a'))]}"

    client.disconnect()
    return exit_text
