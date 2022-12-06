import pandas as pd
from telethon.sync import TelegramClient
import warnings
from telethon.tl.functions.channels import JoinChannelRequest
import socks
from telethon.tl.functions.users import GetFullUserRequest
import time
import math


def filter_words(words_list, text):
    """
    Возвращает False, если в text нет ни одного слова из words_list, в остальных случаях возвращает True
    :param words_list: Список с словами для фильтрации
    :param text: текст для фильтрации
    :return: boolean
    """
    text = text.lower()
    for word in words_list:
        if word.lower() in text:
            return True
    return False


async def get_bio(user):
    pass


client = TelegramClient('79263782950', api_id='2040', api_hash='b18441a1ff607e10a989891a5462e627',
                        proxy=(3, "gate.dc.smartproxy.com", 20000, True, "user-Port50", "Ghd7lKaQj077"))
client.start()
warnings.simplefilter(action='ignore', category=FutureWarning)


def date_about_chat_users(url_list):
    num_of_users = 0
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    for url in url_list:
        print(f'Собираю информацию из чата: {url}')

        try:
            client(JoinChannelRequest(url))
            participants = client.get_participants(url)
            for i, user in enumerate(participants):
                num_of_users += 1
                if not (user.username is None):
                    bio = client(GetFullUserRequest(user)).full_user.about
                    if not (user.username is None) and not (bio is None):
                        new_dct = {
                            "User ID": user.id,
                            "User name": user.username,
                            "First name": user.first_name,
                            "Last name": user.last_name,
                            "User phone number": user.phone,
                            "Premium": user.premium,
                            "About user": bio
                        }
                        if filter_words(words_list=['Python', 'Developer'], text=str(new_dct) + str(bio)):
                            print('----Пользователь прошёл фильтр и был добавлен в таблицу----')
                            df = df.append(new_dct, ignore_index=True)
                            df.reset_index(drop=True, inplace=True)
                    else:
                        new_dct = {
                            "User ID": user.id,
                            "User name": user.username,
                            "First name": user.first_name,
                            "Last name": user.last_name,
                            "User phone number": user.phone,
                            "Premium": user.premium,
                            "About user": bio
                        }
                        df2 = df2.append(new_dct, ignore_index=True)
                        df2.reset_index(drop=True, inplace=True)
        except Exception as ex:
            print(f'{ex}\nОШИБКА С ЧАТОМ: {url}')
    df.rename(columns={"": "index"})
    df.to_csv('Data/Users_info.csv')
    print(f'Количество проскандированных пользователей: {num_of_users}')


if __name__ == '__main__':
    t = time.time()
    date_about_chat_users([
        'https://t.me/smmchat',
        'https://t.me/smmpub_chat',
        'https://t.me/smm_telegram_chat',
        'https://t.me/chat_pro_smm',
        'https://t.me/smmchat',
        'https://t.me/chat_skam',
        'https://t.me/smmruschats',
        'https://t.me/chatus13',
        'https://t.me/smm_chat',
        'https://t.me/smm_chat1',
        'https://t.me/smm_chat2'
    ])
    print("---%s seconds---" % (time.time() - t))
