import aiogram.types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

go_to_reg_button = InlineKeyboardButton(
    text='Начать регистрацию',
    callback_data='fill_register_user'
)
out_to_reg_button = InlineKeyboardButton(
    text='Не регистрироваться',
    callback_data='cancel_register'
)
keyboard_to_reg = InlineKeyboardMarkup(
    inline_keyboard=[[go_to_reg_button],
                     [out_to_reg_button]])

button_start = KeyboardButton(text='/start')
button_help = KeyboardButton(text='/help')
keyboards_start_help = ReplyKeyboardMarkup(keyboard=[[button_start], [button_help],],  resize_keyboard=True)

button_add = KeyboardButton(text="Добавить новую запись 📙")
keyboards_registred = ReplyKeyboardMarkup(keyboard=[[button_add],[button_start], [button_help],])

inline_button_add = InlineKeyboardButton(
    text="Добавить новую запись 📙",
    callback_data='!_add_new_data_!'
)
keyboard_add_new_data = InlineKeyboardMarkup(
    inline_keyboard=[[inline_button_add]])

type_button1 = InlineKeyboardButton(
    text='Научная статья',
    callback_data='0'
)
type_button2 = InlineKeyboardButton(
    text='Автореферат диссертации',
    callback_data='1'
)
type_button3 = InlineKeyboardButton(
    text='Диссертация',
    callback_data='2'
)
type_button4 = InlineKeyboardButton(
    text='Препринт',
    callback_data='3'
)
type_button5 = InlineKeyboardButton(
    text='Монография (отдельные главы)',
    callback_data='4'
)
type_button6 = InlineKeyboardButton(
    text='Учебник',
    callback_data='5'
)
type_button7 = InlineKeyboardButton(
    text='Учебное пособие',
    callback_data='6'
)
type_button8 = InlineKeyboardButton(
    text='Cборник материалов научной конференции',
    callback_data='7'
)
type_button9 = InlineKeyboardButton(
    text='Презентация, научный доклад',
    callback_data='8'
)
type_button10 = InlineKeyboardButton(
    text='Научный отчет',
    callback_data='9'
)
type_button11 = InlineKeyboardButton(
    text='Тип публикации - другое',
    callback_data='10'
)
# keyboards_type_pub = InlineKeyboardMarkup(
#     inline_keyboard=[[type_button1],
#                      [type_button2], [type_button3],[type_button4], [type_button5],[type_button6],[type_button7], [type_button8], [type_button9], [type_button10]])
keyboards_type_pub = InlineKeyboardMarkup(
    inline_keyboard=[[type_button1],
                     [type_button2], [type_button3],[type_button4], [type_button5],[type_button6],[type_button7],[type_button8], [type_button9], [type_button10],[type_button11] ])

public_types_list = ['Научная статья', 'Автореферат диссертации', 'Диссертация', 'Препринт', 'Монография (отдельные главы)', 'Учебник',
                'Учебное пособие','Cборник материалов научной конференции', 'Презентация, научный доклад', 'Научный отчет', 'Тип публикации - другое']

button_yes = InlineKeyboardButton(
    text='Да',
    callback_data='!_yes_!'
)
button_no = InlineKeyboardButton(
    text='Нет',
    callback_data='!_no_!'
)
keyboards_yes_no = InlineKeyboardMarkup(inline_keyboard=[[button_yes, button_no]])

button_send = InlineKeyboardButton(
    text='Отправить в репозиторий',
    callback_data='!_send_!'
)
button_no_send = InlineKeyboardButton(
    text='Начать сначала',
    callback_data='!_no_send_!'
)
keyboards_send_yes_no = InlineKeyboardMarkup(inline_keyboard=[[button_send, button_no_send]])