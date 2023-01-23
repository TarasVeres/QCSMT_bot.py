 # coding=utf-8
import json
from work_data import Chat_hum, Chat_skl

from Parsing import beginning

def checker():
    with open('data_file.json', 'r', encoding='utf8') as read_file:
        Sheet = json.load(read_file)
    return Sheet

def update_sheet():
    beginning()
    with open('data_file.json', 'r', encoding='utf8') as read_file:
        Sheet = json.load(read_file)
    return Sheet

def skl_hum(c_id, data):
    if 'HUM' in c_id['id_loca']:
        return data
    else:
        data = data + '_skl'
        return data

def write_skl_hum(c_id):
    if 'HUM' in c_id['id_loca']:
        return 'Print'
    else:
        return 'Print_SKL'

def ve_chat_skl(c_id):
    if 'HUM' in c_id['id_loca']:
        return Chat_hum
    else:
        return Chat_skl

