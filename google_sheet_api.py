# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 18:10:35 2021

@author: caleb

reference : https://www.maxlist.xyz/2018/09/25/python_googlesheet_crud/
"""

import string
import pygsheets

col_list = list(string.ascii_uppercase)

# 因爲信息對應的column也是已知，所以這裏用dict記住就可以了
def message_col(wks):
    message_col = dict()
    mes_list = wks[1].range('E2:P2')[0]
    for i in range(12):
        message_col[mes_list[i].value] = col_list[4+i]

# 查看Google sheet 内sheet 清單
def get_sheet_list(sht):
    wks_list = sht.worksheets()
    return wks_list

# Initialize: gc 儲存 我們的授權金鑰 json 放置的位子。
def initialize(service_file = "key.json"):
    try:
        myfile = open(service_file, "r") # or "a+", whatever you need                            # exit the loop
    except IOError:
        input("Could not open key.json\n")
    gc = pygsheets.authorize(service_file = service_file)
    return gc

# 利用python 開啓 Google sheet
def open_google_sheet(target_gs = "https://docs.google.com/spreadsheets/d/1ohd8YRgh9ghewZaSP39W0dhPyKw_xI0kbWu_SoClw3A/edit#gid=680064596"):
    gc = initialize()
    sht = gc.open_by_url(target_gs)
    return sht

# 確認每個名字與其對應的點名格子編碼
def create_dict(message,sht):
    d_list = []
    message_col = dict()
    mes_list = sht[1].range('E2:P2')[0]

    for i in range(12):
        message_col[mes_list[i].value] = col_list[4+i]
    
    for i in range(1,len(sht.worksheets())):
        
        wks = sht[i]
        name_list = wks.get_values_batch(['B3:B'])[0][2:]
        d = dict()
        for i in range(len(name_list)):
            if len(name_list[i]) == 0:
                continue
            name = name_list[i][0]
            d[name] = message_col[message] + str(3+i)
        d_list.append(d)
    return d_list

def get_cell(target,d_list):

    # Check 100% accuracy
    for i in range(len(d_list)):
        keys = d_list[i].keys()
        for key in keys:
            if target == key:
                return i,d_list[i][key],key

    # Check >50% accuracy        
    for i in range(len(d_list)):
        keys = d_list[i].keys()
        for key in keys:
            hit = 0.0
            for k in key:
                if k in target:
                    hit = hit + 1.    
            acc = hit/len(key)
            if acc >= 0.5:
                return i,d_list[i][key],key
            
    # If not exists
    return -1,"None","None"

# 點名
def attend(tick,sht):
    wks = sht.worksheets()
    # 點名
    for i in range(len(wks)-1):
        wks_cur = wks[i+1]
        for t in tick[i]:
            wks_cur.update_value(t,'True')
        
    # Failed to find the name
    return 0



def rollcall(name_list,d,sht):
    success = []
    tick = [[],[],[],[],[],[]]
    attendees = set()
    fail = []
    for name in name_list.split():
        print(name)
        i,cell,attendee = get_cell(name,d)
        if i!=-1:
            success.append(name)
            tick[i].append(cell)
            attendees.add(attendee)
        else:
            fail.append(name)
    
    attend(tick,sht)
    
    return success,fail,attendees

def get_confirm_attendees(sht):
    wks = sht.worksheets()
    attendees = set()
    for i in range(1,len(wks)):
        wks_cur = wks[i]
        name_list = wks_cur.get_values_batch(['B3:B'])[0][2:]
        attend = wks_cur.get_values_batch(['D3:D'])[0][2:]
        for j in range(len(name_list)):
            if len(name_list[j])>0 and attend[j][0]=="TRUE":
                attendees.add(name_list[j][0])
    return attendees

if __name__ == '__main__':
    #A1 = sht[1].cell('E51')
    #sht[1].update_value('E51','True')
    sht = open_google_sheet('https://docs.google.com/spreadsheets/d/1ohd8YRgh9ghewZaSP39W0dhPyKw_xI0kbWu_SoClw3A/edit#gid=680064596') 
    name_list = get_confirm_attendees(sht)
    #print(len(sht.worksheets()))
    
    #d = create_dict("信息一",sht)
    #target = ""
    #i,cell = get_cell(target,d)
    #s,c = rollcall('静音\n謝亞城 田家樂 高苡程\n虛俊翰 恩慈高\n黃柏\n陳孜安 其恩\n黃凡芸 其恩路\n張晴雯 曾業偉\n王宏惠\nHsin 致美張\nChunyi\n得真',d,sht)