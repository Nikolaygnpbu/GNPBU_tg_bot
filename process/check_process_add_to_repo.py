async def check_fio_author(fio): #подготовка ФИО к введению в поля
    fio_dict = {}
    fio_temp = []
    s = fio.split(' ')
    for i in s:
        if i != '':
            fio_temp.append(i)
    if len(fio_temp)==2:
        fio_dict.setdefault('f',fio_temp[0])
        fio_dict.setdefault('i',fio_temp[1])
    elif len(fio_temp)==3:
        fio_dict.setdefault('f',fio_temp[0])
        fio_dict.setdefault('i',fio_temp[1])
        fio_dict.setdefault('o',fio_temp[2])
    elif len(fio_temp)>3:
        fio_dict.setdefault('f',fio_temp[0])
        fio_dict.setdefault('i',fio_temp[1])
        fio_dict.setdefault('o',' '.join(fio_temp[2:]))
    return fio_dict

async def check_fio_authors(fio_authors): #Проверяем авторов
    authors_list = []
    fio_authors = fio_authors.split(',')
    print('fio_authors', fio_authors)
    fio_authors = [i.strip() for i in fio_authors]
    print('fio_authors1', fio_authors)
    for i in fio_authors:
        if i!='':
            authors_list.append(await check_fio_author(i))
    print('authors_list', authors_list)
    return authors_list

async def create_authors_string_pole_200(list_authors):
    authors_string = []
    try:
        for i in list_authors:
            if len(i)==2:
                authors_string.append(f"{i['i'][0]}. {i['f']}")
            if len(i)==3:
                authors_string.append(f"{i['i'][0]}. {i['o'][0]}. {i['f']}")
        return [True, ', '.join(authors_string)] # Собираем всех авторов через запятую
    except:
        return [False]

