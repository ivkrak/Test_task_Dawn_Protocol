from telethon.sync import TelegramClient
from API import api_id, api_hash

# test_url = 'https://t.me/pohod_irk'
client = TelegramClient('name', api_id, api_hash)
client.start()

participants = client.get_participants('pohod_irk')
s = str(participants)
