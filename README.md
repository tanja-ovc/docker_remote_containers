# API для YaMDb (+ инфраструктура)

![example workflow](https://github.com/tanja-ovc/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### API

API для платформы YaMDb. Version 1.
Проект на данный момент развёрнут на сервере 51.250.12.20. Документация доступна по адресу http://51.250.12.20/redoc/.

### Инфраструктура

Проект содержит в себе всё необходимое для разворачивания на удалённом сервере с помощью Docker-контейнеров.
Для успешного разворачивания проекта на своём удалённом сервере выполните следующие действия:

 - Если на вашем сервере установлен веб-сервер nginx, остановите его работу.

 - Установите Docker (```sudo apt install docker.io``` для Linux) и docker-compose (https://docs.docker.com/compose/install/).

- Скопируйте файлы _docker-compose.yaml_ и _nginx/default.conf_ из данного проекта на ваш сервер в _home/<ваш_username>/docker-compose.yaml_ и _home/<ваш_username>/nginx/default.conf_ соответственно.

- Добавьте в Secrets GitHub Actions вашего репозитория переменные окружения для работы базы данных:

  DOCKER_USERNAME - ваш юзернейм на Docker Hub
  DOCKER_PASSWORD - ваш пароль на Docker Hub

  HOST - IP вашего удалённого сервера
  USER - юзернейм для подключения к удалённому серверу
  SSH_KEY - private key компьютера, имеющего доступ по SSH к удалённому серверу (это нужно для того, чтобы ваш удалённый сервер опознал сервер GitHub Actions как тот, который имеет право на подключение)

  В случае, если ваш SSH-key создан с прилагающимся паролем, создайте также переменную PASSPHRASE, которая и будет содержать пароль, а в код файла _yamdb\_workflow.yml_ в ```deploy``` добавьте ```passphrase: ${{ secrets.PASSPHRASE }}``` таким образом:
  ```deploy:```
      ```runs-on: ubuntu-latest```
      ```needs: build_and_push_to_docker_hub```
      ```steps:```
        ```- name: executing remote ssh commands to deploy```
          ```uses: appleboy/ssh-action@master```
          ```with:```
            ```host: ${{ secrets.HOST }}```
            ```sername: ${{ secrets.USER }}```
            ```key: ${{ secrets.SSH_KEY }}```
            ```passphrase: ${{ secrets.PASSPHRASE }}```
            ```script: ...```

  Значения для переменных окружения DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT возьмите из файла _infra/.env_

  TELEGRAM_TO - ваш ID в Telegram (узнать можно с помощью бота Userinfobot в Telegram: https://github.com/nadam/userinfobot)
  TELEGRAM_TOKEN - токен бота в Telegram, который будет отправлять вам сообщение об успешном осуществлении workflow (узнать можно с помощью бота BotFather в Telegram)

Workflow будет запускаться при каждом пуше (git push) в ваш репозиторий: будут запускаться тесты и будет происходить обновление Docker образа с последующей его загрузкой на Docker Hub.
В случае, если пуш будет происходить в ветку master, будет запускаться также деплой проекта на вашем удалённом сервере и осуществляться отправка сообщения об успешном осуществлении workflow вам в Telegram.

После успешного деплоя выполните по очереди следующие команды внутри контейнера web:

```sudo docker-compose exec web python manage.py migrate```
```sudo docker-compose exec web python manage.py collectstatic```

Если вы хотите создать суперпользователя, выполните
```sudo docker-compose exec web python manage.py createsuperuser```

Документация проекта будет доступна по адресу http://<IP_вашего_сервера>/redoc/
Админка: http://<IP_вашего_сервера>/admin/

Заполнение БД прилагающимися данными в формате ```.csv``` можно произвести с помощью команды
```sudo docker-compose exec web python manage.py import_data```


### Авторы

_Алексей Борисов - автор системы регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail (ноябрь 2021)._

_Татьяна Овчинникова - автор системы работы с категориями, жанрами и произведениями: модели, представления и эндпойнты для них (ноябрь 2021); автор кода инфраструктуры (январь 2022)._

_Василий Кузьминых - автор системы отзывов и комментариев: модели, представления, эндпойнты, рейтинги произведений. Инициатор разработки и автор manage-команды для внесения данных из файлов формата .csv в существующую базу данных (ноябрь 2021)._