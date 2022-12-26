import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_menu

load_dotenv()


machine = TocMachine(
    states=["menu", "rock_paper_scissors", "guess_number_menu", "play_guess_number", "random_generator", "edit_list", "add_list", "remove_list", "generate", "fsm_image"],
    transitions=[
        {"trigger": "advance", "source": "menu", "dest": "rock_paper_scissors", "conditions": "is_going_rock_paper_scissors"},
        {"trigger": "advance", "source": "rock_paper_scissors", "dest": "rock_paper_scissors", "conditions": "is_playing_rock_paper_scissors"},
        {"trigger": "advance", "source": "menu", "dest": "guess_number_menu", "conditions": "is_going_guess_number"},
        {"trigger": "advance", "source": "guess_number_menu", "dest": "guess_number_menu", "conditions": "is_in_guess_number_menu"},
        {"trigger": "advance", "source": "guess_number_menu", "dest": "play_guess_number", "conditions": "is_playing_guess_number"},
        {"trigger": "advance", "source": "play_guess_number", "dest": "play_guess_number", "conditions": "is_guessing_number"},
        {"trigger": "advance", "source": "play_guess_number", "dest": "guess_number_menu", "conditions": "leave_guessing_number"},
        {"trigger": "advance", "source": "menu", "dest": "random_generator", "conditions": "is_going_random_generator"},
        {"trigger": "advance", "source": "random_generator", "dest": "edit_list", "conditions": "enter_editing_list"},
        {"trigger": "advance", "source": "edit_list", "dest": "edit_list", "conditions": "is_editing_list"},
        {"trigger": "advance", "source": "edit_list", "dest": "add_list", "conditions": "enter_adding_list"},
        {"trigger": "advance", "source": "add_list", "dest": "add_list", "conditions": "is_adding_list"},
        {"trigger": "advance", "source": "edit_list", "dest": "remove_list", "conditions": "enter_removing_list"},
        {"trigger": "advance", "source": "remove_list", "dest": "remove_list", "conditions": "is_removing_list"},
        {"trigger": "advance", "source": "random_generator", "dest": "generate", "conditions": "enter_generate"},
        {"trigger": "advance", "source": "generate", "dest": "generate", "conditions": "is_generating"},    
        {"trigger": "advance", "source": ["add_list", "remove_list"], "dest": "edit_list", "conditions": "finish_edit"},
        {"trigger": "advance", "source": "random_generator", "dest": "random_generator", "conditions": "is_in_random_menu"},
        {"trigger": "advance", "source": ["generate", "edit_list"], "dest": "random_generator", "conditions": "back_to_random_menu"},
        {"trigger": "advance", "source": "menu", "dest": "fsm_image", "conditions": "is_show_fsm"},
        {"trigger": "go_back", "source": "fsm_image", "dest": "menu"},
        {"trigger": "advance", "source": ["rock_paper_scissors", "guess_number_menu", "random_generator"], "dest": "menu", "conditions": "is_leaving"},
    ],
    initial="menu",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_menu(event.reply_token, "你好，請問需要什麼幫忙嗎?")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
