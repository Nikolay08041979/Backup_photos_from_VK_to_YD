import requests
from pprint import pprint
import yadisk
import json
from alive_progress import alive_bar
from datetime import datetime
import time
import os
from os import path

""" Получение VK access_token """ # Implicit Flow для получения ключа доступа пользователя https://dev.vk.com/ru/api/access-token/implicit-flow-user

from vk_access_token import vk_token

""" Скачивание фотографий с профиля VK """ # https://dev.vk.com/ru/method/photos.get

from vk_api_client import VKAPIClient

""" Сохранение фотографий на Яндекс.Диск """

def get_file_name():
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    return date

class YaDiskAPIClient(VKAPIClient):

    YA_API_URL_FOLDER_CREATE = 'https://cloud-api.yandex.net/v1/disk/resources'
    YA_API_URL_GET_LINK = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def __init__(self, ya_token, ya_folder_name):
        VKAPIClient.__init__(self, vk_user_id)
        self.ya_token = ya_token
        self.ya_folder_name = ya_folder_name
        self.y = yadisk.YaDisk(token=self.ya_token)

    def get_ya_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.ya_token}'}

    def get_ya_folder_params(self):
        return {'path': self.ya_folder_name,
                'overwrite': 'true'}

    def get_ya_folder_create(self):
        params = self.get_ya_folder_params()
        headers = self.get_ya_headers()
        response = requests.put(self.YA_API_URL_FOLDER_CREATE, headers=headers, params=params)
        if 200 <= response.status_code <= 300:
            return f'Папка {self.ya_folder_name} успешно создана на Яндекс.Диске'
        else:
            return response.json()['message']

    def get_photos_upload_pc(self):
        photos_list_urls = VKAPIClient.get_vk_profile_photos_url(self)
        for idx, url in enumerate(photos_list_urls):
            response = requests.get(url)
            with open(f'#{idx+1}_vk_photo.jpg', 'wb') as file:
                file.write(response.content)
            print(f'Фотография "#{idx+1}_vk_photo.jpg" успешно сохранена на ПК')
        return f'Все {len(photos_list_urls)} фотографий успешно сохранены на ПК'

    """ Загрузка файлов на Яндекс.Диск """ # Загрузка файла на Диск | описание API | https://yandex.ru/dev/disk/api/reference/upload.html#url-request

    def wr_json_log(self):
        photos_list_sizes = VKAPIClient.get_vk_profile_photos_size(self)
        file_date = get_file_name()
        with open('vk_photos_log.json', 'w') as file:
            for idx, photo_size in enumerate(photos_list_sizes):
                to_json = {'file_name': f'#{idx+1}_{file_date}.jpg', 'size': photo_size}
                json.dump(to_json, file)
                print(f'Информация о загруженной фотографии с именем "#{idx+1}_{file_date}.jpg" добавлена в json-файл')
        print(f'Вся информация по {len(photos_list_sizes)} фотографиям успешно добавлена в файл vk_photos_log.json')
        with open('vk_photos_log.json') as file:
            data = [photo for photo in file]
            return data
# --------------------------------------------------------------------
    """ REST API """

#    y = yadisk.YaDisk(token=ya_token)

    def get_photos_upload_YaRestAPI(self):
#        self.y = yadisk.YaDisk(token=self.ya_token)
        self.get_photos_upload_pc()
        self.get_ya_folder_create()
        file_date = get_file_name()
        photos_list_urls = VKAPIClient.get_vk_profile_photos_url(self)
        for idx in range(len(photos_list_urls)):
            self.y.upload(f'#{idx+1}_vk_photo.jpg', f'/{self.ya_folder_name}/#{idx+1}_{file_date}.jpg')
            print(f'Фотография "#{idx+1}_{file_date}.jpg" успешно загружена на Яндекс.Диск')
        return f'Все {len(photos_list_urls)} фотографий успешно загружены на Яндекс.Диск'
# --------------------------------------------------------------------

""" Прогресс-бар """

mylist = [1,2,3,4,5,6,7,8]

with alive_bar(len(mylist)) as bar:
    for i in mylist:
        bar()
        time.sleep(1)

# --------------------------------------------------------------------

if __name__ == '__main__':
    vk_user_id = int(input('Ваш VK ID (цифровой), откуда необходимо скачать фотографии: '))  # 838704138
    ya_token = str(input('Ваш токен c Полигона Яндекс.диска: ')) # токен с Полигона Яндекс.Диска https://yandex.ru/dev/disk/poligon/
    ya_folder_name = str(input('Введите имя папки на Яндекс.Диске: ')) # VK_photos

    yd_client = YaDiskAPIClient(ya_token, ya_folder_name)

    print()
    pprint(yd_client.get_photos_upload_YaRestAPI())
    print()
    pprint(yd_client.wr_json_log())
