from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message,send_image_message

from linebot.models import MessageTemplateAction

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def is_going_to_echo(self,event):
        text=event.message.text
        return True
    
    def on_enter_echo(self,event):
        reply_token = event.reply_token
        text = event.message.text
        send_text_message(reply_token,text)
        self.go_back()
    
