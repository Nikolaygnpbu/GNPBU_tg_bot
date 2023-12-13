import smtplib
from email.mime.text import MIMEText
from email.header import Header
from environs import Env

async def send_email_ok(all_data_in_mfn):
    env = Env()

    obrashenie = ''
    if all_data_in_mfn[23] == 'м':
        obrashenie = 'Уважаемый'
    else:
        obrashenie = 'Уважаемая'
    msg = MIMEText(
        f'{obrashenie} {all_data_in_mfn[10]} {all_data_in_mfn[11]}!\nВы зарегистрированы в Репозитории РАО. Для входа в систему используйте следующие данные:\n'
        f'Логин: {all_data_in_mfn[30]}\n'
        f'Пароль:{all_data_in_mfn[130]}\n\n'
        f'-------\n'
        f'Репозиторий РАО', 'plain', 'utf-8')
    msg['Subject'] = Header('Регистрация в репозитории РАО', 'utf-8')
    msg['From'] = env("SENT_FROM")
    msg['To'] = all_data_in_mfn[32]
    user = env('USER')
    password = env("PASSWORD")
    sent_to = all_data_in_mfn[32]
    s = smtplib.SMTP_SSL(env("SMTP_SERVER"), int(env("SSL_PORT")), timeout=10)
    s.set_debuglevel(1)
    try:
        s.ehlo()
        s.login(user, password)
        s.sendmail(msg['From'], sent_to, msg.as_string())
    finally:
        print(msg)
        s.quit()
async def send_email_no_ok(all_data_in_mfn):
    env = Env()


    obrashenie = ''
    if all_data_in_mfn[23] == 'м':
        obrashenie = 'Уважаемый'
    else:
        obrashenie = 'Уважаемая'
    msg = MIMEText(
        f'{obrashenie} {all_data_in_mfn[10]} {all_data_in_mfn[11]}, к сожалению, доступ к материалам репозитория РАО предоставляется только научным сотрудникам РАО.\n'
        f'Ваша заявка отклонена.\n\n'
        f'-------\n'
        f'Репозиторий РАО', 'plain', 'utf-8')
    msg['Subject'] = Header('Регистрация в репозитории РАО', 'utf-8')
    msg['From'] = env("SENT_FROM")
    msg['To'] = all_data_in_mfn[32]
    user = env('USER')
    password = env("PASSWORD")
    sent_to = all_data_in_mfn[32]
    s = smtplib.SMTP_SSL(env("SMTP_SERVER"), int(env("SSL_PORT")), timeout=10)
    s.set_debuglevel(1)
    try:
        s.ehlo()
        s.login(user, password)
        s.sendmail(msg['From'], sent_to, msg.as_string())
    finally:
        print(msg)
        s.quit()