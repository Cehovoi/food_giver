import telebot
import shelve
import transitions
from fsm import Consumer


bot = telebot.TeleBot('5012439687:AAEjQ94WLZU6xccEzxKWYV6rmPxbY17uF0g')
fuse = ' Учтите вы только что уже заказали %s, не обкушайтесь! '

@bot.message_handler(commands=['start', 'stop'])
def start(message):
    id_db=str(message.from_user.id)
    name = message.from_user.first_name
    db = shelve.open('customers')
    db[id_db] = Consumer(id_db, name)
    bot.send_message(message.chat.id, db[id_db].state)
    db.close()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    id = message.from_user.id
    id_db=str(id)
    db = shelve.open('customers')
    client = db[id_db]
    try:
        trigger = getattr(client, message.text)
        trigger()
        db[id_db] = client
        answer = client.state
        if client.ordered_pizza and client.switch:
            answer = answer + fuse % client.ordered_pizza + ' Ещё?'
            client.switch = 0
            db[id_db] = client
        db.close()
        bot.send_message(id, "%s" % answer)
    except(AttributeError, transitions.core.MachineError):
        step = client.machine.get_triggers(client.state)[-1]
        if 'to_' in step:
            bot.send_message(id, client.state)
        else:
            bot.send_message(id, "Хошь не хошь, а надо написать - %s" % step)


bot.polling(none_stop=True, interval=0)