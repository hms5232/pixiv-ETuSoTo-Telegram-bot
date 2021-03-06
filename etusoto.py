#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Author：hms5232
Repo：https://gitlab.com/hms5232/pixiv-etusoto-telegram-bot
Bug or suggestion：https://gitlab.com/hms5232/pixiv-etusoto-telegram-bot/-/issues
"""


import os
from configparser import ConfigParser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


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


def init():
	""" initial """
	if not os.path.exists('./images_wait_for_search/'):
		os.makedirs('./images_wait_for_search/')
		print('Create image folder')


def proxy_search(image_path):
	""" proxy image for searching """
	
	with open(image_path, 'rb') as image_file:
		image_to_search = {'file': image_file}
		data_to_post = {'database': '5'}  # pixiv Images
		r = requests.post('https://saucenao.com/search.php', files = image_to_search, data = data_to_post)
		# parsing and return
		if r.status_code != 200:
			print("Request failed!")
			return dict(err = "搜尋好像出錯了")
		soup = BeautifulSoup(r.text, 'html.parser')
		result_table = soup.find('div', {'id':"middle"}).find('table')
		relink = result_table.find('div', class_='resultcontentcolumn').find_all("a", class_="linkify")  # 作品和作者的連結
	
	# 看回傳的結果是否為p站的
	if relink[0].get('href').find('pixiv.net') != -1:
		result = dict(similarity = result_table.find('div', class_='resultsimilarityinfo').string.strip(),  # 相似度
					  title = result_table.find('div', class_='resulttitle').find('strong').string.strip(),  # 作品名稱
					  artwork_id = relink[0].string.strip(),  # Pivix ID
					  artwork_url = relink[0].get('href'),  # Pivix URL
					  author = relink[1].string.strip(),  # 作者
					  author_link = relink[1].get('href')  # 作者連結
					)
	else:
		result = dict()
	
	return result


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
	about_bot = about_bot + '相信不用我多說，請低調🤫。\n'
	about_bot = about_bot + '若使用者使用不當導致任何紛爭，*與作者一概無關*！\n'
	about_bot = about_bot + '*如無法接受請立即停止機器人！*\n'
	about_bot = about_bot + '可透過傳送 `/help` 重新查看使用教學和注意事項\n'
	
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


def help(bot, update):
	""" user call for help """
	manual = ""
	if update.message.chat.type == 'private':
		manual = manual + "直接傳送圖片給小天使，👼會去以圖搜圖🔍。請注意以下幾點：\n"
		manual = manual + "⚠ 一則訊息只傳送一張1⃣圖片（Forward 亦可👌）\n"
		manual = manual + "⚠ 請使用圖片🖼而非檔案❌的方式傳送\n"
		manual = manual + "\n如果想用在*群組👥*或搜尋之前搜尋過的圖，\n"

	manual = manual + "請使用機器人指令 `/search` 「*回覆*」（*reply*）欲搜尋的圖片訊息，\n"
	manual = manual + "小天使就會去回覆的訊息以圖搜圖看看 p 站有沒有🕵\n"
	manual = manual + "最後回傳最可能的結果。"
	
	update.message.reply_text(manual, parse_mode='Markdown')


def format_result(bot, update, image_path):
	""" Get image which user upload, search and return result. """
	
	# search
	result_dict = proxy_search(image_path)

	result = ""
	# 看回傳的結果是否為p站的
	if 'err' in result_dict:
		bot.send_message(update.message.chat_id, result_dict['err'], reply_to_message_id = update.message.message_id)
	elif len(result_dict) > 0:
		result += "符合度：{}\n\n".format(result_dict['similarity'])
		result += "`" + result_dict['title'] + "`\n"  # 作品名
		result += "Pixiv ID: [{}]({})\n".format(result_dict['artwork_id'], result_dict['artwork_url'])
		result += "作者：[{}]({})\n".format(result_dict['author'], result_dict['author_link'])
		inline_keyboard_btn = InlineKeyboardMarkup([[
				InlineKeyboardButton('查看作者 🧑‍🎨', url = result_dict['author_link']),
				InlineKeyboardButton('看作品 🖼', url = result_dict['artwork_url'])
			]])
	else:
		result += "在p站上查無結果"
		inline_keyboard_btn = None
	
	bot.send_message(update.message.chat_id, result, 
					 reply_to_message_id = update.message.message_id, 
					 parse_mode = 'Markdown',
					 reply_markup = inline_keyboard_btn
					)
	
	# delete image
	try:
		os.remove(image_path)
	except OSError as ose:
		print(ose)
	else:
		pass


def donate(bot, update):
	""" donate to author """
	
	donate_info = ''
	donate_info += '感謝您點選此指令查看贊助資訊☕，如果您願意贊助🍦的話，我會很開心🚀。\n'
	donate_info += '網址如下👇：\n'
	donate_info += 'https://ko-fi.com/hms5232'
	
	bot.send_message(update.message.from_user.id, donate_info,
					 reply_markup = InlineKeyboardMarkup([[
						InlineKeyboardButton('包紅包 🧧 點這裡', url = 'https://ko-fi.com/hms5232')
					 ]]))


def repo(bot, update):
	""" repository """
	
	repo_info = ''
	repo_info += '本專案開源於 Gitlab 上，\n'
	repo_info += '歡迎大家給予機器人專案各種回饋，\n'
	repo_info += '單純的標星星⭐也非常歡迎！\n'
	repo_info += '\n網址如下👇：\n'
	repo_info += 'https://gitlab.com/hms5232/pixiv-etusoto-telegram-bot'
	
	bot.send_message(update.message.from_user.id, repo_info)


def get_img(bot, update, is_reply = False):
	""" get image from telegram """
	
	image_path = os.path.join("images_wait_for_search", "{}_{}".format(update.message.chat_id, update.message.message_id))
	if is_reply:
		update.message.reply_to_message.photo[-1].get_file().download(custom_path = image_path)
	else:
		update.message.photo[-1].get_file().download(custom_path = image_path)  # download image
	
	return format_result(bot, update, image_path)


def manual_search(bot, update):
	""" manual search in group """
	
	# 檢查有沒有 reply 訊息
	if update.message.reply_to_message:
		# 檢查 reply 對象有沒有圖
		if update.message.reply_to_message.photo:
			return get_img(bot, update, True)
		else:
			update.message.reply_text("所回覆之訊息無發現圖片", disable_notification="True")
	else:
		update.message.reply_text("請用「回覆」方式指定欲搜尋的圖片", disable_notification="True")


# Initial
init()


"""
處理機器人指令（以「/」開頭的訊息）

格式可簡化為：
	CommandHandler('指令', 要執行的函數)
其中使用者輸入「/指令」
"""
# CommandHandler('指令', 要執行的函數)，使用者輸入「/指令」
updater.dispatcher.add_handler(CommandHandler(['start', 'about'], welcome))  # 歡迎訊息 / 機器人資訊
updater.dispatcher.add_handler(CommandHandler('info', show_user_info))  # 顯示使用者資訊
updater.dispatcher.add_handler(CommandHandler(['help', 'man'], help))  # 你今天 hh 了嗎
updater.dispatcher.add_handler(CommandHandler(['donate', 'present'], donate))  # 有人要斗內了嗚嗚
updater.dispatcher.add_handler(CommandHandler(['contribute', 'code'], repo))  # 歡迎標星星
updater.dispatcher.add_handler(CommandHandler(['search'], manual_search))  # 指定搜尋「被回覆」的訊息圖片

updater.dispatcher.add_handler(MessageHandler(Filters.photo, get_img))


# 執行機器人必須要的，讓機器人運作聽命
updater.start_polling()
updater.idle()
