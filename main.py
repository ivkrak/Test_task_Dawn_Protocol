import grequests
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import ujson as json
import codecs
import os
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import warnings

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


session = get_session('79263782950')
client = TelegramClient(session=f"sessions/{str(session['session_file'])}", api_id=session['app_id'],
                        api_hash=session['app_hash'], proxy=session['proxy'])
client.start()
warnings.simplefilter(action='ignore', category=FutureWarning)


def main(url_list, filter_words_list):
    """
    Функция для сбора аудитории из чатов и фильтрации bio
    :param url_list: list
    :param filter_words_list: list / None
    :return: exel table, csv table
    """

    df = pd.DataFrame()
    full_info = []
    arr_bio = []
    arr_user_name = []
    users_info = []

    for url in url_list:
        print(f'Собираю информацию из чата: {url}')
        client(JoinChannelRequest(url))
        print('Идёт сбор информации об участниках чата')
        users_info = client.get_participants(url)
        arr_user_name = [f'https://t.me/{user.username}' for user in users_info]
        print('Собираю дополнительные данные')

    response = (grequests.get(bio) for bio in arr_user_name)
    resp = grequests.map(response)

    for i in resp:
        if i is not None:
            soup = BeautifulSoup(i.text, 'lxml')

            if 'If you have <strong>Telegram</strong>' in i.text:
                arr_bio.append('')
            else:
                bio = soup.find('div', class_='tgme_page_description')
                arr_bio.append(bio.text)
        else:
            arr_bio.append('')

    result_before_file = {}

    for i, user in enumerate(users_info):
        if user.username is not None:
            result_before_file[user.username] = {
                "User ID": user.id,
                "User name": f'@{user.username}',
                "First name": user.first_name,
                "Last name": user.last_name,
                "User phone number": user.phone,
                "Premium": user.premium,
                "About user": arr_bio[i],
            }

            # test = str(result_before_file[user.username].values()) + str(arr_bio[i])
            # if test is None:
            #     test = ''

            result_before_file[user.username]['full_user_info_text'] = str(result_before_file[user.username].values()) + str(arr_bio[i])

    for value in result_before_file.values():
        if len(filter_words_list) > 0:
            for word in filter_words_list:
                # stop
                if word.lower() in value['full_user_info_text'].lower():
                    del value['full_user_info_text']
                    full_info.append(value)
        else:
            del value['full_user_info_text']
            full_info.append(value)

    for value in full_info:
        df = df.append(value, ignore_index=True)
        df.reset_index(drop=True, inplace=True)

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
            'https://t.me/smm_chat1',
            'https://t.me/mnogorukiy_smm_chat',
            'https://t.me/dads_chat',
            'https://t.me/lobbyirk',
            'https://t.me/pydjango',
            'https://t.me/pohod_irk'
        ],
        filter_words_list=[]
    )

    print('Время работы программы: ', datetime.now() - t)