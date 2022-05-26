"""
Взаимодействие с API Инфра
"""
from urllib.parse import urljoin, urlencode

import requests

SIGN_IN = 'accountApi/SignIn/'
AUTH_USER_INFO = 'accountApi/GetAuthenticationInfo/'
GET_URGENT_LIST = 'sdApi/GetUrgencyList/'
GET_CALL_TYPE_LIST = 'sdApi/GetCallTypeListForClient/'
REGISTER_CALL = 'sdApi/registerCall/'
SIGN_OUT = 'accountApi/SignOut/'


def get_password_encrypted(password, key):
    """Получение шифрованного пароля"""
    return ''.join(chr(x) for x in list(map(lambda y: ord(y) ^ key, password)))


def get_query_params(urlbase, params):
    """Присоединение query параметров к пути"""
    query = "?" + urlencode(params)
    url = urljoin(urlbase, query)
    return url


def get_full_path(urlbase, function):
    """Путь с учетом функции API"""
    return urlbase + function


def login_to_api(urlbase, headers, login, enc_pass):
    """Вход в API"""
    params = {
        'loginName': login,
        'passwordEncrypted': enc_pass,
    }
    url = get_full_path(urlbase=urlbase, function=SIGN_IN)
    url_post = get_query_params(urlbase=url, params=params)
    response = requests.post(url=url_post, headers=headers)
    return response


def logout_from_api(urlbase, headers):
    url = get_full_path(urlbase=urlbase, function=SIGN_OUT)
    response = requests.post(url=url, headers=headers)
    return response


def get_info_auth(urlbase, headers):
    """Получение информации о пользователе"""
    url = get_full_path(urlbase=urlbase, function=AUTH_USER_INFO)
    response = requests.get(url=url, headers=headers)
    return response


def get_urgent_list(urlbase, headers):
    url = get_full_path(urlbase=urlbase, function=GET_URGENT_LIST)
    response = requests.get(url=url, headers=headers)
    return response


def get_call_type_list_for_client(urlbase, headers):
    url = get_full_path(urlbase=urlbase, function=GET_CALL_TYPE_LIST)
    response = requests.get(url=url, headers=headers)
    return response


def register_call(urlbase, headers, user_id, calltype_id, urgency_id, call_summary_name):
    url = get_full_path(urlbase=urlbase, function=REGISTER_CALL)
    params = {
        'UserID': user_id,
        'CallTypeID': calltype_id,
        'UrgencyID': urgency_id,
        'CallSummaryName': call_summary_name,
        'HTMLDescription': 'Беда'
    }
    url_post = get_query_params(urlbase=url, params=params)
    response = requests.post(url=url_post, headers=headers)
    return response


def main(login, password, url, headers):
    try:
        encrypted_password = get_password_encrypted(password=password, key=13)
        data_input = login_to_api(urlbase=url, headers=headers, login=login, enc_pass=encrypted_password)
        data_json_input = data_input.json()
        if not data_json_input.get('Success'):
            raise Exception('login_to_api failed')

        # забираем значение UserID
        data_info_auth = get_info_auth(urlbase=url, headers=headers)
        if not data_info_auth:  # null
            raise Exception('get_info_auth failed')
        data_json_info_auth = data_info_auth.json()
        user_id = data_json_info_auth.get('UserID')

        # срочность заявки
        data_urgent_list = get_urgent_list(urlbase=url, headers=headers)
        data_json_urgent_list = data_urgent_list.json()
        if not data_json_urgent_list[0].get('ID'):
            raise Exception('get_urgent_list failed')
        urgency_id = data_json_urgent_list[2].get('ID')

        data_call_type = get_call_type_list_for_client(urlbase=url, headers=headers)
        data_json_call_type = data_call_type.json()
        if not data_json_urgent_list[0].get('ID'):
            raise Exception('get_call_type_list_for_client')
        # название заявки
        call_summary_name = data_json_call_type[3].get('Name')
        # ИД типа заявки
        calltype_id = data_json_call_type[3].get('ID')

        data_register_call = register_call(urlbase=url, headers=headers, user_id=user_id, calltype_id=calltype_id,
                                           urgency_id=urgency_id, call_summary_name=call_summary_name)
        data_json_register_call = data_register_call.json()
        if not data_json_register_call.get('CallID'):
            raise Exception('register_call failed')
        data_logout = logout_from_api(urlbase=url, headers=headers)
        data_json_logout = data_logout.json()
        if data_json_logout.get('Message'):
            raise Exception('get_info_auth failed')

    finally:
        return True


if __name__ == '__main__':
    URL = 'http://62.109.6.35/inframanager/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                             'Safari/537.36',
               'Accept-Language': 'ru-RU,ru;q=0.9',
               }
    LOGIN = 'user'
    PASSWORD = 'user'

    if main(url=URL, headers=HEADERS, login=LOGIN, password=PASSWORD):
        print('over')
