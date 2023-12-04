import datetime
import string
cyrillic_lower_letters = [' ','-','а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
cyrillic_letters = set()
for i in cyrillic_lower_letters:
    cyrillic_letters.add(i)
alphanbet = set(string.ascii_letters)|cyrillic_letters

async def check_author(text: str) ->bool:
    flag = True
    count_probel = 0
    fio = []
    try:
        if text.count(" ") == 0: # Проверяем чтоб был хотя бы 1 пробел, значит есть Фамилия и имя
            return False
        else:
            s = text.split(' ')
            for i in s:
                if i!='':
                    fio.append(i)
            if len(fio)<2:
                return False

        for i in text: # Проверяем на наличие только тех символов, которые есть в множестве alphanbet
            if i not in alphanbet:
                flag = False
        return flag
    except:
        return False

async def check_authors(text: str) ->bool:
    flag = True
    try:
        try:
            s = text.split(',')
            s = [i.strip() for i in s]
            for i in s:
                return await check_author(i)
        except:
            return await check_author(text)
    except:
        return False

async def check_year(year):
    try:
        t = datetime.datetime.strptime(str(year), '%d.%m.%Y' )
        if t< datetime.datetime.now():
            return True
        else:
            return False
    except:
        return False


async def check_print_authors(all_data):
    try:
        s = all_data["authors"]
        return s
    except:
        return "отсутствуют"

async def check_print_abstract(all_data):
    try:
        s = all_data["abstract"]
        return s
    except:
        return "отсутствует"

async def check_print_keywords_en(all_data):
    try:
        s = all_data["keywords_en"]
        return s
    except:
        return "отсутствуют"