import requests
from pprint import pprint
import yadisk
import json
from alive_progress import alive_bar
from datetime import datetime
import time

""" Получение VK access_token """ # Implicit Flow для получения ключа доступа пользователя https://dev.vk.com/ru/api/access-token/implicit-flow-user

from vk_access_token import vk_token

""" Скачивание фотографий с профиля VK """ # https://dev.vk.com/ru/method/photos.get

vk_user_id = int(input('Ваш VK ID (цифровой), откуда необходимо скачать фотографии: ')) # my VK ID 838704138 https://vk.com/id838704138

VK_API_PHOTOGET_URL = 'https://api.vk.com/method'  # url = 'https://api.vk.com/method/photos.get'

def get_params_vk_photos():
    return {'access_token': vk_token,
            'v': '5.131',
            'owner_id': vk_user_id,
            'album_id': 'profile',
            'extended': 1,  # 'likes' have to be used for file photo name <qty_likes.jpg>
            'feed_type': 'photo',
            'photo_sizes': 1,
            'count': 5}  # Photos qty by default: 5

def get_vk_profile_photos_info():
    params = get_params_vk_photos()
    response = requests.get(f'{VK_API_PHOTOGET_URL}/photos.get', params=params)
    photos_sizes_list = response.json()['response']['items'][0]['sizes']
    return photos_sizes_list

def get_vk_profile_photos_url():       # here we have to get photos urls based on specific requirements (max height/width) mentioned in project description
    items = get_vk_profile_photos_info()
    items_sorted = sorted(items, key=lambda item: (item['height'] * item['width']), reverse=True)
    photos_url_list = [item['url'] for item in items_sorted]
    return photos_url_list[:5]  # Photos qty by default: 5

def get_vk_profile_photos_size():
    items = get_vk_profile_photos_info()
    items_sorted = sorted(items, key=lambda item: (item['height'] * item['width']), reverse=True)
    photos_size_list = [item['type'] for item in items_sorted]
    return photos_size_list[:5]  # Photos qty by default: 5


""" Сохранение фотографий на Яндекс.Диск """

ya_token = str(input('Ваш токен c Полигона Яндекс.диска: '))  # токен с Полигона Яндекс.Диска https://yandex.ru/dev/disk/poligon/

YA_API_URL_FOLDER_CREATE = 'https://cloud-api.yandex.net/v1/disk/resources'
YA_API_URL_GET_LINK = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

def get_ya_headers():
    return {'Content-Type': 'application/json',
            'Authorization': f'OAuth {ya_token}'}

def get_ya_folder_params():
    return {'path': 'VK_photos',
            'overwrite': 'true'}

def get_ya_folder_create():
    params = get_ya_folder_params()
    headers = get_ya_headers()
    response = requests.put(YA_API_URL_FOLDER_CREATE, headers=headers, params=params)
    if response.status_code == 201:
        return 'Папка VK_photos успешно создана на Яндекс.Диске'
    else:
        return response.json()['message']

def get_file_name():
    date = datetime.strftime(datetime.now(), "%d.%m.%Y-%H.%M.%S")
    return date

def get_photos_upload_pc():
    photos_list_urls = get_vk_profile_photos_url()
    for idx, url in enumerate(photos_list_urls):
        response = requests.get(url)
        with open(f'#{idx+1}_vk_photo.jpg', 'wb') as file:
            file.write(response.content)
        print(f'Фотография "#{idx+1}_vk_photo.jpg" успешно сохранена на ПК')
    return f'Все {len(get_vk_profile_photos_url())} фотографий успешно сохранены на ПК'

""" Загрузка файлов на Яндекс.Диск """ # Загрузка файла на Диск | описание API | https://yandex.ru/dev/disk/api/reference/upload.html#url-request

def get_photos_upload_ya():
    headers = get_ya_headers()
    for i in range(len(get_vk_profile_photos_url())):
        params = {'path': f'/VK_photos/#{i+1}_vk_photo.jpg',
              'overwrite': 'true',
              'fields': 'size'}
        response = requests.get(YA_API_URL_GET_LINK, params=params, headers=headers)
        url_for_upload = response.json().get('href')
        with open(f'#{i+1}_vk_photo.jpg', 'rb') as file:
            response = requests.put(url_for_upload, files={'file': file}, headers=headers)
        print(f'Фотография "#{i+1}_vk_photo.jpg" успешно загружена на Яндекс.Диск')
    return f'Все {len(get_vk_profile_photos_url())} фотографий успешно загружены на Яндекс.Диск'

def write_json_log():
    photos_size_list = get_vk_profile_photos_size()
    with open('vk_photos_log.json', 'w') as file:
        for idx, photo_size in enumerate(photos_size_list):
            to_json = {'file_name': f'#{idx+1}_{get_file_name()}.jpg', 'size': photo_size}
            json.dump(to_json, file)
            print(f'Информация о загруженной фотографии с именем "#{idx+1}_{get_file_name()}.jpg" добавлена в json-файл')
    return f'Вся информация по {len(get_vk_profile_photos_size())} фотографиям успешно добавлена в файл vk_photos_log.json'

def read_json_log():
    write_json_log()
    with open('vk_photos_log.json') as file:
        data = [photo for photo in file]
        return data
# --------------------------------------------------------------------
""" REST API """

y = yadisk.YaDisk(token=ya_token)

def get_photos_upload_YaRestAPI():
    get_photos_upload_pc()
    get_ya_folder_create()
    for i in range(len(get_vk_profile_photos_url())):
        y.upload(f'#{i+1}_vk_photo.jpg', f'/VK_photos/#{i+1}_{get_file_name()}.jpg')
        print(f'Фотография "#{i+1}_{get_file_name()}.jpg" успешно загружена на Яндекс.Диск')
    return f'Все {len(get_vk_profile_photos_url())} фотографий успешно загружены на Яндекс.Диск'
# --------------------------------------------------------------------

""" Прогресс-бар """

mylist = [1,2,3,4,5,6,7,8]

with alive_bar(len(mylist)) as bar:
    for i in mylist:
        bar()
        time.sleep(1)

# --------------------------------------------------------------------

print()
pprint(get_photos_upload_YaRestAPI())
print()
pprint(read_json_log())

