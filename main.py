import requests
import logging
from logging.handlers import RotatingFileHandler

import config
import utils
from schemas import CurrencySchema, ValueSchema
from crud import MainCurrenciesCrud, MainValuesCrud
from database import SessionLocal


class Currency:
    def __init__(self):
        self.session = requests.Session()
        self.db_session = SessionLocal()
        self.currency_crud: MainCurrenciesCrud = MainCurrenciesCrud(session=self.db_session)
        self.value_crud: MainValuesCrud = MainValuesCrud(session=self.db_session)
        self.base_value = float()
        self.msg = []
        self.check = False
        self.items_count = 0

    def start(self):
        if utils.is_holiday():
            return
        currencies_xml = self.get_currency_xml()
        currencies_list = utils.convert_xml_to_list(currencies_xml)
        for currency in currencies_list:
            self.parse_currency(currency)
        message = utils.make_msg(self.msg)
        if self.check:
            utils.send_to_tg(message)

    def get_currency_xml(self):
        params = {'fdate': utils.today_is('%d.%m.%Y')}
        response = self.session.get(config.URL, params=params)
        return response.text

    def parse_currency(self, currency: dict):
        currency_obj = CurrencySchema(code=currency['title'], quant=currency['quant'], name=currency['fullname'])
        value_obj = ValueSchema(value=currency.get('description'))
        self.check_data_from_db(currency_obj, value_obj)

    def check_data_from_db(self, currency_obj: CurrencySchema, value_obj: ValueSchema):
        self.items_count += 1
        code = self.currency_crud.get_or_create(currency_obj)
        value_obj.currency_id = code.id
        last_currency = self.value_crud.get_last_currency(code.id)
        if last_currency:
            percent = utils.get_percentage(float(value_obj.value), float(last_currency.value))
            value_obj.percent = percent
        if currency_obj.code in config.CURRENCIES and (not last_currency or value_obj.percent != 0):
            self.value_crud.insert(value_obj)
            self.msg.append(utils.make_project_msg(currency_obj, value_obj, last_currency.value))
            self.check = True


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[RotatingFileHandler('currency.log', mode='a+', maxBytes=10485760, backupCount=2, encoding='utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    Currency().start()
