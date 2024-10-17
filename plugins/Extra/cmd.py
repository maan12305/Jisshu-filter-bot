import pytz
import re
import logging
import asyncio
import datetime, time
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from datetime import timedelta, date, datetime
from utils import temp
from info import DATABASE_URI, DATABASE_NAME, ADMINS

logger = logging.getLogger(name)
logger.setLevel(logging.ERROR)

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
totalverified = db["total_verified"]

async def count_verifications():
    try:
        y = await totalverified.find_one({
            "TOTAL_VERIFIED": "ANSH"
        })
        logging.info(y)
        return y
    except Exception as e:
        logging.exception(f"Error counting: {e}")
        return

@Client.on_message(filters.command('verified') & (filters.user(ADMINS) | filters.user(ADMINS)))
async def total_verifications_today(client, message):
    try:
        v = await count_verifications()
        if not v:
            await message.reply('Some error.')
            return
        today = v.get('verified_count_today')
        yesterday = v.get('verified_count_yesterday')
        year = v.get('this_year')
        month = v.get('this_month')
        last_month = v.get('last_month_count') 
        # Create buttons
        buttons = [
            [
                InlineKeyboardButton("ᴛᴏᴅᴀʏ", callback_data="button1"),
                InlineKeyboardButton(f"{today}", callback_data="button2")
            ],
            [
                InlineKeyboardButton("ʏᴇsᴛᴇʀᴅᴀʏ", callback_data="button3"),
                InlineKeyboardButton(f"{yesterday}", callback_data="button4")
            ],
            [
                InlineKeyboardButton("ᴛʜɪs ᴍᴏɴᴛʜ", callback_data="yeanr"),
                InlineKeyboardButton(f"{month}", callback_data="ynear")
            ],
            [
                InlineKeyboardButton("ʟᴀsᴛ ᴍᴏɴᴛʜ", callback_data="yeanr"),
                InlineKeyboardButton(f"{last_month}", callback_data="ynear")
            ],
            [
                InlineKeyboardButton("ᴛʜɪs ʏᴇᴀʀ", callback_data="yearn"),
                InlineKeyboardButton(f"{year}", callback_data="yenjar")
            ],
            [
                InlineKeyboardButton("♻️ ʀᴇҒʀᴇSʜ", callback_data="rfsh")
            ]
        ]
        
        # Create inline keyboard markup
        keyboard = InlineKeyboardMarkup(buttons)
        
        await message.reply_text(f"ᴛᴏᴛᴀʟ ᴠᴇʀɪҒɪᴇᴅ ᴜsᴇʀs ✨", reply_markup=keyboard)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
        
        
@Client.on_callback_query(filters.regex("rfsh")) 
async def refrsh_data(client, query):
    try:
        v = await count_verifications()
        if not v:
            await query.answer('Some error, check logs!', show_alert=True)
            return
        today = v.get('verified_count_today')
        yesterday = v.get('verified_count_yesterday')
        year = v.get('this_year')
        month = v.get('this_month')
        last_month = v.get('last_month_count') 
        # Create buttons
        buttons = [
            [
                InlineKeyboardButton("ᴛᴏᴅᴀʏ", callback_data="button1"),
                InlineKeyboardButton(f"{today}", callback_data="button2")
            ],
            [
                InlineKeyboardButton("ʏᴇsᴛᴇʀᴅᴀʏ", callback_data="button3"),
                InlineKeyboardButton(f"{yesterday}", callback_data="button4")
            ],
            [
                InlineKeyboardButton("ᴛʜɪs ᴍᴏɴᴛʜ", callback_data="yeanr"),
                InlineKeyboardButton(f"{month}", callback_data="ynear")
            ],
            [
                InlineKeyboardButton("ʟᴀsᴛ ᴍᴏɴᴛʜ", callback_data="yeanr"),
                 InlineKeyboardButton(f"{last_month}", callback_data="ynear")
            ],
            [
                InlineKeyboardButton("ᴛʜɪs ʏᴇᴀʀ", callback_data="yearn"),
                InlineKeyboardButton(f"{year}", callback_data="yenjar")
            ],
            [
                InlineKeyboardButton("♻️ ʀᴇҒʀᴇSʜ", callback_data="rfsh")
            ]
        ]
        
        # Create inline keyboard markup
        keyboard = InlineKeyboardMarkup(buttons)
        await query.message.edit(f"ᴛᴏᴛᴀʟ ᴠᴇʀɪҒɪᴇᴅ ᴜsᴇʀs ✨", reply_markup=keyboard)
    except Exception as e:      
        await query.answer(f" {e}")
