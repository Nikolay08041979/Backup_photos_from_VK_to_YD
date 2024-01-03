import requests
from pprint import pprint
import yadisk
import json
from alive_progress import alive_bar
from datetime import datetime
import time
import os
from os import path

""" Получение VK access_token """  # Implicit Flow для получения ключа доступа пользователя https://dev.vk.com/ru/api/access-token/implicit-flow-user

from vk_access_token import vk_token

""" Скачивание фотографий с профиля VK """  # https://dev.vk.com/ru/method/photos.get

class VKAPIClient:

    VK_API_PHOTOGET_URL = 'https://api.vk.com/method'  # url = 'https://api.vk.com/method/photos.get'

    def __init__(self, vk_user_id):
        self.vk_user_id = vk_user_id  # vk_user_id = 838704138 #int(input('Ваш VK ID (цифровой), откуда необходимо # скачать фотографии: ')) # my VK ID 838704138 https://vk.com/id838704138

    def get_params_vk_photos(self):
        return {'access_token': vk_token,
                'v': '5.131',
                'owner_id': self.vk_user_id,
                'album_id': 'profile',
                'extended': 1,  # 'likes' have to be used for file photo name <qty_likes.jpg>
                'feed_type': 'photo',
                'photo_sizes': 1,
                'count': 5}  # Photos qty by default: 5

    def get_vk_profile_photos_info(self):
        params = self.get_params_vk_photos()
        response = requests.get(f'{self.VK_API_PHOTOGET_URL}/photos.get', params=params)
        if 200 <= response.status_code <= 300:
            photos_sizes_list = response.json()['response']['items'][0]['sizes']
            return photos_sizes_list
        else:
            return 'ERROR'

    def get_vk_profile_photos_url(self):  # here we have to get photos urls based on specific requirements (max height/width) mentioned in project description
        items = self.get_vk_profile_photos_info()
        items_sorted = sorted(items, key=lambda item: (item['height'] * item['width']), reverse=True)
        photos_url_list = [item['url'] for item in items_sorted]
        return photos_url_list[:5]  # Photos qty by default: 5

    def get_vk_profile_photos_size(self):
        items = self.get_vk_profile_photos_info()
        items_sorted = sorted(items, key=lambda item: (item['height'] * item['width']), reverse=True)
        photos_size_list = [item['type'] for item in items_sorted]
        return photos_size_list[:5]  # Photos qty by default: 5


if __name__ == '__main__':
    vk_user_id = int(input('Ваш VK ID (цифровой), откуда необходимо скачать фотографии: ')) # 838704138
    vk_client = VKAPIClient(vk_user_id)
    pprint(vk_client.get_vk_profile_photos_info())
    pprint(vk_client.get_vk_profile_photos_url())
    pprint(vk_client.get_vk_profile_photos_size())

