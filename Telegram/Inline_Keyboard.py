# coding=utf-8
from aiogram import types

def inline_c2(data, backer, c_id):
    button = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(data), 2):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                types.InlineKeyboardButton(text=data[i+1], callback_data=data[i+1])
            )
        except IndexError:
            button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                       types.InlineKeyboardButton(text='⬅️ Назад', callback_data=c_id[backer]))
        else:
            if data[i+1] == data[-1]:
                button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=c_id[backer]))
    return button

def inline_c3(data, backer, c_id):
    button = types.InlineKeyboardMarkup(row_width=3)
    for i in range(0, len(data), 3):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                types.InlineKeyboardButton(text=data[i+1], callback_data=data[i+1]),
                types.InlineKeyboardButton(text=data[i+2], callback_data=data[i+2]),
            )
        except IndexError:
            try:
                if data[i + 1] == data[-1]:
                    button.add(
                        types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                        types.InlineKeyboardButton(text=data[i+1], callback_data=data[i+1])
                    )
                    button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=c_id[backer]))
            except IndexError:
                if data[i] == data[-1]:
                    button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                               types.InlineKeyboardButton(text='⬅️ Назад', callback_data=c_id[backer])
                    )
        else:
            if data[i+2] == data[-1]:
                button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=c_id[backer]))
    return button

def inline_c3_data100(data, backer, c_id, count=0):
    button = types.InlineKeyboardMarkup(row_width=3)
    data_set = []
    count = count
    while data:
        if len(data) > 99:
            ind_ex = 97
            data_set.append(data[:ind_ex])
        else:
            ind_ex = len(data)
            data_set.append(data[:ind_ex])
        data = data[ind_ex:]

    elem = data_set[count]
    for i in range(0, len(elem), 3):
        try:
            button.add(
                types.InlineKeyboardButton(text=elem[i], callback_data=elem[i]),
                types.InlineKeyboardButton(text=elem[i + 1], callback_data=elem[i + 1]),
                types.InlineKeyboardButton(text=elem[i + 2], callback_data=elem[i + 2]),
            )
        except IndexError:
            try:
                button.add(
                    types.InlineKeyboardButton(text=elem[i], callback_data=elem[i]),
                    types.InlineKeyboardButton(text=elem[i + 1], callback_data=elem[i + 1])
                )
            except IndexError:
                button.add(
                    types.InlineKeyboardButton(text=elem[i], callback_data=elem[i])
                )
    if (count == 0):
        button.add(
            types.InlineKeyboardButton(text="Наступна сторінка⏩📖", callback_data='data_set+1')
        )
    elif data_set[count] != data_set[-1]:
        button.add(
            types.InlineKeyboardButton(text='📖⏪Попередня сторінка', callback_data='data_set+1'),
            types.InlineKeyboardButton(text="Наступна сторінка⏩📖", callback_data='data_set-1'),
        )
    elif data_set[count] == data_set[-1]:
        button.add(
            types.InlineKeyboardButton(text='📖⏪Попередня сторінка', callback_data='data_set-1')
        )
    button.add(
        types.InlineKeyboardButton(text='⬅️ Назад', callback_data=c_id[backer])
    )
    return button, data_set

def inline_c1(data, backer, c_id):
    button = types.InlineKeyboardMarkup(row_width=1)
    for i in range(0, len(data)):
        button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]))
    button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=c_id[backer]))
    return button


def inline_c2_home(data):
    button = types.InlineKeyboardMarkup()
    for i in range(0, len(data), 2):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                types.InlineKeyboardButton(text=data[i+1], callback_data=data[i+1])
            )
        except IndexError:
            button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]))
    return button

def inline_c2_nonBacker(data, backer):
    button = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(data), 2):
        try:
            button.add(
                types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                types.InlineKeyboardButton(text=data[i+1], callback_data=data[i+1])
            )
        except IndexError:
            button.add(types.InlineKeyboardButton(text=data[i], callback_data=data[i]),
                       types.InlineKeyboardButton(text='⬅️ Назад', callback_data=backer))
        else:
            if data[i+1] == data[-1]:
                button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=backer))
    return button

def func_message(message):
    message_id = message.from_user.id
    message_txt = message.text
    return message_id, message_txt

def deleter_key(delete, c_id):
    for key in delete:
        if key in c_id:
            c_id.pop(key)
    return c_id

def media(m_id, post):
    med = []
    for i in m_id['photos']:
        if i != m_id['photos'][-1]:
            med.append(types.InputMediaPhoto(media=i))
        else:
            med.append(types.InputMediaPhoto(media=i, caption=post))
    for i in m_id['videos']:
        if m_id['photos']:
            med.append(types.InputMediaVideo(media=i))
        else:
            if i != m_id['videos'][-1]:
                med.append(types.InputMediaVideo(media=i))
            else:
                med.append(types.InputMediaVideo(media=i, caption=post))
    return med