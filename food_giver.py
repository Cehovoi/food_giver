#!/usr/bin/env python3
import click
import telebot
from pizza_bot import Bot as PizzaBot



@click.command()
@click.option('--token', envvar="TOKEN", help='Telegram Token')
def main(token):
    bot = telebot.TeleBot(token, parse_mode=None)
    pizza_bot = PizzaBot()
    offset = None
    while True:
        for message in bot.get_updates(offset=offset):
            try:
                offset = message.update_id + 1
                response = pizza_bot.handle(message.message.chat.id, message.message.text)
                print(response)
                bot.send_message(message.message.chat.id, response)
            except Exception as e:
                pass

if __name__ == '__main__':
    main()
