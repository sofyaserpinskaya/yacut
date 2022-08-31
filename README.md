
# yacut - сервис укорачивания ссылок

### Автор:

yacut - [Софья Серпинская](https://github.com/sofyaserpinskaya)

tests - [Яндекс.Практикум](https://github.com/yandex-praktikum)

### Технологии:

Python, Flask, flask-sqlalchemy, sqlalchemy, flask-wtf, wtforms

### Подготовка и запуск сервера:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:sofyaserpinskaya/yacut.git

cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить сервер:

```
flask run
```
