import time
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '15hCNBPiViHGKPxxSuMHrv6ZOd20vtlQqUPM4K731U_w'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

day = 32
number = 4

def number_writer():
    global day, number
    if day != time.localtime().tm_mday:
        _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Print!A1:A30000', majorDimension='ROWS').execute()
        number = int(_['values'][-1][-1]) if _['values'][-1][-1] != '№' else 4
        day = time.localtime().tm_mday
    return number

def update_number_writer():
    global day, number
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Print!A1:A30000', majorDimension='COLUMNS').execute()
    number = int(_['values'][-1][-1]) if _['values'][-1][-1] != '№' else 4
    return number

def writer(c_id):
    global number
    number += 1
    value = [[''] for i in range(29)]
    value[0] = [str(number)]
    value[1] = [time.strftime("%d.%m.%Y", time.localtime())]
    value[2] = [time.strftime("%H:%M", time.localtime())]
    value[3] = [c_id['line']]
    value[4] = [c_id['project']]
    value[5] = [c_id['side']]
    value[6] = [c_id['team']]
    value[9] = [c_id['non_liquidity_board']]
    value[10] = [c_id['non_liquidity_mult']]
    if 'yes_count_amount_data' in c_id:
        value[8] = [c_id['yes_count_amount_data']]
        value[7] = [int(*value[8]) - int(*value[10])]
    for i in c_id['writer_stack']:
        defects = {
            "Розворот по куту": 11,
            "Зміщення компонента": 12,
            "Відсутність компонента": 13,
            "Недостатнє змочування": 14,
            "Кульки припою": 15,
            "Відсутність змочування": 16,
            "Відсутність паяного з'єднання": 17,
            "Коротке замикання": 18,
            "Неліквідний компонент": 19,
            "Невірна полярність": 20,
            "Перевернутий": 21,
            "Пошкодження маски": 22,
            "Неліквід плати": 23,
            "Помилковий компонент": 24,
            "Зайвий компонент": 25,
            "Проміжок": 26,
            "Окислені контактні майданчики": 27,
        }
        if value[defects[i[0]]] != ['']:
            value[defects[i[0]]][0] += f'/{i[2]}-{i[3]}'
        else:
            value[defects[i[0]]] = [f'{i[2]}-{i[3]}']
    value[28] = [c_id['reported']]
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Print!A{number}:AC30000',
                 "majorDimension": "COLUMNS",
                 "values": value}
            ]
        }
    ).execute()

def writer_non_defect(c_id):
    global number
    number += 1
    value = [[''] for i in range(29)]
    value[0] = [str(number)]
    value[1] = [time.strftime("%d.%m.%Y", time.localtime())]
    value[2] = [time.strftime("%H:%M", time.localtime())]
    value[3] = [c_id['line']]
    value[4] = [c_id['project']]
    value[5] = [c_id['side']]
    value[6] = [c_id['team']]
    value[7] = [c_id['yes_count_amount_data']]
    value[8] = [c_id['yes_count_amount_data']]
    value[9] = [0]
    value[10] = [0]
    value[28] = [c_id['reported']]
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Print!A{number}:AC30000',
                 "majorDimension": "COLUMNS",
                 "values": value}
            ]
        }
    ).execute()

