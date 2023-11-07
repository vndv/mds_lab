# Airflow


## 1.3.1 Установка

Создадим рабочий каталог для Airflow и внутри него virtualenv каталог Python 3. Дальше мы подразумеваем что это виртуальное окружение имеет название `afenv`.

```bash
$ mkdir ~/airflow
$ cd ~/airflow
$ virtualenv -p /usr/bin/python3 afenv
$ source afenv/bin/activate
(afenv) $ python -V
3.10.6
```

Установим Airflow в созданный virtualenv  

```bash
(afenv) $ pip install apache-airflow==2.2.5
```

Рабочая версия: 2.2.5 Тестировалось все на ней и системном Python3, Ubuntu 20.04. Вторая версия отличается от 1 в существенных для нас моментах, поэтому важно использовать именно вторую версию инструмента.


Нам нужно создать каталог для всех служебных файлов Airflow, где будут так же располагаться DAG-файлы и плагины Airflow. После создания каталога установим переменную среды `AIRFLOW_HOME`.  

```bash
(afenv) $ mkdir airflow_home
(afenv) $ export AIRFLOW_HOME=`pwd`/airflow_home
```
Теперь выполните команду, которая будет создавать и инициализировать базу данных Airflow:  

```bash
(afenv) $ cd $AIRFLOW_HOME
(afenv) $ airflow db init
```
Если команда отработала, то Airflow создал свой конфигурационный файл `airflow.cfg` в `AIRFLOW_HOME`:

```bash
(afenv) $ ls $AIRFLOW_HOME
airflow.cfg  airflow.db  logs  webserver_config.py
```

Нам нужна эта переменная потому что любая команда которая имеет дело с airflow идёт смотреть в окружение и есть ли там переменная `AIRFLOW_HOME`. Если переменной нет, то airflow идёт в папку `~/airflow` (т.е. например `/home/ubuntu/airflow`) и ищет там конфиг. Если такой папки нет то он её создаст. Хорошей практикой является определять эту переменную окружения даже если мы в итоге будем использовать дефолтный путь.

Проверим установился ли Airflow:  

```bash
(afenv) $ airflow version
2.2.5
```

Запустим веб-приложение Airflow:  

```
(afenv) $ airflow webserver -p 8081
```

Теперь можно посетить веб-приложение Airflow в браузере на порту 8081 `<your-ip:8081>`. Заметьте, что мы использовали 8081 вместо дефолтного 8080, чтобы избежать конфликта с как-нибудь другим сервисом который может его захотеть. Чекер будет искать Airflow именно на этом порту по умолчанию, но это можно будет исправить.


В отдельном окне запустите airflow scheduler:  

```bash
$ export AIRFLOW_HOME=/home/ubuntu/airflow/airflow_home
$ source /home/ubuntu/airflow/afenv/bin/activate
(afenv) $ airflow scheduler
```

## 1.3.2 Настройка конфигурации

Добавьте установку значения переменной `AIRFLOW_HOME` в файл `~/.bash_profile`
```bash
echo "export AIRFLOW_HOME=/home/ubuntu/airflow/airflow_home" >> ~/.bash_profile
```
Чтобы изменения вступили в силу необходимо выполнить source ~/.bash_profile, если вы вызовете комаду `echo $AIRFLOW_HOME` вы должны увидеть 
```
/home/ubuntu/airflow/airflow_home
```

Теперь давайте настроим порт и авторизацию пользователей в конфиг файле. Но прежде чем вносить изменения в конфиг - забэкапьте его:
```bash
sudo cp $AIRFLOW_HOME/airflow.cfg $AIRFLOW_HOME/airflow.cfg_bak
```
Проверьте, что файл скопировался:
```bash
$ head $AIRFLOW_HOME/airflow.cfg_bak

[core]
# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository. This path must be absolute.
dags_folder = /home/ubuntu/airflow/airflow_home/dags

# Hostname by providing a path to a callable, which will resolve the hostname.
# The format is "package.function".
#
# For example, default value "socket.getfqdn" means that result from getfqdn() of "socket"
# package will be used as hostname.
```


Откройте `airflow.cfg`, например при помощи `sudo vim $AIRFLOW_HOME/airflow.cfg` или `sudo nano $AIRFLOW_HOME/airflow.cfg` (кому чем привычнее), и измените настройки:  

### в секции `[webserver]`:
* замена дефолтного 8080, который в конфликте с чем-нибудь.
* `web_server_port = 8081`


После чего снова проинициализируйте перезапустите веб-приложение и scheduler. Чтобы проверить, подцепились ли изменения и что Webserver Airflow стартанул на порту 8081 в отдельно терминале выполните
```bash
$ source /home/ubuntu/airflow/afenv/bin/activate
$ airflow config get-value webserver web_server_port
```

## 1.3.3 Учётные записи

Создайте своего пользователя-админа с сильным паролем (назначьте свой пароль!)

```bash
$ source /home/ubuntu/airflow/afenv/bin/activate
(afenv) $ airflow users create -r Admin -u admin -f Name -l Surname -e admin@example.com -p 'Sae6ieZu'
```

Теперь можете залогиниться с этим юзером в UI на порту 8081.  


## 1.3.4 Запуск и останова

Запуск выполняется в отдельных окнах.
Веб-приложение:

```bash
$ source /home/ubuntu/airflow/afenv/bin/activate
(afenv) $ airflow webserver
```

Scheduler:  
```bash
$ export AIRFLOW_HOME=/home/ubuntu/airflow/airflow_home
$ source /home/ubuntu/airflow/afenv/bin/activate
(afenv) $ airflow scheduler
```

Для остановки веб-приложения и scheduler выполнить Ctrl+C в соответствующем окне.

Чтобы они не "выключались" при отсоединении от сервера, можно установить себе tmux и запускать webserver/scheduler в них

* [Краткая шпаргалка по tmux](https://eax.me/tmux/)
* [Gentle introduction to tmux](https://medium.com/hackernoon/a-gentle-introduction-to-tmux-8d784c404340)


