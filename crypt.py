import cryptocode


def api_keys():
    """
    Функция для дешифрования api_id и api_hash
    :return: api_id, api_hash
    """
    api_id = 'As1mCflR+/k=*zLyvSufeU8RYD3PcYLulvw==*XVafoLqfNEjVVUzB5/8/aw==*eXbQd3enrVjXmVi3hKAHgQ=='
    api_hash = '4bdeiTfla7xytkd82eDsf2keW6TkSad2TY9vlPQliDg=*r4iqZjhleBNYUOMEAV8eVQ==*fAzCrD0dqHmFzEVvJPNmOw==*ubx8TTtVFktKXy5gfuWOvg=='

    decrypt_password = input('Ваш пароль для расшифровки api - ')

    return cryptocode.decrypt(api_id, decrypt_password), cryptocode.decrypt(api_hash, decrypt_password)
