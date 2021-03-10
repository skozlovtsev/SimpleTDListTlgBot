import telebot
import settings
import datetime
from my_json import MyJsonWorks
from funcs.format_output import format_output


bot = telebot.TeleBot(settings.token)
json = MyJsonWorks("todolist.json")


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('show list')
    bot.send_message(message.chat.id, 'hi ' + message.chat.first_name + ', you can write end controll your plans', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def show_response_list_message(message):
    if message.text.split(sep=" ", maxsplit=2)[0] == "add":
        json.add(format_output(message.text.split(sep=" ", maxsplit=2)[1:2],message.text.split(sep=" ", maxsplit=2)[2:3], str(datetime.datetime.now())[0:10], "active"))
        settings.to_do_list = json()
    if message.text == 'show list':
        markup = telebot.types.InlineKeyboardMarkup()
        for i in range(len(json())):
            markup.add(telebot.types.InlineKeyboardButton(text=[*json()][i], callback_data=[*json()][i]))
        bot.send_message(message.chat.id, "your to do lists", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data.split(sep=" ", maxsplit=1)[0] == 'delete':
        json.delete(call.data.split(sep=" ", maxsplit=1)[1])
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="delete", callback_data='delete' + ' ' + call.data))
        string = "{} {}\n\n{}\n{}".format(call.data, json()[call.data][1], json()[call.data][0], json()[call.data][2])
        bot.send_message(call.message.chat.id, string, reply_markup=markup)


bot.polling()
