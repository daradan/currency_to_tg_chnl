from typing import Union
from sqlalchemy.orm import Session
from models import CurrencyModel, ValueModel
from schemas import CurrencySchema, ValueSchema


class Crud:
    def __init__(self, session: Session, schema):
        self.session = session
        self.schema = schema

    def get(self, pk):
        return self.session.get(self.schema, pk)

    def update(self, data):
        self.session.query(self.schema).filter_by(id=data['id']).update(**data)

    def delete(self, pk):
        self.session.query(self.schema).filter_by(id=pk).delete()

    def insert(self, data: Union[CurrencySchema, ValueSchema]):
        obj = self.schema(**data.dict())
        self.session.add(obj)
        self.session.commit()
        return obj


class CurrenciesCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    def get_by_code(self, code):
        return self.session.query(self.schema).filter_by(code=code).first()

    def get_or_create(self, new_code: CurrencySchema):
        obj = self.get_by_code(new_code.code)
        if obj:
            return obj
        return self.insert(new_code)


class ValuesCrud(Crud):
    def __init__(self, session: Session, schema):
        super().__init__(session, schema)

    def get_last_currency(self, currency_id: int):
        return self.session.query(self.schema).filter_by(currency_id=currency_id).order_by(self.schema.id.desc()).first()


class MainCurrenciesCrud(CurrenciesCrud):
    def __init__(self, session: Session):
        super().__init__(session, CurrencyModel)


class MainValuesCrud(ValuesCrud):
    def __init__(self, session: Session):
        super().__init__(session, ValueModel)
