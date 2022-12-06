import os
from dotenv import load_dotenv, find_dotenv
from requests.structures import CaseInsensitiveDict


load_dotenv(find_dotenv())


TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
TG_CHANNEL_ERROR = os.getenv('TG_CHANNEL_ERROR')

URL = 'https://nationalbank.kz/rss/get_rates.cfm'
URL_HOLIDAYS = 'https://raw.githubusercontent.com/daradan/production_calendar_kz/main/kz_holidays_2.json'

CURRENCIES = ['USD', 'EUR', 'RUB', 'CAD', 'AED', 'CNY', 'KRW', 'UZS', 'KGS']
