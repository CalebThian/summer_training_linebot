from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message,send_image_message

from linebot.models import MessageTemplateAction

from google_sheet_api import rollcall,open_google_sheet

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.is_rollcalling_flag = False
    
    def is_going_to_echo(self,event):
        text=event.message.text
        if "點名" in text:
            return False
        return True
    
    def on_enter_echo(self,event):
        reply_token = event.reply_token
        text = "阿門"
        send_text_message(reply_token,text)
        self.go_back()
    
    def is_going_to_class(self,event):
        text=event.message.text
        if "點名" in text:
            return True
        
    def on_enter_class(self,event):
        reply_token = event.reply_token
        text = "請問是夜間班還是周末班？夜間班請輸入‘1’,周末班請輸入'2'"
        send_text_message(reply_token,text)
        
    def is_going_to_mes(self,event):
        text=event.message.text
        if text=='1' or text == '2':
            if text == '1':
                gs = 'https://docs.google.com/spreadsheets/d/1ohd8YRgh9ghewZaSP39W0dhPyKw_xI0kbWu_SoClw3A/edit#gid=680064596'
            elif text == '2':
                gs = 'https://docs.google.com/spreadsheets/d/1ohd8YRgh9ghewZaSP39W0dhPyKw_xI0kbWu_SoClw3A/edit#gid=680064596'
            global sht
            sht = open_google_sheet(gs)
            return True
        
    def on_enter_mes(self,event):
        reply_token = event.reply_token
        text = "請告訴我這是第幾篇信息？（如：“信息一”）"
        send_text_message(reply_token,text) 
        
    def is_going_to_rollcall(self,event):
        text=event.message.text
        mes = ['信息一',
               '信息二',
               '信息三',
               '信息四',
               '信息五',
               '信息六',
               '信息七',
               '信息八',
               '信息九',
               '信息十',
               '信息十一',
               '信息十二']
        global message
        for mes_name in mes:
            for m in mes_name:
                print(m,mes_name)
                if m in text:
                    message = m
                    return True
        
    def on_enter_rollcall(self,event):
        reply_token = event.reply_token
        if not self.is_rollcalling_flag:
            text = "好的，可以開始點名咯"
            self.is_rollcalling_flag = True
            send_text_message(reply_token,text) 
        elif self.is_rollcalling_flag:
            success,fail = rollcall(event.message.text,message,sht)    
            text = "成功點名的有:\n"
            for name in success:
                text = text + name + "\n"
            text = text + "共" + str(len(success))+"人\n"
            
            text = text + "沒認出是誰的有:\n"
            for name in fail:
                text = text + name + "\n"
            text = text + "共" + str(len(fail))+"人\n"
            send_text_message(reply_token,text)
        
    def is_rollcalling(self,event):
        text=event.message.text
        self.is_rollcalling_flag = True
        if "完成點名" != text:
            return True
    
    