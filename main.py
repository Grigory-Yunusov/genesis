import telebot
import sqlite3

name = None

bot = telebot.TeleBot("6665963815:AAFF3zSCU9oSLFuju2xa9HwXj7ccrn4a030")





@bot.message_handler(commands=['hello'])
def main(message):
    bot.send_message(message.chat.id, f"How can I help you, {message.from_user.first_name}?")




@bot.message_handler(commands=['info'])
def main(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('genesis_base.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), phone varchar(12))')
    conn.commit()
    cur.close()
    conn.close()


    bot.send_message(message.chat.id, "add name")
    bot.register_next_step_handler(message, user_name)



def user_name(message):
    global name 
    name = message.text.strip()
    bot.send_message(message.chat.id, "add phone")
    bot.register_next_step_handler(message, user_phone)

def user_phone(message): 
    tel = message.text.strip()
    conn = sqlite3.connect('genesis_base.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, phone) VALUES ("%s", "%s")' % (name, tel))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('show all', callback_data='users'))
    bot.send_message(message.chat.id, "you are registered!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('genesis_base.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    info = ""
    for el in users:
        info += f"Name: {el[1]}, Phone: {el[2]}\n"

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)



@bot.message_handler(commands=['change'])
def change(message):
    conn = sqlite3.connect('genesis_base.sql')
    cur = conn.cursor()

    cur.execute('UPDATE users SET phone = ? WHERE name = ?', (6, f"{user_name}"))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, "write name")
    bot.send_message(message.chat.id, user_name)
    bot.send_message(message.chat.id, "change phone")
    bot.register_next_step_handler(message, user_phone)
def change_phone(message):
    global name
    name = message.text.strip()
    # bot.send_message(message.chat.id, "change phone")
    # bot.register_next_step_handler(message, user_phone)









@bot.message_handler()
def info(message):
    if message.text.lower() == 'hi':
        bot.send_message(message.chat.id, f"How can I help you, {message.from_user.first_name}?")
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
















bot.polling(none_stop=True)

