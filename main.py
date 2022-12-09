import pandas as pd
from telethon.sync import TelegramClient
import warnings
from telethon.tl.functions.channels import JoinChannelRequest
from datetime import datetime
from tqdm import tqdm
import requests


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


def get_bio(user_login):
    """
    Функция для выполнения запросов (about user)
    :param user_login: имя пользователя / username
    :return: информация о пользователе типа str, в случае ошибки, выдаст None и описание ошибки
    """
    r = requests.get(f'https://t.me/{user_login}')
    arr = list(r.text.split('\n'))
    s = str((arr[27])[42::])

    return s if 'You can contact' not in s else None


client = TelegramClient('79263782950', api_id='2040', api_hash='b18441a1ff607e10a989891a5462e627',
                        proxy=(3, "gate.dc.smartproxy.com", 20000, True, "user-Port50", "Ghd7lKaQj077"))
client.start()
warnings.simplefilter(action='ignore', category=FutureWarning)


def date_about_chat_users(url_list):
    df = pd.DataFrame()
    for url in url_list:
        print(f'Собираю информацию из чата: {url}')

        try:
            try:
                client(JoinChannelRequest(url))
            except Exception as ex: print(ex)
            for user in tqdm(client.get_participants(url)):
                # wasOnline = user.status.was_online ТУТ НУЖНО ДОПИЛИТЬ

                 if user.username is not None:
                    if user.username is not None and (bio := get_bio(user.username)) is not None:
                        new_dct = {
                            "User ID": user.id,
                            "User name": user.username,
                            "First name": user.first_name,
                            "Last name": user.last_name,
                            "User phone number": user.phone,
                            "Premium": user.premium,
                            "About user": bio
                        }
                        if True or filter_words(words_list=['smm', 'смм'], text=str(new_dct) + str(bio)):
                            df = df.append(new_dct, ignore_index=True)
                            df.reset_index(drop=True, inplace=True)
        except Exception as ex:
            print(f'{ex}\nОШИБКА С ЧАТОМ: {url}')
    df.rename(columns={"": "index"})
    df.to_csv('Data/Filtered_Users_info.csv')


if __name__ == '__main__':
    t = datetime.now()

    date_about_chat_users([
    'https://t.me/chat3',
    ])

    print('Время работы программы: ', datetime.now() - t)
