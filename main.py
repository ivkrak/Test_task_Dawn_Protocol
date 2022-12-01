from telethon import TelegramClient
from API import api_id, api_hash
from functions import data_for_chat_parsing


arr_chats, user_API = data_for_chat_parsing()

print(f'{user_API=}\n{arr_chats=}')
