# coding=utf-8
import json
import pprint

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

Sheet = dict()

def func_Access_id():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Access_id!A1:B100', majorDimension='ROWS').execute()
    Sheet['access_id'] = {}
    for i in _['values']:
        Sheet['access_id'][int(i[0])] = i[1]
    return Sheet

def func_Line():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Lines!A1:A30', majorDimension='ROWS').execute()
    Sheet['lines'] = []
    for i in _['values']:
        Sheet['lines'] += [i[0]]
    return Sheet

def func_Teams():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Teams!A1:A30', majorDimension='ROWS').execute()
    Sheet['teams'] = []
    for i in _['values']:
        Sheet['teams'] += [i[0]]
    return Sheet

def func_Break():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Break!A1:B30', majorDimension='ROWS').execute()
    Sheet['break'] = dict()
    for i in _['values']:
        Sheet['break'][i[0]] = i[1]
    return Sheet

def func_3_5_10():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='3_5_10!A1:B10', majorDimension='ROWS').execute()
    Sheet['3_5_10'] = dict()
    for i in _['values']:
        Sheet['3_5_10'][i[0]] = i[1]
    return Sheet

def func_Device():
    global Sheet, type, device
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Stage_device!A1:C500', majorDimension='ROWS').execute()
    Sheet['project_all'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                type = i[0]
                Sheet['project_all'][type] = [] if i[1] == i[-1] else {}
            if (i[1] != '') and (i[1] == i[-1]):
                device = i[1]
                Sheet['project_all'][type] += [device]
            if (i[1] != '') and (i[1] != i[-1]):
                device = i[1]
                Sheet['project_all'][type][device] = [] if i[2] == i[-1] else {}
            if (i[2] != '') and (i[2] == i[-1]):
                project = i[2]
                Sheet['project_all'][type][device] += [project]
        except (IndexError, KeyError):
            pass
    return Sheet



def func_Spec():
    global Sheet, project, side, spec
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Stage_component!A1:D30000', majorDimension='ROWS').execute()
    Sheet['spec_all'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                project = i[0]
                Sheet['spec_all'][project] = [] if i[1] == i[-1] else {}
            if (i[1] != '') and (i[1] == i[-1]):
                side = i[1]
                Sheet['spec_all'][project] += [side]
            if (i[1] != '') and (i[1] != i[-1]):
                side = i[1]
                Sheet['spec_all'][project][side] = [] if i[2] == i[-1] else {}
            if (i[2] != '') and (i[2] == i[-1]):
                spec = i[2]
                Sheet['spec_all'][project][side] += [spec]
            if (i[2] != '') and (i[2] != i[-1]):
                spec = i[2]
                Sheet['spec_all'][project][side][spec] = [] if i[3] == i[-1] else {}
            if (i[3] != '') and (i[3] == i[-1]):
                component = i[3]
                Sheet['spec_all'][project][side][spec] += [component]
        except ZeroDivisionError:
            pass
    return Sheet

def func_Defects():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Defects!A1:A50', majorDimension='ROWS').execute()
    Sheet['defects'] = []
    for i in _['values']:
        Sheet['defects'] += [i[0]]
    return Sheet

def func_component_info():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Component_info!A2:C2000', majorDimension='ROWS').execute()
    Sheet['component_info'] = dict()
    for i in _['values']:
        Sheet['component_info'][i[0]] = i[1:]
    for i in _['values']:
        # if (len(i) < 3) or ()
        Sheet['component_info'][i[2]] = i[:2]
    return Sheet


def beginning():
    func_Access_id()
    func_Line()
    func_Teams()
    func_Break()
    func_3_5_10()
    func_Device()
    func_Spec()
    func_Defects()
    with open("data_file.json", "w", encoding='utf8') as write_file:
        json.dump(Sheet, write_file, skipkeys=False, indent=4, ensure_ascii=False)
    return

beginning()
# pprint.pprint(func_component_info())