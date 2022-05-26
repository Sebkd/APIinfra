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

def get_responce(responce):
    if isinstance()


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
    params = {
        'UserID': user_id,

    }

def main(login, password, url, headers):
    encrypted_password = get_password_encrypted(password=password, key=13)
    data_input = login_to_api(urlbase=url, headers=headers, login=login, enc_pass=encrypted_password)

    data_info_auth = json_get_info_auth(urlbase=url, headers=headers)
    data_json_info_auth = data_info_auth.json()
    # забираем значение UserID
    user_id = data_json_info_auth['UserID']
    get_urgent_list(urlbase=url, headers=headers)
    data_call_type = get_call_type_list_for_client(urlbase=url, headers=headers)
    data_json_call_type = data_call_type.json()
    # здесь забираем через ID и Name тип заявки и айди-зявки




if __name__ == '__main__':
    URL = 'http://62.109.6.35/inframanager/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 '
                             'Safari/537.36',
               'Accept-Language': 'ru-RU,ru;q=0.9',
               }
    LOGIN = 'user'
    PASSWORD = 'user'

    main(url=URL, headers=HEADERS, login=LOGIN, password=PASSWORD)
