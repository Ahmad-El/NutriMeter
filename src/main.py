import telebot
import nutritionix as nx
from telebot import types
from orm_model import Sport, Base
from psql_settings import Session, engine
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
buffer = []

bot = telebot.TeleBot(BOT_TOKEN)
menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_markup.row("food", "sport")
Base.metadata.create_all(engine)


@bot.message_handler(commands=["sport"])
def get_sport_request(message):
    text = "Enter your workout. Example:\n *30 min weight lifting*"
    send_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    buffer.append(send_msg.message_id)
    bot.register_next_step_handler(send_msg, sport_handler)


def send_message_to_tg(datas: dict, message: types.Message):
    bot.delete_messages(message.chat.id, buffer)
    buffer.clear()
    text = ""
    for data in datas:
        try:
            session = Session()
            new_event = Sport(
                name=data["Sport"],
                met=data["Metabolic equivalent of task"],
                duration_min=float(data["Duration"].split(" ")[0]),
                calories_kcal=float(data["Calories Expended"].split(" ")[0]),
                date=datetime.datetime.now(),
            )
            session.add(new_event)
            session.commit()
            session.close()
        except Exception as e:
            print(e)

        for key in data:
            text += f"*{key}*: {data[key]}\n"
        text += "   -----   \n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def sport_handler(message):
    sport = message.text
    type_api = nx.ender["sport"]
    query = {"query": sport}
    try:
        json_data = nx.get_responce(type_api, query)
        data = nx.parse_sport(json_data)
    except Exception as e:
        # print(e)
        msg_id = bot.send_message(
            message.chat.id, "*Bad input*", parse_mode="Markdown"
        ).message_id
        buffer.append(msg_id)
    else:
        send_message_to_tg(data, message)


@bot.message_handler(commands=["food"])
def get_food_request(message):
    text = "Enter a query like *1 cup mashed potatoes* or *grapes 100g* or *twix chocolate*"
    send_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    buffer.append(send_msg.message_id)
    bot.register_next_step_handler(send_msg, food_handler)


def food_handler(message):
    food = message.text
    type_api = nx.ender["food"]
    query = {"query": food}
    try:
        json_data = nx.get_responce(type_api, query)
        data = nx.parse_food(json_data)
    except Exception as e:
        # print(e)
        msg_id = bot.send_message(
            message.chat.id, "*Bad input*", parse_mode="Markdown"
        ).message_id
        buffer.append(msg_id)
    else:
        send_message_to_tg(data, message)


@bot.message_handler(commands=["start"])
def send_menu(message):
    # buffer.append(message.message_id)
    bot.send_message(
        message.chat.id, "Please choose Category", reply_markup=menu_markup
    ).message_id
    # buffer.append(msg_id)


@bot.message_handler(func=lambda message: True)
def handle_choice(message):
    # bot.delete_message(message.chat.id, message.message_id)
    buffer.append(message.message_id)
    if message.text == "food":
        get_food_request(message)
    elif message.text == "sport":
        get_sport_request(message)
    else:
        msg_id = bot.send_message(
            message.chat.id, "Invalid choice. Please use the menu."
        ).message_id
        buffer.append(msg_id)


bot.infinity_polling()
