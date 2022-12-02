import pandas as pd
from telethon.sync import TelegramClient
import warnings
from crypt import api_keys

chat_urls = ['https://t.me/pohod_irk', 'https://t.me/lobbyirk']
api_id, api_hash = api_keys()
client = TelegramClient('name', api_id, api_hash)
client.start()
warnings.simplefilter(action='ignore', category=FutureWarning)


def date_about_chat_users(url_list):
    df = pd.DataFrame()
    for url in url_list:
        participants = client.get_participants(url)

        for user in participants:
            new_dct = {
                "User ID": user.id,
                "User name": user.username,
                "First name": user.first_name,
                "Last name": user.last_name,
                "User phone number": user.phone,
                "Premium": user.premium
            }

            df = df.append(new_dct, ignore_index=True)
            df.reset_index(drop=True, inplace=True)
    df.to_csv('Data/test1_df.csv')
    return None


if __name__ == 'main':
    date_about_chat_users(chat_urls)
