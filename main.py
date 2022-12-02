import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import UserStatusOnline

from crypt import api_keys
import pandas as pd
# test_url = 'https://t.me/pohod_irk'
api_id, api_hash = api_keys()
client = TelegramClient('name', api_id, api_hash)
client.start()
participants = client.get_participants('https://t.me/lobbyirk')


def TotalList_to_json(TotalList):
    """
    Функция для преобразования формата TotalList в json
    :return: json
    """

    df = pd.DataFrame()
    for i in TotalList:
        s = (str(i))
        s = s.replace("=", ": ")
        s = s.replace("User(", "{'")
        s = s.replace(", ", ",\n'")
        s = s.replace(":", "':")
        s = s.replace("UserProfilePhoto(", "{'")
        s = s.replace("UserStatusOffline(", "{'")
        s = s.replace("UserStatusOnline(", "{'")
        s = s.replace("utc))", "utc)}")
        s = s.replace("')", "'")
        s = s.replace("'phone': ", "'phone': '")
        s = s[0:-1]+ "'''" + '}'
        s = s.replace("'0", "0")
        s = s.replace("'1", "1")
        s = s.replace("'2", "2")
        s = s.replace("'3", "3")
        s = s.replace("'4", "4")
        s = s.replace("'5", "5")
        s = s.replace("'6", "6")
        s = s.replace("'7", "7")
        s = s.replace("'8", "8")
        s = s.replace("'9", "9")
        s = s.replace("'tzinfo':", "tzinfo=")
        s = s.replace("'None", "None")
        s = s.replace("'photo': ", "'photo': '''" )
        try:
            s = s.replace("expires'", "'expires'")
        except NameError:
            pass
        try:
            s = s.replace("UserStatusRecently()", "None")
        except NameError:
            pass
        with open('Data/inf.txt', encoding='utf-8', mode="w") as f:
            try:
                f.seek(0)
                f.write(s)
                dct = eval(s)
            except SyntaxError:
                try:
                    f.seek(0)
                    f.write(s)
                    s = s + '}'
                    dct = eval(s)
                except SyntaxError:
                    try:
                        f.seek(0)
                        f.write(s)
                        s = s + '}'
                        dct = eval(s)
                    except SyntaxError:
                        try:
                            f.seek(0)
                            f.write(s)
                            s = s +'}'
                            dct = eval(s)
                        except SyntaxError:
                            dct = {
                                'id': None,
                                'username': None,
                                'first_name': None,
                                'last_name': None,
                                'phone': None,
                                'premium': None
                            }
            f.seek(0)
            f.write(s)
            new_dct = {
                'UserID': dct['id'],
                'User_name': dct['username'],
                'First_name': dct['first_name'],
                'Last_name': dct['last_name'],
                'User_phone_number': dct['phone'],
                'Premium': True if dct['premium']==True else None

            }
            df = df.append(new_dct, ignore_index=True)
            df.reset_index(drop=True, inplace=True)
            df.to_csv('Data/df.csv')
            df.to_json('Data/df.json')
    return df


print(TotalList_to_json(participants))
