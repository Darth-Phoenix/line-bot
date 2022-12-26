import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from linebot.models import MessageAction, TemplateSendMessage, ButtonsTemplate


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_menu(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
        [
            TextSendMessage(text=text),
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='功能選單',
                    text='今晚，你想來點...',
                    thumbnail_image_url='https://i.imgur.com/BWO4igP.jpeg',
                    actions=[
                        MessageAction(
                            label='猜拳',
                            text='猜拳'
                        ),
                        MessageAction(
                            label='猜數字',
                            text='猜數字'
                        ),
                        MessageAction(
                            label='隨機產生器',
                            text='隨機產生器'
                        ),
                        MessageAction(
                            label='看我的FSM',
                            text='聽話，讓我看看!'
                        )
                    ]
                )
            )
        ]
    )

def send_rock_paper_scissors(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
        [
            TextSendMessage(text=text), 
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='猜拳',
                    text='你要出什麼呢?',
                    actions=[
                        MessageAction(
                            label='剪刀',
                            text='剪刀'
                        ),
                        MessageAction(
                            label='石頭',
                            text='石頭'
                        ),
                        MessageAction(
                            label='布',
                            text='布'
                        ),
                        MessageAction(
                            label='退出',
                            text='林北不玩了'
                        )
                    ]
                )
            )
        ]
    )

def send_guess_number(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
        [
            TextSendMessage(text=text), 
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='猜數字',
                    text='來猜猜看我的數字啊',
                    actions=[
                        MessageAction(
                            label='開始遊戲',
                            text='讓我來猜你的數字'
                        ),
                        MessageAction(
                            label='結果統計',
                            text='我表現得如何'
                        ),
                        MessageAction(
                            label='退出',
                            text='林北不玩了'
                        )
                    ]
                )
            )
        ]
    )

def send_random_generator(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
        [
            TextSendMessage(text=text), 
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='隨機產生器',
                    text='當遇到選擇障礙時的好幫手',
                    actions=[
                        MessageAction(
                            label='開始產生',
                            text='開始產生'
                        ),
                        MessageAction(
                            label='編輯選項',
                            text='編輯選項'
                        ),
                        MessageAction(
                            label='檢視選項',
                            text='檢視選項'
                        ),
                        MessageAction(
                            label='退出',
                            text='林北不玩了'
                        )
                    ]
                )
            )
        ]
    )

def send_edit_list(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
        [
            TextSendMessage(text=text), 
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title = '編輯選項',
                    text = '顧名思義，新增或刪除選項',
                    actions=[
                        MessageAction(
                            label='新增選項',
                            text='新增選項'
                        ),
                        MessageAction(
                            label='刪除選項',
                            text='刪除選項'
                        ),
                        MessageAction(
                            label='檢視選項',
                            text='檢視選項'
                        ),
                        MessageAction(
                            label='上一頁',
                            text='結束'
                        )
                    ]
                )
            )
        ]
    )

def send_fsm_image(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/LASOGdd.png',
            preview_image_url='https://i.imgur.com/LASOGdd.png'
        )
    line_bot_api.reply_message(reply_token, image_message)

