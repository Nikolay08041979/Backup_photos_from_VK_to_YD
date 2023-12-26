# Курсовая работа «Резервное копирование»

## Прилагаются:
✅ Файл с кодом программы: main.py

✅ Файл с зависимостями: requirements.txt

## Задание:

### Нужно написать программу, которая будет:
✅ Получать фотографии с профиля (аватарок). Для этого нужно использовать метод photos.get. 

✅ Сохранять фотографии максимального размера (ширина/высота в пикселях) на Я.Диске.

✅ Для имени фотографий использовать количество лайков (если количество лайков одинаково, то добавить дату загрузки).

✅ Сохранять информацию по фотографиям в json-файл с результатами.

### Входные данные:
#### Пользователь вводит:
1) id пользователя vk;
2) токен с Полигона Яндекс.Диска. 
   
#### Выходные данные:
1) json-файл с информацией по файлу:
   [{
    "file_name": "34.jpg",
    "size": "z"
    }]
2) Измененный Я.диск, куда добавились фотографии.​​

### Обязательные требования к программе:
✅ Использовать REST API Я.Диска и ключ, полученный с полигона.

✅ Для загруженных фотографий нужно создать свою папку.

✅ Сохранять указанное количество фотографий (по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске

✅ Сделать прогресс-бар или логирование для отслеживания процесса программы. 

✅ Код программы должен удовлетворять PEP8.

✅ У программы должен быть свой отдельный репозиторий.

✅ Все зависимости должны быть указаны в файле requiremеnts.txt.​ 

## Дополнтельные открытые вопросы по коду, по которым требуются комментарии 

1) (до 32 строки) необходимо разобрать адресную строку, чтобы получить из нее VK access_token (пока необходимо вставлять вручную). Подскажите как это сделать или может есть под рукой описание как это сделать. будут очень признателен????

2) (с 34 по 68 строки) здесь получаю ссылки на фотографии с профиля (аватарки) как сказано по условию. в моем профиле в VK только одна фотка (технически вставить больше чем одну там нельзя!), поэтому везде одна и та же ссылка на фото из профиля..... при этом размер у всех копий разный! то есть можно предположить, что инфа возвращается по разным фото, а ссылка только на одну фото - из профиля....  вот ссылка на мой профль в vk https://vk.com/id838704138 (я его только для этой задачи создал, поэтому лайков там нет и далее в качестве имени используется дата заказчки фото на яндекс диск). далее везде в работе только одна полученная фото из профиля в пяти копиях с разным размером.
