# coding=utf-8
from aiogram import Dispatcher, Bot, types, executor

import assembler_message
from run_json import checker, update_sheet
import writer
import Inline_Keyboard

Token_work = '5700162823:AAHXlrfrtM_bTnJeK52Mvs1KnuY9hEqV0LM'
Chat_work = '-1001770966304'

Token_test = '5182014508:AAEBytjLM9Gu-3F2o1Qc2QPt5bwdvNWxFEk'
Chat_test = '-1001626029923'

bot = Bot(Token_work)
dp = Dispatcher(bot)
Reply_message = dict()
mq = str()

@dp.message_handler(commands=['updatesheet'])
async def UpdateSheet(message: types.Message):
    global Sheet
    if message.chat.id == message.from_user.id:
        Sheet = update_sheet()
        if str(message.from_user.id) in Sheet['access_id']:
            await bot.send_message(chat_id=message.chat.id, text='Данні оновлено. Щоб зробити запис натисніть  /start')
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(commands=['counterrowsheet'])
async def Update_number_counter_Sheet(message: types.Message):
    if message.chat.id == message.from_user.id:
        if str(message.from_user.id) in Sheet['access_id']:
            writer.number = writer.update_number_writer()
            await bot.send_message(chat_id=message.chat.id, text='Лічильник рядків оновлено. Щоб зробити запис натисніть  /start')
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global Reply_message, Sheet
    m_id = Inline_Keyboard.func_message(message)[0]
    if message.chat.id == message.from_user.id:
        button = types.InlineKeyboardMarkup(row_width=1)
        Sheet = checker()
        writer.number_writer()
        if str(message.from_user.id) in Sheet['access_id']:
            Reply_message[m_id] = dict()
            button.add(types.InlineKeyboardButton(text='Внести данні в журнал', callback_data='data'),
                       types.InlineKeyboardButton(text='Інформування о дефекті\Зупинка лінії', callback_data='defects_1'),
                       types.InlineKeyboardButton(text='Перерва', callback_data='break'))
            await bot.send_message(message.chat.id, text='Оберіть тип повідомлення:', reply_markup=button)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.callback_query_handler(lambda callback_query: True)
async def device_callback(call: types.CallbackQuery):
    global mq, Reply_message, Sheet
    mq = ''
    button = types.InlineKeyboardMarkup(row_width=1)
    c_id = call.from_user.id
    try:
        Reply_message[c_id]['reported'] = Sheet['access_id'][str(c_id)]
        Reply_message[c_id]['back'] = 'back'
        if call.data in 'back':
            await call.answer('')
            Reply_message[c_id] = dict()
            button.add(types.InlineKeyboardButton(text='Внести данные в журнал', callback_data='data'),
                       types.InlineKeyboardButton(text='Інформування о дефекті\Зупинка лінії',
                                                  callback_data='defects_1'),
                       types.InlineKeyboardButton(text='Перерва', callback_data='break'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='Оберіть тип повідомлення:', reply_markup=button)
        elif (call.data in 'break') or ('backer_line' in call.data):
            await call.answer('')
            if call.data in 'break':
                Reply_message[c_id]['break'] = call.data
            delete = ['count_defects', 'data', 'defects', 'device', 'line', 'no_amount_data', 'non_liquidity', 'yes_coments_information'
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects', 'team'
                      'type', 'type_spec', 'writer_stack', 'time_break', '3_5_10', 'type_defect', 'yes_photo', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            line = [i for i in Sheet['lines']]
            button = Inline_Keyboard.inline_c2(line, 'back', Reply_message[c_id])
            if call.data in 'break':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть лінію:', reply_markup=button)
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Оберіть лінію:', reply_markup=button)
        elif 'defects_1' in call.data:
            await call.answer('')
            Reply_message[c_id]['yes_photo'] = 'defects_1'
            delete = ['count_defects', 'data', 'defects', 'device', 'line', 'no_amount_data', 'non_liquidity', 'yes_coments_information'
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects', 'team'
                       'type', 'type_spec', 'writer_stack', 'time_break', '3_5_10', 'type_defect', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data='back'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Надішліть фото.\n\n⚠️Не більше 10 медіафайлів за 1 раз', reply_markup=button)
        elif (call.data in Sheet['lines']) and ('break' in Reply_message[c_id]):
            await call.answer('')
            Reply_message[c_id]['line'] = call.data
            delete = ['count_defects', 'data', 'defects', 'device', 'no_amount_data', 'non_liquidity', 'yes_coments_information'
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects', 'team'
                       'type', 'type_spec', 'writer_stack', 'time_break', '3_5_10', 'type_defect', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            time_break = [i for i in Sheet['break']]
            button = Inline_Keyboard.inline_c2(time_break, 'break', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть перерву:', reply_markup=button)
        elif call.data in Sheet['break']:
            await call.answer('')
            Reply_message[c_id]['time_break'] = Sheet['break'][call.data]
            delete = ['count_defects', 'data', 'defects', 'device', 'no_amount_data', 'non_liquidity',
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects', 'team'
                       'type', 'type_spec', 'writer_stack', '3_5_10', 'type_defect', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            post = assembler_message.assembling_break(Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='Так', callback_data='yes_break'),
                       types.InlineKeyboardButton(text='⬅️Назад', callback_data=Reply_message[c_id]['line']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'''Перевірте чи вірно сформовані данні:⬇️\n\n{post}''', reply_markup=button)
        elif ('yes' in call.data) and (call.data not in 'yes_amount_data'):
            await call.answer('')
            post = ''
            if 'yes_break' in call.data:
                post = '✅ Повідомлення про відсутність успішно переслане!\nЩоб зробити новий запис натисніть /start'
                reply = assembler_message.assembling_break(Reply_message[c_id])
                await bot.send_message(chat_id=Chat_work, text=reply)
            else:
                if 'yes_3_5_10' in call.data:
                    post = '✅ Повідомлення про зупинку лінії успішно переслане!\nЩоб зробити новий запис натисніть /start'
                elif 'yes_information_of_defect' in call.data:
                    post = '✅ Повідомлення з інформування про дефект переслане!\nЩоб зробити новий запис натисніть /start'
                await bot.send_media_group(chat_id=Chat_work, media=Reply_message[c_id]['med'])

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=post)
        elif call.data in 'data':
            await call.answer('')
            Reply_message[c_id]['data'] = call.data
            delete = ['count_defects', 'defects', 'device', 'no_amount_data', 'non_liquidity', 'yes_coments_information'
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects', 'team'
                       'type', 'type_spec', 'writer_stack', '3_5_10', 'type_defect', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            line = [i for i in Sheet['lines']]
            button = Inline_Keyboard.inline_c2(line, 'back', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть лінію:', reply_markup=button)
        elif (call.data in Sheet['lines']) and (('yes_photo' in Reply_message[c_id]) or ('data' in Reply_message[c_id])):
            await call.answer('')
            Reply_message[c_id]['line'] = call.data
            delete = ['count_defects', 'defects', 'device', 'no_amount_data', 'non_liquidity', 'yes_coments_information'
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects', 'team'
                       'type', 'type_spec', 'writer_stack', '3_5_10', 'type_defect', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            teams = [i for i in Sheet['teams']]
            button = Inline_Keyboard.inline_c2_nonBacker(teams, 'backer_line')
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть команду:', reply_markup=button)
        elif (call.data in Sheet['teams']) and (('yes_photo' in Reply_message[c_id]) or ('data' in Reply_message[c_id])):
            await call.answer('')
            Reply_message[c_id]['team'] = call.data
            delete = ['count_defects', 'defects', 'device', 'no_amount_data', 'non_liquidity', 'yes_coments_information'
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects',
                       'type', 'type_spec', 'writer_stack', '3_5_10', 'type_defect', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            type = [i for i in Sheet['project_all']]
            button = Inline_Keyboard.inline_c2(type, 'line', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть лінійку девайсів:', reply_markup=button)
        elif call.data in Sheet['project_all']:
            await call.answer('')
            Reply_message[c_id]['type'] = call.data
            delete = ['count_defects', 'defects', 'device', 'no_amount_data', 'non_liquidity',
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects',
                    'type_spec', 'writer_stack', '3_5_10', 'type_defect', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            device = [i for i in Sheet['project_all'][Reply_message[c_id]['type']]]
            button = Inline_Keyboard.inline_c2(device, 'team', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть девайс:', reply_markup=button)
        elif ('type' in Reply_message[c_id]) and (call.data in Sheet['project_all'][Reply_message[c_id]['type']]):
            await call.answer('')
            Reply_message[c_id]['device'] = call.data
            delete = ['count_defects', 'defects', 'no_amount_data', 'non_liquidity', 'yes_coments_information'
                      'non_liquidity_board', 'non_liquidity_mult', 'project', 'side', 'spec', 'stack_defects',
                    'type_spec', 'writer_stack', '3_5_10', 'type_defect', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            project = [i for i in Sheet['project_all'][Reply_message[c_id]['type']][Reply_message[c_id]['device']]]
            button = Inline_Keyboard.inline_c1(project, 'type', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть проект:', reply_markup=button)
        elif (call.data in Sheet['project_all'][Reply_message[c_id]['type']][Reply_message[c_id]['device']]) \
                and ('data' in Reply_message[c_id]):
            await call.answer('')
            Reply_message[c_id]['project'] = call.data
            delete = ['count_defects', 'defects', 'no_amount_data', 'non_liquidity','non_liquidity_board', 'coments', 'yes_coments_information'
            'non_liquidity_mult', 'side', 'yes_amount_data', 'spec', 'stack_defects', 'type_spec', 'writer_stack', '3_5_10', 'type_defect']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            side = [i for i in Sheet['spec_all'][Reply_message[c_id]['project']]]
            button = Inline_Keyboard.inline_c2(side, 'device', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть строну:', reply_markup=button)
        elif ('project' in Reply_message[c_id]) and (call.data in Sheet['spec_all'][Reply_message[c_id]['project']]):
            await call.answer('')
            Reply_message[c_id]['side'] = call.data
            Reply_message[c_id]['stack_defects'] = ''
            Reply_message[c_id]['writer_stack'] = []
            delete = ['count_defects', 'defects', 'no_amount_data', 'non_liquidity', 'non_liquidity_board',
                      'non_liquidity_mult', 'spec', 'yes_amount_data', 'yes_count_amount_data', 'type_spec', '3_5_10',
                      'type_defect', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button = types.InlineKeyboardMarkup(row_width=2)
            button.add(types.InlineKeyboardButton(text='Так', callback_data='yes_amount_data'),
                       types.InlineKeyboardButton(text='Ні', callback_data='no_amount_data'))
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data=Reply_message[c_id]['project']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Внести кількість перевірених плат??', reply_markup=button)
        elif 'no_amount_data' in call.data:
            await call.answer('')
            Reply_message[c_id]['no_amount_data'] = call.data
            delete = ['count_defects', 'defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'spec',
                    'type_spec', '3_5_10', 'type_defect', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            defects = [i for i in Sheet['defects']]
            button = Inline_Keyboard.inline_c2(defects, 'side', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть дефект:', reply_markup=button)
        elif call.data in Sheet['defects']:
            await call.answer('')
            Reply_message[c_id]['defects'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'spec',
                    'type_spec', '3_5_10', 'type_defect', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            type_spec = [i for i in Sheet['spec_all'][Reply_message[c_id]['project']][Reply_message[c_id]['side']]]
            button = Inline_Keyboard.inline_c2_nonBacker(type_spec, 'no_amount_data')
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть тип компоненту:', reply_markup=button)
        elif (('project' in Reply_message[c_id]) and ('side' in Reply_message[c_id])) and \
                (call.data in Sheet['spec_all'][Reply_message[c_id]['project']][Reply_message[c_id]['side']]):
            await call.answer('')
            Reply_message[c_id]['type_spec'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'spec',
                     '3_5_10', 'type_defect', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            spec = [i for i in Sheet['spec_all'][Reply_message[c_id]['project']][Reply_message[c_id]['side']] \
                [Reply_message[c_id]['type_spec']]]
            if len(spec) > 99:
                Reply_message[c_id]['data_set_count'] = 0
                button, Reply_message[c_id]['data_set'] = Inline_Keyboard.inline_c3_data100(spec, 'defects', Reply_message[c_id], Reply_message[c_id]['data_set_count'])
            else:
                button = Inline_Keyboard.inline_c3(spec, 'defects', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть компонент:', reply_markup=button)
        elif 'data_set' in call.data:
            await call.answer('')
            if 'data_set+1' in call.data:
                Reply_message[c_id]['data_set_count'] += 1
                spec = [i for i in Sheet['spec_all'][Reply_message[c_id]['project']][Reply_message[c_id]['side']] \
                    [Reply_message[c_id]['type_spec']]]
                button, Reply_message[c_id]['data_set'] = Inline_Keyboard.inline_c3_data100(spec, 'defects', Reply_message[c_id], Reply_message[c_id]['data_set_count'])
            elif 'data_set-1' in call.data:
                Reply_message[c_id]['data_set_count'] -= 1
                spec = [i for i in Sheet['spec_all'][Reply_message[c_id]['project']][Reply_message[c_id]['side']] \
                    [Reply_message[c_id]['type_spec']]]
                button, Reply_message[c_id]['data_set'] = Inline_Keyboard.inline_c3_data100(spec, 'defects', Reply_message[c_id], Reply_message[c_id]['data_set_count'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть компонент:', reply_markup=button)
        elif 'yes_amount_data' in call.data:
            await call.answer('')
            Reply_message[c_id]['yes_amount_data'] = call.data
            delete = ['count_defects', 'defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'spec',
                      'type_spec', '3_5_10', 'type_defect', 'coments', 'yes_coments_information', 'yes_count_amount_data']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data=Reply_message[c_id]['side']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть кількість:', reply_markup=button)
        elif (('project' in Reply_message[c_id]) and ('side' in Reply_message[c_id]) and ('type_spec' in Reply_message[c_id]))\
            and (call.data in Sheet['spec_all'][Reply_message[c_id]['project']][Reply_message[c_id]['side']]
            [Reply_message[c_id]['type_spec']]):
            await call.answer('')
            Reply_message[c_id]['spec'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', '3_5_10',
                      'coments', 'type_defect', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data=Reply_message[c_id]['type_spec']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть кількість дефектів:', reply_markup=button)
        elif (call.data in Sheet['project_all'][Reply_message[c_id]['type']][Reply_message[c_id]['device']]) \
                and ('yes_photo' in Reply_message[c_id]):
            await call.answer('')
            Reply_message[c_id]['project'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', '3_5_10',
                      'coments', 'type_defect', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            backer = Reply_message[c_id]['device']
            button = types.InlineKeyboardMarkup(row_width=1)
            button.add(types.InlineKeyboardButton(text='Інформування о дефекті', callback_data='information_of_defect'),
                       types.InlineKeyboardButton(text='Зупинка лінії', callback_data='stop_line'),
                       types.InlineKeyboardButton(text='⬅️Назад', callback_data=backer))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Тип повідомлення:', reply_markup=button)
        elif 'stop_line' in call.data:
            await call.answer('')
            Reply_message[c_id]['type_defect'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', '3_5_10', 'coments',
                      'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            stop = [i for i in Sheet['3_5_10']]
            button = Inline_Keyboard.inline_c2(stop, 'project', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Оберіть по якому принципу зупинена лінія:', reply_markup=button)
        elif (call.data in Sheet['3_5_10']) and (call.data in 'Коментар'):
            await call.answer('')
            Reply_message[c_id]['3_5_10'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data='stop_line'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть коментар по зупинці лінії:', reply_markup=button)
        elif (call.data in Sheet['3_5_10']) and ('Коментар' not in call.data):
            await call.answer('')
            Reply_message[c_id]['3_5_10'] = Sheet['3_5_10'][call.data]
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            if 'coments' in Reply_message[c_id]:
                del Reply_message[c_id]['coments']
            post = assembler_message.assembling_3_5_10(Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='Так', callback_data='yes_3_5_10'),
                       types.InlineKeyboardButton(text='⬅️Назад', callback_data=Reply_message[c_id]['type_defect']))
            Reply_message[c_id]['med'] = Inline_Keyboard.media(Reply_message[c_id], post)
            await bot.send_media_group(call.message.chat.id, media=Reply_message[c_id]['med'])
            await bot.send_message(call.message.chat.id, text='Перевірте чи вірно сформовані данні', reply_markup=button)
        elif 'information_of_defect' in call.data:
            await call.answer('')
            Reply_message[c_id]['information'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'coments', 'amount',
                      'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data=Reply_message[c_id]['project']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть кількість:', reply_markup=button)
        elif call.data in 'coments_information':
            await call.answer('')
            Reply_message[c_id]['yes_coments_information'] = call.data
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'non_liquidity_mult', 'coments']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data='back_coments_information'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть коментар:', reply_markup=button)
        elif 'back_coments_information' in call.data:
            await call.answer('')
            button = types.InlineKeyboardMarkup(row_width=2)
            button.add(types.InlineKeyboardButton(text='Так', callback_data='coments_information'),
                       types.InlineKeyboardButton(text='Ні', callback_data='no_coment_information'))
            button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data='information_of_defect'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Внести коментар?', reply_markup=button)
        elif 'no_coment_information' in call.data:
            await call.answer('')
            post = assembler_message.assembling_information_defects(Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='Так', callback_data='yes_information_of_defect'),
                       types.InlineKeyboardButton(text='⬅️Назад', callback_data='back_coments_information'))
            Reply_message[c_id]['med'] = Inline_Keyboard.media(Reply_message[c_id], post)
            await bot.send_media_group(call.message.chat.id, media=Reply_message[c_id]['med'])
            await bot.send_message(call.message.chat.id, text='Перевірте чи вірно сформовані данні',
                                   reply_markup=button)
        elif call.data in 'non_liquidity':
            await call.answer('')
            Reply_message[c_id]['non_liquidity'] = None
            delete = ['count_defects', 'non_liquidity_board', 'non_liquidity_mult', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='back_post'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть кількість неліквідних плат:', reply_markup=button)
        elif call.data in 'non_liquidity_mult':
            await call.answer('')
            Reply_message[c_id]['non_liquidity_mult'] = None
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='non_liquidity'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть кількість мультиплікатов з дефектом:', reply_markup=button)
        elif 'NOK_defect' in call.data:
            await call.answer('')
            delete = ['amount', 'non_liquidity', 'repair', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            defect = [i for i in Sheet['defects']]
            backer = 'spec' if Reply_message[c_id]['stack_defects'] in '' else 'back_post'
            button = Inline_Keyboard.inline_c2_nonBacker(defect, backer)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть дефект:',
                                        reply_markup=button)
        elif call.data in 'back_post':
            await call.answer('')
            button = types.InlineKeyboardMarkup(row_width=2)
            button.add(
                types.InlineKeyboardButton(text='Додати дефект', callback_data='NOK_defect'),
                types.InlineKeyboardButton(text='Наступний крок ➡️', callback_data='non_liquidity')
            )
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_amount'))
            await bot.send_message(call.message.chat.id, text=f"{Reply_message[c_id]['stack_defects']}\n", reply_markup=button)
        elif call.data in 'back_amount':
            await call.answer('')
            b = Reply_message[c_id]['stack_defects'].split('Дефект:')
            b = b[:-1]
            Reply_message[c_id]['stack_defects'] = 'Дефект:'.join(b)
            Reply_message[c_id]['writer_stack'] = Reply_message[c_id]['writer_stack'][:-1]
            Reply_message[c_id]['amount'] = None
            delete = ['count_defects', 'non_liquidity', 'non_liquidity_board', 'coments', 'yes_coments_information']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data=Reply_message[c_id]['defects']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть кількість плат з дефектом:', reply_markup=button)
        elif call.data in 'non_count_sheet':
            await call.answer('')
            writer.writer(Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='✅ Данні успішно внесені в таблицю.\nЩоб Зробити новий запис натисніть /start')
        elif 'no_count_data' in call.data:
            await call.answer('')
            button.add(types.InlineKeyboardButton(text='Так', callback_data='sheet_count_data'),
                       types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='back_count_data'))
            post = assembler_message.non_count_data(Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=post)
            await bot.send_message(call.message.chat.id, text='Перевірте чи вірно сформовані данні?', reply_markup=button)
        elif 'sheet_count_data' in call.data:
            await call.answer('')
            writer.writer_non_defect(Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='✅ Данні успішно внесені в таблицю.\nЩоб Зробити новий запис натисніть /start')
        elif 'back_count_data' in call.data:
            await call.answer('')
            button.add(types.InlineKeyboardButton(text='Так', callback_data='no_amount_data'),
                       types.InlineKeyboardButton(text='Ні', callback_data='no_count_data'))
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='yes_amount_data'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text='Внести дефекти?', reply_markup=button)
    except ZeroDivisionError:
        pass


@dp.message_handler(content_types=['video', 'photo'])
async def photo(message):
    global Reply_message, mq, Sheet
    m_id = Inline_Keyboard.func_message(message)[0]
    if message.chat.id == m_id:
        Sheet = checker()
        if str(message.chat.id) in Sheet['access_id']:
            if 'yes_photo' in Reply_message[m_id]:
                if mq == '':
                    Reply_message[m_id]['photos'] = []
                    Reply_message[m_id]['videos'] = []
                    Reply_message[m_id]['med'] = []
                    Reply_message[m_id]['stack_defects'] = ''
                    Reply_message[m_id]['writer_stack'] = []
                try:
                    Reply_message[message.chat.id]['photos'].append(message.photo[0].file_id)
                except (KeyError, IndexError):
                    pass
                try:
                    Reply_message[message.chat.id]['videos'].append(message.video.file_id)
                except AttributeError:
                    pass
                line = [i for i in Sheet['lines']]
                button = Inline_Keyboard.inline_c2(line, 'yes_photo', Reply_message[m_id])
                if mq == '':
                    mq = message.media_group_id
                    await bot.send_message(chat_id=message.chat.id, text='Оберіть лінію:', reply_markup=button)
                    mq = ''
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')



@dp.message_handler(content_types=['text'])
async def handle_files(message):
    if message.chat.id == message.from_user.id:
        if str(message.from_user.id) in Sheet['access_id']:
            global Reply_message, mq
            button = types.InlineKeyboardMarkup(row_width=2)
            try:
                m_id = Inline_Keyboard.func_message(message)[0]
                text_message = Inline_Keyboard.func_message(message)[1]
                if ('3_5_10' in Reply_message[m_id]) and (Reply_message[m_id]['3_5_10'] in 'Коментар'):
                    Reply_message[m_id]['3_5_10'] = Sheet['3_5_10'][Reply_message[m_id]['3_5_10']]
                    Reply_message[m_id]['coments'] = text_message
                    post = assembler_message.assembling_3_5_10(Reply_message[m_id])
                    button.add(types.InlineKeyboardButton(text='Так', callback_data='yes_3_5_10'),
                               types.InlineKeyboardButton(text='⬅️Назад',
                                                          callback_data=Reply_message[m_id]['type_defect']))
                    Reply_message[m_id]['med'] = Inline_Keyboard.media(Reply_message[m_id], post)
                    await bot.send_media_group(message.chat.id, media=Reply_message[m_id]['med'])
                    await bot.send_message(message.chat.id, text='Перевірте чи вірно сформовані данні',
                                           reply_markup=button)
                elif ('information' in Reply_message[m_id]) and ('amount' not in Reply_message[m_id]):
                    if message.text.isdigit():
                        Reply_message[m_id]['amount'] = text_message
                        button.add(types.InlineKeyboardButton(text='Так', callback_data='coments_information'),
                                   types.InlineKeyboardButton(text='Ні', callback_data='no_coment_information'))
                        button.add(types.InlineKeyboardButton(text='⬅️Назад', callback_data='information_of_defect'))
                        await bot.send_message(message.chat.id, text='Внести коментар?', reply_markup=button)
                    else:
                        post = assembler_message.input_validation_defect
                        await bot.send_message(message.chat.id, text=post)
                elif 'yes_coments_information' in Reply_message[m_id]:
                    Reply_message[m_id]['coments'] = text_message
                    post = assembler_message.assembling_information_defects(Reply_message[m_id])
                    button.add(types.InlineKeyboardButton(text='Так', callback_data='yes_information_of_defect'),
                               types.InlineKeyboardButton(text='⬅️Назад',
                                                          callback_data='back_coments_information'))
                    Reply_message[m_id]['med'] = Inline_Keyboard.media(Reply_message[m_id], post)
                    await bot.send_media_group(message.chat.id, media=Reply_message[m_id]['med'])
                    await bot.send_message(message.chat.id, text='Перевірте чи вірно сформовані данні',
                                           reply_markup=button)
                elif ('yes_amount_data' in Reply_message[m_id]) and ('yes_count_amount_data' not in Reply_message[m_id]):
                    if message.text.isdigit():
                        Reply_message[m_id]['yes_count_amount_data'] = text_message
                        button.add(types.InlineKeyboardButton(text='Так', callback_data='no_amount_data'),
                                   types.InlineKeyboardButton(text='Ні', callback_data='no_count_data'))
                        button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='yes_amount_data'))
                        await bot.send_message(message.chat.id, text='Внести дефекти?', reply_markup=button)
                    else:
                        post = assembler_message.input_validation_defect
                        await bot.send_message(message.chat.id, text=post)
                elif ('side' in Reply_message[m_id]) and ('non_liquidity' not in Reply_message[m_id]):
                    if message.text.isdigit():
                        Reply_message[m_id]['count_defects'] = text_message
                        button.add(
                            types.InlineKeyboardButton(text='Додати дефект', callback_data='NOK_defect'),
                            types.InlineKeyboardButton(text='Наступний крок ➡️', callback_data='non_liquidity')
                        )
                        button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_amount'))
                        Reply_message[m_id]['stack_defects'] += assembler_message.assembling_defect(Reply_message[m_id])
                        await bot.send_message(message.chat.id, text=f"{Reply_message[m_id]['stack_defects']}\n",
                                               reply_markup=button)
                    else:
                        post = assembler_message.input_validation_defect
                        await bot.send_message(message.chat.id, text=post)
                elif ('non_liquidity' in Reply_message[m_id]) and ('non_liquidity_mult' not in Reply_message[m_id]):
                    if message.text.isdigit():
                        Reply_message[m_id]['non_liquidity_board'] = text_message
                        Reply_message[m_id]['non_liquidity_mult'] = None
                        button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='non_liquidity'))
                        await bot.send_message(message.chat.id, text='Введіть загальну кількість плат переданих на ремонт:',
                                               reply_markup=button)
                    else:
                        post = assembler_message.input_validation_defect
                        await bot.send_message(message.chat.id, text=post)
                elif 'non_liquidity_mult' in Reply_message[m_id]:
                    if message.text.isdigit():
                        Reply_message[m_id]['non_liquidity_mult'] = text_message
                        post = assembler_message.non_count_data(Reply_message[m_id])
                        button.add(types.InlineKeyboardButton(text='Так', callback_data='non_count_sheet'),
                            types.InlineKeyboardButton(text='⬅️ Назад', callback_data='non_liquidity_mult'))
                        await bot.send_message(message.chat.id, text=post)
                        await bot.send_message(message.chat.id, text='Перевірте чи вірно сформовані данні?', reply_markup=button)
                    else:
                        post = assembler_message.input_validation_defect
                        await bot.send_message(message.chat.id, text=post)
                else:
                    await bot.send_message(message.chat.id, text=assembler_message.input_validation_defect)
            except ZeroDivisionError:
                pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=False)