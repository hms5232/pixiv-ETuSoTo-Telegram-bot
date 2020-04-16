#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Author：hms5232
Repo：https://gitlab.com/hms5232/pixiv-etusoto-telegram-bot
Bug or suggestion：https://gitlab.com/hms5232/pixiv-etusoto-telegram-bot/-/issues
"""


from configparser import ConfigParser
from telegram.ext import Updater, CommandHandler


# 設定一些個人的環境變數
env = ConfigParser()
env.read('config.ini')
'''
env.get('bot', 'telegram_bot_token')
env['bot']['telegram_bot_token']
'''
# If you don't want use config.ini, please edit following variables for your environment.
telegram_bot_token = env['etusoto']['telegram_bot_token']


'''
尚未執行機器人之前，可傳送訊息給機器人後至下列網址查看：

	https://api.telegram.org/bot{$token}/getUpdates
'''
updater = Updater(token=telegram_bot_token)  # 呼叫 bot 用


"""
對應指令的函數們

:param bot: 機器人預設值一定要，如果沒有給的話，你的機器人不會回覆
:param update: Telegram update資訊
"""

def welcome(bot, update):
	""" Show user welcome message. """
	
	chat_id = update.message.from_user.id
	
	about_bot = ''
	about_bot = about_bot + 'Hello! 感謝您的使用。\n'
	about_bot = about_bot + '相信不用我多說，請低調。\n'
	about_bot = about_bot + '若使用者使用不當導致任何紛爭，**與作者一概無關**！\n'
	about_bot = about_bot + '**如無法接受請立即停止機器人！**\n'
	
	bot.send_message(chat_id, about_bot, parse_mode='Markdown')


def show_user_info(bot, update):
	""" 回覆使用者的資訊 """
	
	user_info = ''
	user_info = user_info + '發送人 first name：{}\n'.format(update.message.from_user.first_name)
	user_info = user_info + '發送人 last name：{}\n'.format(update.message.from_user.last_name)
	user_info = user_info + '發送人 full name：{}\n'.format(update.message.from_user.full_name)
	user_info = user_info + '發送人 username：{}\n'.format(update.message.from_user.username)
	user_info = user_info + '發送人 id：{}\n'.format(update.message.from_user.id)
	user_info = user_info + 'message_id：{}\n'.format(update.message.message_id)
	user_info = user_info + '所在的聊天室 id：{}\n'.format(update.message.chat.id)
	user_info = user_info + '所在的聊天室 type：{}\n'.format(update.message.chat.type)
	user_info = user_info + '訊息內容：{}\n'.format(update.message.text)
	
	update.message.reply_text(user_info, disable_notification="True")


def hello(bot, update):
	""" Hello World! """
	
	# 兩種方法傳送訊息予使用者
	update.message.reply_text('Hello world!')  #方法一
	bot.sendMessage(update.message.from_user.id, 'Welcome to Telegram!')  # 方法二
	"""
		方法二的 sendMessage 是 send_message 的別名
		以 python 的使用習慣，應該是後者較為符合
		https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.send_message
	"""


"""
處理機器人指令（以「/」開頭的訊息）

格式可簡化為：
	CommandHandler('指令', 要執行的函數)
其中使用者輸入「/指令」
"""
# CommandHandler('指令', 要執行的函數)，使用者輸入「/指令」
updater.dispatcher.add_handler(CommandHandler(['start', 'about'], welcome))  # 歡迎訊息 / 機器人資訊
updater.dispatcher.add_handler(CommandHandler('info', show_user_info))  # 顯示使用者資訊
updater.dispatcher.add_handler(CommandHandler(['hello', 'hi'], hello))  # Hello World!


# 執行機器人必須要的，讓機器人運作聽命
updater.start_polling()
updater.idle()
