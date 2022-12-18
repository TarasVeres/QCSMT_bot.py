import time

def assembling_break(c_id):
    post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n''' \
           f'''Лінія: {c_id['line']}\n''' \
           f'''Оператор: {c_id['reported']}\n'''\
           f'''{c_id['time_break']}'''
    return post

def assembling_3_5_10(c_id):
    stop = c_id['3_5_10'].split('.')
    stop = '\n'.join(stop)
    post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n'''
    if ('coments' in c_id) and ('3_5_10' in c_id):
        post += f'''{stop} {c_id['coments']}\n'''
    if ('coments' not in c_id) and ('3_5_10' in c_id):
        post += f'''{stop}\n'''
    post += f'''Проект: {c_id['project']}\n'''
    post += f'''Лінія: {c_id['line']} - {c_id['team']}\n'''\
            f'''Оператор: {c_id['reported']}'''
    return post

def assembling_information_defects(c_id):
    post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n''' \
           f'''Проект: {c_id['project']}\n''' \
           f'''Лінія: {c_id['line']} - {c_id['team']}\n''' \
           f'''Кількість дефектів: {c_id['amount']}\n'''
    if ('coments' in c_id):
        post += f'''{c_id['coments']}\n'''
    post += f'''Оператор: {c_id['reported']}'''
    return post

def assembling_defect(m_id):
    assembliator = f'''Дефект: {m_id['defects']}\n'''\
                  f'''Сторона: {m_id['side']}\n'''\
                  f'''Компонент: {m_id['spec']}\n'''\
                  f'''Кількість: {m_id['count_defects']}\n'''\
                  f'''__________\n'''
    writer_defect(m_id)
    return assembliator

def writer_defect(m_id):
    m_id['writer_stack'].append([m_id['defects'], m_id['side'], m_id['spec'], m_id['count_defects']])
    return m_id

def non_count_data(c_id):
    post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n''' \
           f'''Проект: {c_id['project']}\n''' \
           f'''Лінія: {c_id['line']} - {c_id['team']}\n'''
    if 'yes_count_amount_data' in c_id:
        post += f'''Перевірено: {c_id['yes_count_amount_data']}\n'''
    if 'non_liquidity_board' in c_id:
        post += f'''Плат з дефектами: {c_id['non_liquidity_board']}\n'''\
                f'''Мультипликатов з дефектними платами: {c_id['non_liquidity_mult']}'''\
                f'''\n__________\n''' \
                f'''{c_id['stack_defects']}'''
    post += f'''Оператор: {c_id['reported']}'''
    return post


input_validation_defect = f'Введено невірні данні\n\n' \
           f'✅Tільки числа\n' \
           f'❌Заборонено вводити літери\n' \
           f'❌Заборонено вводити десяткові цифри\n\n' \
           f'Введіть кількість ще раз'