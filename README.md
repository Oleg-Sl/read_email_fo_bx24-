## 1. Приложение "Создание сделки на основе входящего письма электронной почты"

Описание.
Приложение читает письма с почтового ящика и создает на основе каждого из них сделку в Битрикс24. Приложение запускается планировщиком операционной системы cron. 
В сделку добавляются следующие данные из письма:
- тема;
- тело;
- email;
- вложения (т.е. приложенные файлы к письму).

Файлы и директории приложения:
- get_mail_and_create_deal - логика приложения;
- logs/print - логи;
- run_mail.py - файл запуска приложения;
- script_mail.sh - скрипт для запуска приложения планировщиком cron.

Установка:
- склонировать репозиторий на ваш сервер;
- в директории проекта выполнить команды:
  - python3 -m venv env
  - source env/bin/activate
  - pip install -r requirements .txt
- в директории проекта создать файл "secrets.json" с содержимым:
  {
      "server": <адрес_вашего_почтового_сервера>,
      "username": <логин_вашего_почтового_сервера>,
      "password": <пароль_вашего_почтового_сервера>,
      "webhook": <входящий_вебхук_вашего_портала_битрикс(с_правом_доступа_к_CRM)>,
      "countmail": <текуший_номер_письма(порядковый_номер_письма_в_почте)>
  };
- в функции "create_deal" файла "get_mail_and_create_deal/mail_input.py" изменить имена полей на поля вашего Биртикс:
  - тема письма - тип поля "строка";
  - тело письма - тип поля "строка";
  - ID сделки связанного с письмом - тип поля "число";
  - email - тип поля "строка"; 
  - ID контакта - тип поля "строка"; 
  - вложения из почты - тип поля "файл" множественное;
- в файле "script_mail.sh" изменить значение переменной "MY_WORK_DIR" на полный путь к вашему приложению;
- выполнить команду - chmod +x script_mail.sh;
- добавить задание в планировщик cron:
  - вызвать команду - crontab -e
  - добавить задание в этот файл - #*/<задержка_в_минутах_между_запусками> * * * * <полный_путь_к_файлу_script_mail.sh>

## 2. Приложение "Добавление рейтинга из серсиса sipuni в сделку Битрикс24"

Описание.
Приложение получает данные звонков из Sipuni и сохраняет рейтинг и язык поставленный клиентом в текущую (активную/в работе) сделку Биртрикс24 связанную с данным клиентом. Приложение запускается планировщиком операционной системы cron.

Файлы и директории приложения:
- get_and_save_raiting_calls - логика приложения;
- logs/rating - логи;
- run_rating.py - файл запуска приложения;
- script_rating.sh - скрипт для запуска приложения планировщиком cron.

Установка:
- склонировать репозиторий на ваш сервер;
- в директории проекта выполнить команды:
  - python3 -m venv env
  - source env/bin/activate
  - pip install -r requirements .txt
- в директории проекта создать файл "secrets.json" с содержимым:
  {
      "sipuni_user": <логин_пользователя_sipuni>,
      "sipuni_token": <пароль_пользователя_sipuni>,
      "webhook": <входящий_вебхук_вашего_портала_битрикс(с_правом_доступа_к_CRM)>,
  };
- в функции "get_language_id_by_name" файла "get_and_save_raiting_calls/services.py" изменить значения переменных:
  - FIELD_LANGUAGE_KAZ - идентификатор значения "Каз" поля "Язык" в Битрикс;
  - FIELD_LANGUAGE_RUS - идентификатор значения "Рус" поля "Язык" в Битрикс;
- в функции "save_rating_to_bx24" файла "get_and_save_raiting_calls/rating.py" изменить значения:
  - FIELD_DEAL_RATING - имя поля "Рейтинг" в Битрикс24 (текст или число);
  - FIELD_DEAL_LANGUAGE - имя поля "Язык" в Битрикс24 (списочное);
  - COLS_CSV - номера колонок файла со статистикой из Sipuni:
    - direction - колонка с нправлением звонка (вход./исход.); 
    - from_phone - колонка с номером кто звонил; 
    - to_phone - колонка с номером кому звонили;
    - rating - колонка с рейтингом поставленного клиентом; 
    - language - колонка с языком клиента.
- в файле "script_rating.sh" изменить значение переменной "MY_WORK_DIR" на полный путь к вашему приложению;
- выполнить команду - chmod +x script_rating.sh;
- добавить задание в планировщик cron:
  - вызвать команду - crontab -e
  - добавить задание в этот файл - #*/<задержка_в_минутах_между_запусками> * * * * <полный_путь_к_файлу_script_rating.sh>

