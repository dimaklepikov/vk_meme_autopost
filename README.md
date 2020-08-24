# Автоматический постинг коммиксов VK

Утилита, позволяющая выкладывать случайный коммикс из [xkcd](https://xkcd.com/) в группу 
социальной сети [VK](https://vk.com/), версия API - 5.122 
 
## Как установить и запустить?
1. Уставновить Python 3+
```sh
$ sudo apt-get install python3
```
2. Установить, создать и активировать виртуальное окружение (Linux or MacOS)
```sh
$ pip install virtualenv
$ virtualenv vk_meme_autopost
$ source vk_meme_autopost/bin/activate
```
3. Установить файл с зависимостями
```sh
$ pip install -r requirements.txt
```
4. Создать [приложение](https://vk.com/apps?act=manage), получить его идентификатор в разделе "настройки"

5. В папке проекта создать файл с переменными окружения [.env](https://pypi.org/project/python-dotenv/):
   - Получить [VK_ACCESS_TOKEN](https://vk.com/dev/implicit_flow_group) для Вашего сообщества
   - Создать в файле переменную с названием TOKEN:
        ```sh
        TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

6. Узнать id группы, в которую будут загружаться коммисксы, вписать его в переменную GROUP_ID в main.py
```sh
GROUP_ID = xxxxxxxxx
```

7. Запустить файл main.py
```sh
$ python3 path/main.py
```

## Цель проекта:
Проект написан в образовательных целях в рамках прохождения курса [API веб-сервисов](https://dvmn.org/modules/web-api)
платформы [DevMan](https://dvmn.org/)
