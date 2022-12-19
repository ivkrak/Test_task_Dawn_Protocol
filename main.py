import pandas as pd
from telethon.sync import TelegramClient
import warnings
from telethon.tl.functions.channels import JoinChannelRequest
from tqdm import tqdm
import requests
import ujson as json
import codecs
import os

class JsonGetInfo:
    @staticmethod
    def read_json(json_path: str) -> str:
        with codecs.open(json_path, "r", "utf-8") as F:
            return json.load(F)

    @staticmethod
    def write_to_json(json_path: str, data) -> None:
        if not isinstance(data, str):
            data = json.dumps(data)
        with codecs.open(json_path, "w", "utf-8") as temp:
            temp.write(data)


def file_exist(fname) -> bool:
    if fname is None:
        return False
    return os.path.exists(fname)


def get_session(session):
    if file_exist(f'sessions//{session}.json'):
        try:
            json_path = 'sessions//{}.json'.format(session)
            return JsonGetInfo.read_json(json_path)
        except Exception as ex:
            print(f'Ошибка с сессией {ex}')
            return None



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
    ДОПИЛИТЬ!!! Медленно работает!!!
    :param user_login: имя пользователя / username
    :return: информация о пользователе типа str, в случае ошибки, выдаст None и описание ошибки
    """
    r = requests.get(f'https://t.me/{user_login}')
    arr = list(r.text.split('\n'))
    s = str((arr[27])[42::])

    return s if 'You can contact' not in s else None



session = get_session('79263782950')

client = TelegramClient(session=f"sessions/{str(session['session_file'])}", api_id=session['app_id'], api_hash=session['app_hash'],
                         proxy=session['proxy'])


client.start()
warnings.simplefilter(action='ignore', category=FutureWarning)


def date_about_chat_users(url_list):
    df = pd.DataFrame()
    for url in url_list:
        print(f'Собираю информацию из чата: {url}')

        try:
            client(JoinChannelRequest(url)) # заходит в чат по utl
            for user in tqdm(client.get_participants(url)): # получает список юзеров с информацией о них из чата
                if user.username is not None:
                    if (bio := get_bio(user.username)) is not None:
                        new_dct = {
                            "User ID": user.id,
                            "User name": user.username,
                            "First name": user.first_name,
                            "Last name": user.last_name,
                            "User phone number": user.phone,
                            "Premium": user.premium,
                            "About user": bio
                        }
                        if filter_words(words_list=['smm', 'смм'], text=str(new_dct.values()) + str(bio)):
                            df = df.append(new_dct, ignore_index=True)
                            df.reset_index(drop=True, inplace=True)
        except Exception as ex:
            print(f'{ex}\nОШИБКА С ЧАТОМ: {url}')
    # df.rename(columns={"": "index"})
    df.to_csv('Data/Filtered_Users_info.csv', encoding="utf-16")
    df.to_html('Data/Filtered_Users_info.html', encoding="utf-16")
    df.to_excel('Data/Filtered_Users_info.xlsx', encoding="utf-16")


if __name__ == '__main__':
    date_about_chat_users([
    'https://t.me/smm_chat1',
    ])
