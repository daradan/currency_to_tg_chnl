import config
from schemas import CurrencySchema, ValueSchema

import requests
import logging
import time
from datetime import datetime
import xmltodict


def today_is(date_format: str) -> str:
    return datetime.today().strftime(date_format)


def convert_xml_to_list(xml_data: str) -> list:
    converted = xmltodict.parse(xml_data)['rates']['item']
    return converted


def make_project_msg(cur_obj: CurrencySchema, value_obj: ValueSchema, previous: str) -> str:
    msg = ''
    float_cur = float(value_obj.value)
    float_prev = float(previous)
    if float_cur > float_prev:
        msg += f"⬆ {cur_obj.code} {cur_obj.quant} - {float_cur} ({float_prev})"
    elif float_cur < float_prev:
        msg += f"⬇ {cur_obj.code} {cur_obj.quant} - {float_cur} ({float_prev})"
    elif float_cur == float_prev:
        msg += f"↔ {cur_obj.code} {cur_obj.quant} - {float_cur}"
    if value_obj.percent >= 5:
        msg += f" ‼️"
    elif value_obj.percent <= -5:
        msg += f" ✅"
    return msg


def make_msg(msg: list) -> str:
    message = '\n'.join(msg)
    message += f"\n\n{config.TG_CHANNEL}"
    return message


def get_percentage(current: float, previous: float) -> int:
    if current < previous:
        current, previous = previous, current
    return round(int(((current - previous) / current) * 100))
    # a < b = ((b - a) / a) * 100
    # a > b = ((a - b) / a) * 100


def is_holiday() -> bool:
    today = int(today_is('%Y%m%d'))
    holiday = requests.get(config.URL_HOLIDAYS).json()
    if today in holiday.get('holidays'):
        return True
    return False


def send_to_tg(message: str):
    url = f'https://api.telegram.org/bot{config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': config.TG_CHANNEL,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"TG MSG: {data}")
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_error(message)


def send_error(message):
    url = f'https://api.telegram.org/bot{config.TG_TOKEN}/sendMessage'
    params = {
        'chat_id': config.TG_CHANNEL_ERROR,
        'text': message
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        data = r.json()
        logging.info(f"TG ERROR: {data}")
        time_to_sleep = data['parameters']['retry_after']
        time.sleep(time_to_sleep)
        send_error(message)


if __name__ == '__main__':
    print(is_holiday())
