from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Float
from sqlalchemy.orm import relationship

from database import Base, engine


class CurrencyModel(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    quant = Column(Integer)

    values = relationship('ValueModel', back_populates='currency')


class ValueModel(Base):
    __tablename__ = 'value'
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    value = Column(String, nullable=False)
    percent = Column(Float)
    currency_id = Column(Integer, ForeignKey(CurrencyModel.id))

    currency = relationship('CurrencyModel', back_populates='values')


Base.metadata.create_all(engine)
