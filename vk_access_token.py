from urllib.parse import urlencode
import requests
from pprint import pprint

""" Получение VK access_token """ # Implicit Flow для получения ключа доступа пользователя https://dev.vk.com/ru/api/access-token/implicit-flow-user

vk_app_id = 51817165  # ID APP VK keeps the same

VK_OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'

def get_params_vk_auth():
    return {'client_id': vk_app_id,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'scope': 'photos',
            'response_type': 'token',
            'v': '5.131'}

def get_vk_access_token():
    params = get_params_vk_auth()
    response = requests.get(f'{VK_OAUTH_BASE_URL}?{urlencode(params)}')
    return response

def get_vk_oauth_url():
    params = get_params_vk_auth()
    vk_oauth_url = f'{VK_OAUTH_BASE_URL}?{urlencode(params)}'
    return vk_oauth_url

# Здесь необходимо разобрать адресную строку, чтобы получить из нее access_token... пока вставлен вручную ниже

vk_token = str(input('Необходимо вручную вставить VK access token: '))

# ---------------------------------------------------

pprint(get_vk_oauth_url())
print()
pprint(get_vk_access_token())
print()
