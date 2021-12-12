import telebot
bot = telebot.TeleBot('5012439687:AAEjQ94WLZU6xccEzxKWYV6rmPxbY17uF0g')
from fsm import Consumer


process = {}
fuse = ' Учтите вы уже заказали %s, не обкушайтесь!'

@bot.message_handler(commands=['start', 'stop'])
def start(message):
    id=message.from_user.id
    name = message.from_user.first_name
    process[id] = Consumer(id, name)
    bot.send_message(message.chat.id, process[id].state)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    id = message.from_user.id
    global process
    client = process[id]
    try:
        trigger = getattr(client, message.text)
        trigger()
        process[id] = client
        addition = ''
        if client.ordered_pizza and client.switch:
            addition = fuse % client.ordered_pizza
            client.switch = 0
        bot.send_message(id, ("%s" % client.state) + addition)
    except(Exception):
        step = client.machine.get_triggers(client.state)[-1]
        bot.send_message(id, "Хошь не хошь, а надо написать - %s" % step)


bot.polling(none_stop=True, interval=0)