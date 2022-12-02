def data_for_chat_parsing():
    # region
    """
    Функция для приёма:

    **user_API**

    **списка ссылок на чаты**

    :return: Список ссылок на чаты, user_API
    """
    arr_chats = []
    api_id = input('Напишите сюда свой api_id - ')
    api_hash = input('Напишите сюда свой api_hash - ')
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
    # endregion
    return arr_chats, api_id, api_hash
