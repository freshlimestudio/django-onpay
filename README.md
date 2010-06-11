# django-onpay

## Что это?

Как видно из названия, это приложение для работы с платежной системой
<http://onpay.ru/> для сайта, построенного на фреймворке джанго.

Пользователи других фреймворков или своих велосипедов на python (svarga,
pylons, turbogears, web.py, etc) могут написать своё приложение, специально
для этого основная функциональность собрана в файле `common.py`.
Фреймворко-зависимую часть (запросы, систему хранения, обработку форм,
оповещение менеджеров) естественно придётся переписать, взяв за основу
текущий код.

## Как работает onpay?

Все просто, надо:

 1. Сгенерировать тег `iframe` из множества параметров. В этом поможет
    класс `IframeGenerator`.
 2. Принять запрос от сервиса, который и скажет, кому и сколько денег положили
    и собственно внести сумму в базу данных.

## Установка

 1. Если на сервере стоит python 2.5 или ниже, надо установить python-lxml
 1. Снимаем mercurial-репозиторий,
 1. делаем симлинк директории onpay в site-packages,
 1. прописываем `onpay` в `INSTALLED_APPS`,
 1. `./manage.py syncdb`
 1. в `settings.py` добавляем переменную `ONPAY` с минимумом настроек (см. ниже),
 1. добавляем в `urls.py`: `('^onpay/', include('onpay.urls')),`,
 1. тестируем работу.

## Настройка

Все параметры хранятся в словаре `ONPAY` в файле `settings.py`.

Обязательные параметры (без комментариев):

    ONPAY = {
        'onpay_login': 'example',
        'private_code': 'ksjgJskLJds',
    }

Необязательные параметры:

        "url_success": "http://example.org/onpay/api/",
        # default: то что задано в настройках на сайте onpay
        "use_balance_table": True,
        # записывать в таблицу баланса. Без нее если честно не пробовал
        "pay_mode": "fix",
        # 'free' - обновление баланса, юзер может изменить цифру
        # 'fix' - фиксированный платеж, цифра в фрейме только для чтения
        "f": None,
        # скин, возможные значения - None, 1, 2, 3
        # в зависимости от скина
        # подробнее: http://onpay.ru/form/
        "enable_email_notify": None,
        # если включить опцию, при платежах будет отправлен email
        # через функцию email_managers
        "enable_footman_update_balance": None,
        # это только для примера и включать ни в коем случае нельзя!
        # при получении платежа накидывается баланс на счет пользователя
        # из профиля другого приложения (не путать с таблицей Balance)
        # по аналогии стоит написать свою функцию и подключить через сигнал,
        # если вам требуется хранить счет пользователя в другом месте
        "new_operation_status": 0,
        # опция довольно бесполезная, оставил так как была в рхршных примерах
        "debug": None,
        # на данный момент отправляет через mail_admins запрос от onpay

Чтобы встроить платежную систему в свой дизайн надо переопределить шаблоны
из папки onpay. Надеюсь с этим справитесь без проблем.

Можно вместо include в urls.py прописать свои роуты к своим views,
если требуется какие-то изменения.

Можно поменять параметры после инициализации IframeGenerator:

    iframe_generator = IframeGenerator()
    iframe_generator.set_f(3)
    iframe_generator.width = 100500
    iframe_generator.pay_mode = "free"

После оплаты отправляется сигнал `onpay.signals.refilled_balance`,
если на него подписать свою функцию, можно добиться любой функциональности.
Примеры смотрите в файле `signals.py`.

Ну и, наконец, можно изменить исходные тексты и прислать hg патчи мне
- по возможности добавлю в репозиторий. Комментарии писались по большей части
на русском, так как сама платежная система русская.

## To-Do

То, что хотелось бы сделать (но врядли у меня дойдут руки до этого,
"и так работает"):

 1. Опция для английского языка фрейма
 1. Более качественная поддержка fix платежей (я концентрировался на free)
 1. Поддержка скинов для одной валюты
 1. Добавить сигналы на все случаи жизни
 1. Сделать `setup.py` и установку через `pip`
 1. Автоматические тесты
 1. Еще несколько фич, которые в данный момент не помню

Автор: Денис Бурый <denger@footter.com>

Лицензия: BSD
