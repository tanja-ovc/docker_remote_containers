# Docker YaMDB Remote

### Проект YamDB с инфраструктурой для деплоя на удалённом сервере

![example workflow](https://github.com/tanja-ovc/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

- Данный проект посвящен созданию инфраструктуры для деплоя __на удалённом сервере__ уже существующего проекта YaMDB (https://github.com/tanja-ovc/api_yamdb_group_project).

_Примечание:_ на данный момент удалённый сервер на Яндекс.Облаке, где я размещала проект, не работает в связи с истечением гранта на использование виртуальной машины.

### Описание

Что я делала, чтобы развернуть проект YaMDB на удалённом сервере (использовалась виртуальная машина на Яндекс.Облаке):

Действия с удалённым сервером:

 - Установила Docker (```sudo apt install docker.io``` для Linux) и docker-compose (https://docs.docker.com/compose/install/) на свой сервер.

- Скопировала файлы _docker-compose.yaml_ и _nginx/default.conf_ из данного проекта на сервер в _home/<мой_username>/docker-compose.yaml_ и _home/<мой_username>/nginx/default.conf_ соответственно.

__!__ NB: Если на сервере установлен веб-сервер nginx, нужно предварительно __остановить его работу__.

- Добавила в Secrets GitHub Actions данного репозитория переменные окружения для работы базы данных:

  DOCKER_USERNAME - мой юзернейм на Docker Hub

  DOCKER_PASSWORD - мой пароль на Docker Hub

  HOST - IP моего удалённого сервера

  USER - мой юзернейм для подключения к удалённому серверу

  SSH_KEY - private key компьютера, имеющего доступ по SSH к удалённому серверу (это нужно для того, чтобы удалённый сервер опознал сервер GitHub Actions как тот, который имеет право на подключение)

  _Примечание:_ в случае, если SSH-key создан с прилагающимся паролем, нужно создать также переменную PASSPHRASE, которая и будет содержать пароль, а в код файла _yamdb\_workflow.yml_ в ```deploy``` добавить ```passphrase: ${{ secrets.PASSPHRASE }}``` таким образом:
          
  ```
  deploy:
    runs-on: ubuntu-latest
    needs: build_and_push_to_docker_hub
    steps:
      - name: executing remote ssh commands to deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USER }}
          key: ${{ secrets.SSH_KEY }}
          passphrase: ${{ secrets.PASSPHRASE }}
          script: ...
  ```

  Значения для переменных окружения DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT берутся из файла _infra/.env_

  TELEGRAM_TO - мой ID в Telegram (узнать свой ID можно с помощью бота @userinfobot в Telegram)

  TELEGRAM_TOKEN - токен бота в Telegram, отправляющего мне сообщение об успешном осуществлении workflow (о том, как создать бота и узнать его токен, здесь: https://core.telegram.org/bots#6-botfather)

Workflow запускатется при каждом пуше (git push) в репозиторий: запускаются тесты и происходит обновление Docker образа с последующей его загрузкой на Docker Hub.

В случае, если пуш будет происходить в ветку master, будет запускаться также деплой проекта на удалённом сервере и осуществляться отправка сообщения об успешном осуществлении workflow в мой Telegram.

После успешного деплоя я выполнила по очереди следующие команды внутри контейнера web (выполнить миграции, собрать статику, создать суперпользователя):

```sudo docker-compose exec web python manage.py migrate```

```sudo docker-compose exec web python manage.py collectstatic```

```sudo docker-compose exec web python manage.py createsuperuser```

Документация проекта будет доступна по адресу http://<IP_сервера>/redoc/

Админка: http://<IP_сервера>/admin/

Заполнение БД прилагающимися данными в формате ```.csv``` я производила с помощью команды

```sudo docker-compose exec web python manage.py import_data```


### Авторство

Автор инфраструктуры: Татьяна Овчинникова

Авторство разворачиваемого проекта YaMDB принадлежит команде из трёх человек (включая меня). Подробнее можно прочитать в README проекта YaMDB: https://github.com/tanja-ovc/api_yamdb_group_project.
