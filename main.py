import grequests
import pandas as pd
from telethon.sync import TelegramClient
import warnings
from telethon.tl.functions.channels import JoinChannelRequest
import ujson as json
import codecs
import os
from bs4 import BeautifulSoup
from datetime import datetime

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


def get_session(session: str) -> str:
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


def get_bio(html_text):
    """
    Функция для выполнения запросов (about user)
    ДОПИЛИТЬ!!! Медленно работает!!!
    :param html_text: текст сырого запроса
    :return: информация о пользователе типа str, в случае ошибки, выдаст None и описание ошибки
    """
    # грамматику
    soup = BeautifulSoup(html_text, 'lxml')
    bio = soup.find('div', class_ = 'tgme_page_description')

    try:
        if 'If you have Telegram' in bio.text.strip():
            return ''
        else:
            return bio.text.strip()
    except: return ''


session = get_session('79263782950')
client = TelegramClient(session=f"sessions/{str(session['session_file'])}", api_id=session['app_id'],
                        api_hash=session['app_hash'], proxy=session['proxy'])
client.start()
warnings.simplefilter(action='ignore', category=FutureWarning)


def main(*, url_list, filter_words_list):
    """
    Функция для сбора аудитории из чатов и фильтрации bio
    :param url_list: list
    :param filter_words_list: list / None
    :return: exel table, csv table
    """

    df = pd.DataFrame()
    for url in url_list:
        print(f'Собираю информацию из чата: {url}')
        try:
            client(JoinChannelRequest(url)) # заходит в чат по utl
            print('Идёт сбор информации об участниках чата')
            users_info = client.get_participants(url)
            arr_user_name = [f'https://t.me/{user.username}' for user in users_info]
            print('Собираю дополнительные данные')
            response = (grequests.get(bio) for bio in arr_user_name)
            resp = grequests.map(response)
            arr_bio = []
            for i in resp:
                try:
                    arr_bio.append(get_bio(i.text))
                except: arr_bio.append('')
            for i, user in enumerate(users_info):
                if user.username is not None:
                    new_dct = {
                        "User ID": user.id,
                        "User name": f'@{user.username}',
                        "First name": user.first_name,
                        "Last name": user.last_name,
                        "User phone number": user.phone,
                        "Premium": user.premium,
                        "About user": arr_bio[i]
                    }
                    filter = True if (filter_words_list == [] or filter_words_list is None) else False
                    if filter or (filter_words(words_list=filter_words_list, text=str(new_dct.values()) + str(arr_bio[i]))):
                        df = df.append(new_dct, ignore_index=True)
                        df.reset_index(drop=True, inplace=True)
        except Exception as ex:
            print(f'{ex}\nОШИБКА С ЧАТОМ: {url}')
    df.rename(columns={"": "index"})
    df.to_csv('Data/Filtered_Users_info.csv', encoding="utf-16")
    df.to_excel('Data/Filtered_Users_info.xlsx', encoding="utf-16")
    with open('Data/Filtered_Users_info.txt', 'w', encoding='utf-16') as f:
        for item in list(df['User name'].values):
            f.write(f'{item}\n')

if __name__ == '__main__':
    t = datetime.now()
    main(
        url_list=[
            'https://t.me/shevtsovchat'
            'https://t.me/smm_chat1',
            'https://t.me/pohod_irk',
        ],
        filter_words_list=None
    )

    print('Время работы программы: ', datetime.now() - t)