# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

## Установка Postgres
### Windows
[Скачайте](https://www.postgresql.org/download/windows/) PostgresQL,
[установите](https://winitpro.ru/index.php/2019/10/25/ustanovka-nastrojka-postgresql-v-windows/).
Задайте пароль пользователя `postgres`. Создайте базу данных.

### Linux
```bash
sudo apt update
# Установите СУБД PostgreSQL:
sudo apt -y install postgresql
# После установки СУБД откройте терминал и переключитесь на пользователя postgres с помощью команды:
sudo -i -u postgres
# Создаём базу
createdb starburgerdb
# Задаём пароль пользователю postgres
psql
\password postgres
Enter new password:
# вводим пароль
```


## Подключение базы данных Postgres к проекту Django
```python
# star_burger/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'starburgerdb',
        'USER': 'postgres',
        'PASSWORD': '<пароль пользователя postgres>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Переменные окружения

В каталоге `star_burger/` создайте файл `.env` и заполните его следующими строковыми данными:
```
SECRET_KEY=<Секретный ключ Django-проекта>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, loclhost
```

[Получите ключ](https://dvmn.org/encyclopedia/api-docs/yandex-geocoder-api/) для Яндекс Geo-API и добавьте в ваш
`.env`-файл строку
```
YANDEX_GEOCODER_API=<ваш ключ>
```

Выполните миграции:
```sh
python manage.py migrate
```

Создайте суперпользователя Django:
```sh
python manage.py createsuperuser
```

Запустите сервер:
```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран.
Переходите к следующему разделу README.

### Сборка фронтенда

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух
программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver`
откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что `Node.js` и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет
их версии:
```sh
nodejs --version
# v12.18.2
# Если ошибка, попробуйте node:
node --version
# v12.18.2

npm --version
# 6.14.5
```

Версия `nodejs` должна быть не младше 10.0. Версия `npm` не важна. Как обновить Node.js читайте
в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты `Node.js`.
Получится аналог виртуального окружения как для Python, но для `Node.js`

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений,
похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и
совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. `Parcel` будет работать в фоне и
следить за изменениями в JS-коде.

*nix:
```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Windows:
```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд.
О готовности вы узнаете по сообщению в консоли:
```
√ Built in 10.89s
```

`Parcel` будет следить за файлами в каталоге `bundles-src`.
Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует.
Затем `Parcel` перейдёт в каждый из этих подключенных файлов и узнает что импортируют они.
И так далее, пока не закончатся файлы. В итоге `Parcel` получит полный список зависимостей.
Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`.
Они полностью самодостаточно и потому пригодны для запуска в браузере.
Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/),
то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда `Parcel` складывает результаты своей работы.
Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория
с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать
файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта,
когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию.
В норме `Parcel` решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и
предупреждает JS-код в браузере о необходимости подтянуть свежий код.
Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша,
жмите <kbd>Ctrl-F5</kbd>.

## Как запустить prod-версию сайта
Соберите фронтенд:
```sh
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```

Настройте бэкенд: создайте файл `.env` в каталоге `star_burger/` со следующими строками:
- `DEBUG=False` — выключение режима отладки.
- `SECRET_KEY` — секретный ключ Django-проекта. Он отвечает за шифрование на сайте.
В частности, им зашифрованы все пароли на вашем сайте.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)

[Получите ключ](https://dvmn.org/encyclopedia/api-docs/yandex-geocoder-api/) для Яндекс Geo-API и добавьте в ваш
`.env`-файл строку
```
YANDEX_GEOCODER_API=<ваш ключ>
```

## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:
- Второй урок [учебного модуля Django](https://dvmn.org/modules/django/)

# deploy-скрипт для сервера
Для быстрого применения на сервере изменений в репозитории выполните скрипт `/opt/star-burger/deploy_star_burger.sh`

Он вытягивает изменения с репозитория, устанавливает зависимости, накатывает миграции, собирает фронтенд, статику и
перезапускает сайт.

# Работающий сайт, расположенный на внешнем хостинге - [star-burger.redbor.ru](https://star-burger.redbor.ru/)
