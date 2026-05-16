from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from Script import script
import asyncio
import sys
import os

START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT 
ABOUT_TXT = script.ABOUT_TXT

@Client.on_message(filters.command("start") & filters.private)
async def start(bot, cmd):
	await cmd.reply_text(
		START_TXT.format(cmd.from_user.first_name), 
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("🔮помощь", callback_data='help_cb'),
					InlineKeyboardButton("⚔что это такое", callback_data='about_cb')
				],
				[
					InlineKeyboardButton("👨🏼‍💻Разраб", url='https://t.me/WerhesDev')
				]
			]
		)
	)
    
  
@Client.on_message(filters.command("help") & filters.private)
async def help(bot, cmd):	
	await cmd.reply_text(
		HELP_TXT, 
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("⚔что это такое", callback_data='about_cb'),
					InlineKeyboardButton("⚡назад", callback_data='start_cb')
				],
				[
					InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
					InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
				]
			]
		)
	)
    
@Client.on_message(filters.command("about") & filters.private)
async def about(bot, cmd):	
	await cmd.reply_text(
		ABOUT_TXT, 
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("🔮помогите", callback_data='help_cb'),
					InlineKeyboardButton("⚡назад", callback_data='start_cb')
				],
				[
					InlineKeyboardButton("👨🏼‍💻Разраб", url='https://t.me/WerhesDev')
				]
			]
		)
	)
