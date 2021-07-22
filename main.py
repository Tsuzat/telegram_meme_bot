import telebot
import threading
from time import sleep, time
from decouple import config
from helpers import *
from fetch_memes import send_meme

BOT_TOKEN = config("TOKEN")
BOT_INTERVAL = 1
BOT_TIMEOUT = 10

bot = None  # Keep the bot object as global variable if needed


def bot_polling():
    global bot  # Keep the bot object as global variable if needed
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(BOT_TOKEN)  # Generate new bot instance
            botactions(bot)  # If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex:  # Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else:  # Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break  # End loop


def botactions(bot):
    # Set all your bot handlers inside this function
    # If bot is used as a global variable, remove bot as an input param
    @bot.message_handler(commands=["source_code","code"])
    def code(message):
        bot.reply_to(message, "https://github.com/Tsuzat/telegram_meme_bot")

    @bot.message_handler(commands=["help"])
    def help(message):
        with open('help_text.txt','r') as f:
            text = f.read()

        bot.reply_to(message, text)

    @bot.message_handler(commands=["meme"])
    def meme(message):
        now = time() # set a start time
        subreddit, method = get_args_for_meme(message.text[6:]) #get arguments 
        data = send_meme(subreddit=subreddit, method=method)
        if data is None:
            bot.reply_to(message, "Couldn't fetch meme, please check the command")
        else:
            title = data['title']
            source = "https://www.reddit.com" + data['permalink']
            url = data['url']
            caption = f"{title}\nurl:{url}\nFrom:{source}\nfetched in: {round(time()-now,2)} sec"
            bot.send_photo(message.chat.id, url, caption)


polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()

# Keep main program running while bot runs threaded
if __name__ == "__main__":
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break
