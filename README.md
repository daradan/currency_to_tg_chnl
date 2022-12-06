## Скрейпинг курсов валют с Национального банка Казахстана
Работу скрипта можно посмотреть тут:
- [Курс тенге](https://t.me/kursKZT)

Скрипт скрейпит (парсит) сайт Национального банка Казахстана и добавляет в БД информацию о курсах валют. При следующем запуске проверяет курс, и в случае изменения курса добавляет новый курс в БД. Если курс изменен, то отправляет на Telegram-канал.

### Установка и настройка
Клонируем репозитории
```
git clone https://github.com/daradan/currency_to_tg_chnl.git
```
Устанавливаем библиотеки
```
pip install -r requirements.txt
```
Создаем файл ___.env___ и заполняем свои данные
```
TG_TOKEN=...
TG_CHANNEL=@...
TG_CHANNEL_ERROR=...
```

## Scraping exchange rates from the National Bank of Kazakhstan
The work of the script can be seen here:
- [KZT exchange rate](https://t.me/kursKZT)

The script scrapes (parses) the site of the National Bank of Kazakhstan and adds information about exchange rates to the database. At the next launch it checks the exchange rate and adds a new rate to the database in case of exchange rate changes. If the rate is changed, it sends it to the Telegram-channel.

### Installation and setup
Clone repositories
```
git clone https://github.com/daradan/currency_to_tg_chnl.git
```
Installing libraries
```
pip install -r requirements.txt
```
Create file ___.env___ and fill in your data
```
TG_TOKEN=...
TG_CHANNEL=@...
TG_CHANNEL_ERROR=...
```
