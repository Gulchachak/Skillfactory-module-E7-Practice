В данном приложении реализован сервис Доска объявлений.

Это приложение использует Flask в качестве фреймворка для приложения, MongoDB для хранения данных.

Для запуска на локальной машине необходимо:

  склонировать этот репозиторий

  перейти в папку репозиторием

  python -m venv venv

  pip install -r requirements.txt

  python app.py

В данном приложении доступы следующие эндпоинты:

/new_advert - создание нового объявления

/new_tag - добавление тега к существующему объявлению по ID

/new_comment - добавление комментария к существующему объявлению по ID

/<:id> - получение существующего объявления (с тегами и комментариями) по ID

/stats/<:id> - статистика для объявления по ID


