import pandas as pd
from telethon.sync import TelegramClient
import warnings
from crypt import api_keys

chat_urls = ['https://t.me/pohod_irk', 'https://t.me/lobbyirk', 'https://t.me/pythonstepikchat',
             'http://t.me/+fqNb78zlQY81NGUy']
api_id, api_hash = api_keys()
client = TelegramClient('ivkrak', api_id, api_hash)
client.start()
warnings.simplefilter(action='ignore', category=FutureWarning)


def date_about_chat_users(url_list):
    df = pd.DataFrame()
    for url in url_list:
        print(f'Собираю информацию из чата: {url}')

        try:
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
        except Exception as ex:
            print(f'{ex}\nОШИБКА С ЧАТОМ: {url}')
    df.rename(columns={"": "index"})
    df.to_csv('Data/Users_info.csv')


if __name__ == '__main__':
    date_about_chat_users(chat_urls)