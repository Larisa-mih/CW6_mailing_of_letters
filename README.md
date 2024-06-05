<h3 align="center">Сервис рассылки на Django</h3>


## О проекте

Сервис email рассылок. После регистрации вы сможете добавить клиентов, сообщение и создать рассылку,
выбрав дату начала и окончания рассылки и с какой периодичностью производить рассылку.
При наступлении даты отправки происходит автоматическая отправка сообщения вашим клиентам.

## Технологии
- Django
- PostgreSQL
- Redis
- APScheduler


## Настройка проекта

Для работы с проектом произведите базовые настройки.

### 1. Клонирование проекта

Клонируйте репозиторий используя следующую команду.
  ```sh
  git clone https://github.com/Larisa-mih/CW6_mailing_of_letters.git
  ```


### 2. Настройка виртуального окружения и установка зависимостей

Создает виртуальное окружение:
```text
python3 -m venv venv
```

Активирует виртуальное окружение:
```text
source venv/bin/activate          # для Linux и Mac
venv\Scripts\activate.bat         # для Windows
```

Устанавливает зависимости:
```text
pip install -r requirements.txt
```

### 3. Редактирование .env.sample:

- В корне проекта переименуйте файл .env.sample в .env и отредактируйте параметры:
    ```text
  
    # Django
    SECRET_KEY=secret_key - секретный ключ django проекта
    DEBUG=True - режим DEBUG
  
    # Postgresql
    NAME="db_name" - название вашей БД
    USER="postgres" - имя пользователя БД
    PASSWORD="secret" - пароль пользователя БД
    HOST="host" - можно указать "localhost" или "127.0.0.1"
    PORT=port - указываете порт для подключения по умолчанию 5432
  
    # Mailing  
    EMAIL='your_email@yandex.ru' - ваш email yandex
    EMAIL_PASSWORD='your_yandex_smtp_password' - ваш пароль smtp (подробнее о настройке ниже)
    
    # Redis
    CACHE_ENABLED=True - использование кэша
    LOCATION=redis://host:port - данные местоположения redis
    ```
- О настройке почты smtp: 
[Настройка почтового сервиса SMTP ](https://proghunter.ru/articles/setting-up-the-smtp-mail-service-for-yandex-in-django)

### 4. Настройка БД и кэширования:

- Примените миграции:
  ```text
  python manage.py migrate
  ```
  
- Для заполнения базы примените фикстуры:
  ```text
  python manage.py loaddata fixtures/*.json
  ```

- Установите Redis:

  - Linux команда:
   ```text
   sudo apt install redis; 
  или 
  sudo yum install redis;
   ```

  - macOS команда:
   ```text
   brew install redis;
   ```

  Windows инструкция:
  - [Перейти на Redis docs](https://redis.io/docs/install/install-redis/install-redis-on-windows/)


## Использование

- Для запуска проекта наберите в терминале команду:
  ```text
  python manage.py runserver
  ```
  перейдите по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)


- Для запуска автоматической отправки рассылок, необходимо использовать команду запустив рядом с проектом в новом окне:
  ```text
  python manage.py run_apsheduler
  ```
  
- Для ручного запуска рассылок можно использовать команду:
  ```text
  python manage.py run_mailing
  ```