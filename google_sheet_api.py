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
    gc = pygsheets.authorize(service_file = service_file)
    return gc

# 利用python 開啓 Google sheet
def open_google_sheet(target_gs = "https://docs.google.com/spreadsheets/d/1ohd8YRgh9ghewZaSP39W0dhPyKw_xI0kbWu_SoClw3A/edit#gid=680064596"):
    gc = initialize()
    sht = gc.open_by_url(target_gs)
    return sht

# 點名
def attend(name,message,target_gs = None):
    if target_gs:
        sht = open_google_sheet(target_gs = target_gs)
    else:
        sht = open_google_sheet()
    wks = sht.worksheets()
    col_list = list(string.ascii_uppercase)
    item_row = 2
    
    # 找到姓名的cell，假設每一個worksheet都是一樣的位置
    # 假設從第二頁開始查
    # 因爲已知都在‘B’，所以爲了節省時間就不搜尋了
    name_col = 'B'
    '''
    wks_cur = wks[1]
    for alpha in col_list:
        cell = alpha+item_row
        if wks_cur.cell(cell).value == "姓名":
            name_col = alpha
            break
    '''
    # 找對應格子， 設爲True
    # 因爲信息對應的column也是已知，所以這裏用dict記住就可以了
    message_col = dict()
    mes_list = wks[1].range('E2:P2')[0]
    for i in range(12):
        message_col[mes_list[i].value] = col_list[4+i]

        
    for i in range(1,len(wks)):
        wks_cur = wks[i]
        ite = 3
        while True:
            if wks_cur.cell(name_col + str(ite)).value == name:
                wks_cur.update_value(message_col[message] + str(ite),'True')
                return
            elif wks_cur.cell(name_col + str(ite)).value == "":
                break
            else:
                ite = ite+1


if __name__ == '__main__':
    #A1 = sht[1].cell('E51')
    #sht[1].update_value('E51','True')
    attend('田家樂','信息二')