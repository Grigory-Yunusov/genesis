import telebot
from telebot import types
import sqlite3



bot = telebot.TeleBot("6665963815:AAFF3zSCU9oSLFuju2xa9HwXj7ccrn4a030")





@bot.message_handler(commands=['hello'])
def main(message):
    bot.send_message(message.chat.id, f"How can I help you, {message.from_user.first_name}?")




@bot.message_handler(commands=['info'])
def main(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('data_base.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_ment primary key, name varchar(50), phone varchar(12)')
    conn.commit()
    cur.close()
    conn.close()


    bot.send_message(message.chat.id, "add name")
    bot.register_next_step_handler(message, user_name)



def user_name(message):
    pass

@bot.message_handler()
def info(message):
    if message.text.lower() == 'hi':
        bot.send_message(message.chat.id, f"How can I help you, {message.from_user.first_name}?")
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')















bot.polling(none_stop=True)

