# import telethon


def data_for_chat_parsing():
    """
    Функция для приёма:

    **user_API**

    **списка ссылок на чаты**

    :return: Список ссылок на чаты, user_API
    """
    arr_chats = []
    user_API = input('Напишите сюда свой user API - ')
    n = int(input("""Для выбора одного из сценариев нужно ввести число:
        1 - Построчный ввод ссылок на чаты
        0 - Ввод ссылок на чаты через ; (точку с запятой)
        
        Ваше число - """))

    match n:
        case 1:
            print('Для завершения ввода отправьте пустой ввод')
            while True:
                s = input('Напишите сюда название чата - ')
                if s == '':
                    break
                else:
                    arr_chats.append(s)
        case 0:
            arr_chats = input('Напишите сюда название чатов через ;  (точку с запятой) - ').replace(' ', '').split(';')
    return arr_chats, user_API


arr_chats, user_API = data_for_chat_parsing()

print(f'{user_API=}\n{arr_chats=}')
