from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message,send_image_message

from linebot.models import MessageTemplateAction

from google_sheet_api import rollcall,open_google_sheet,create_dict,get_confirm_attendees

class TocMachine(GraphMachine):
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.init()
        
    def init(self):
        self.is_rollcalling_flag = False
        self.sht = None
        self.d = None
        self.attendees = set()
        self.confirm_attendees = set()
        
    def is_going_to_end(self,event):
        text=event.message.text
        if text == "中斷點名":
            return True
    
    def on_enter_end(self,event):
        reply_token = event.reply_token
        text = "已中斷點名"
        send_text_message(reply_token,text)
        self.go_back()
        
    def is_going_to_greetings(self,event):
        text=event.message.text
        if "打招呼" in text:
            return True
    
    def on_enter_greetings(self,event):
        reply_token = event.reply_token
        text = "弟兄姊妹們平安喜樂，我是這次協助大家點名的機器人小夏！\n\n只要輸入“點名”，我就會開始協助弟兄姊妹點名哦！請按著指示與教學進行點名！\n\n願弟兄姊妹能更進入這次夏季訓練的信息！"
        send_text_message(reply_token,text)
        self.go_back()
    
    def is_going_to_class(self,event):
        text=event.message.text
        if text == "點名":
            return True
        
    def on_enter_class(self,event):
        reply_token = event.reply_token
        text = "請問是夜間班還是周末班？夜間班請輸入‘1’,周末班請輸入'2'"
        send_text_message(reply_token,text)
        
    def is_going_to_mes(self,event):
        text=event.message.text
        if text=='1' or text == '2' or text == '3':
            if text == '1':
                gs = 'https://docs.google.com/spreadsheets/d/1z735DZS2StVi9jKFGtxpdBYlP41RGYV9aM1ikFUkc08/edit#gid=680064596'
            elif text == '2':
                gs = 'https://docs.google.com/spreadsheets/d/1FezG1Io3rTJLtkJNBIL9LVNbTVCma8iwJWxjRUWHZ9E/edit#gid=680064596'
            elif text == '3':
                gs = 'https://docs.google.com/spreadsheets/d/1ohd8YRgh9ghewZaSP39W0dhPyKw_xI0kbWu_SoClw3A/edit#gid=680064596'
            self.sht = open_google_sheet(gs)
            return True
        
    def on_enter_mes(self,event):
        reply_token = event.reply_token
        text = "請問這是第幾篇信息呢？（如：“信息一”）"
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
        for mes_name in mes:
            if mes_name in text:
                message = mes_name
                print("If success:")
                self.d = create_dict(message,self.sht)
                print("Success!")
                return True
        
    def on_enter_rollcall(self,event):
        reply_token = event.reply_token
        print("flag = " + str(self.is_rollcalling_flag))
        if not self.is_rollcalling_flag:
            text = "好的，可以開始點名咯"
            self.is_rollcalling_flag = True
            send_text_message(reply_token,text) 
        elif self.is_rollcalling_flag:
            success,fail,maybe_success,attendees_cur = rollcall(event.message.text,self.d,self.sht)
            self.attendees = self.attendees | attendees_cur
            text = "成功點名的有:\n"
            for name in success:
                text = text + name + "\n"
            text = text + "共" + str(len(success))+"人\n\n"
            
            text = text + "可能點錯的有:\n"
            for pair in maybe_success:
                text = text + "\"" + pair[0] + "\" 我認爲是 \"" + pair[1] +"\"\n"
            text = text + "共" + str(len(maybe_success)) +"人\n\n"
            
            text = text + "沒認出是誰的有:\n"
            for name in fail:
                text = text + name + "\n"
            text = text + "共" + str(len(fail))+"人\n"
            send_text_message(reply_token,text)
        
    def is_rollcalling(self,event):
        if event.message.type == "text":
            text=event.message.text
            self.is_rollcalling_flag = True
            if "完成點名" != text:
                return True
    
    def is_going_to_finish(self,event):
        if event.message.type == "text":
            text=event.message.text
            self.is_rollcalling_flag = True
            if "完成點名" in text:
                return True
            
    def on_enter_finish(self,event):
        reply_token = event.reply_token
        self.confirm_attendees = get_confirm_attendees(self.sht)
        text = "目前點到人數為"+str(len(self.attendees))+"\n未到會人位為：\n"
        no_attend = self.confirm_attendees - self.attendees
        for name in no_attend:
            text = text + name + "\n"
        text = text + "共" + str(len(no_attend))
        send_text_message(reply_token,text)
    
        # Initialize for next rollcall
        self.init()
        self.go_back()
        