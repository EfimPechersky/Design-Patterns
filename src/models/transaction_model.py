from .abstract_model import abstract_model
from Core.validator import validator
from Core.repository import repository
from .nomenclature_model import nomenclature_model
from.storage_model import storage_model
from .range_model import range_model
from Dto.transaction_dto import transaction_dto
from datetime import datetime
"""Класс, описывающий транзакции"""
class transaction_model(abstract_model):
    __date:datetime=None
    __nomenclature:nomenclature_model=None
    __storage:storage_model=None
    __num:float=0
    __range:range_model=None

    def __init__(self):
        super().__init__()

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        validator.validate(value,datetime)
        self.__date = value
    
    @property
    def nomenclature(self):
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value):
        validator.validate(value,nomenclature_model)
        self.__nomenclature = value
    
    @property
    def storage(self):
        return self.__storage

    @storage.setter
    def storage(self, value):
        validator.validate(value,storage_model)
        self.__storage = value
    
    @property
    def num(self):
        return self.__num

    @num.setter
    def num(self, value):
        validator.validate(value,float)
        self.__num = value
    
    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value):
        validator.validate(value,range_model)
        self.__range = value

    """Фабричный метод создания экземпляра класса транзакция"""
    @staticmethod
    def create(date,nomenclature,storage,num,range):
        item=transaction_model()
        item.date=date
        item.nomenclature=nomenclature
        item.storage=storage
        item.num=num
        item.range = range
        return item
    
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:transaction_dto, cache:dict):
        validator.validate(dto, transaction_dto)
        validator.validate(cache, dict)
        nomenclature = cache[dto.nomenclature_id]
        range = cache[dto.range_id]
        storage = cache[dto.storage_id]
        date=datetime.strptime(dto.date, "%d-%m-%Y")
        item= transaction_model.create(date,nomenclature,storage,dto.num,range)
        item.id=dto.id
        return item
    
    """Фабричный метод в Dto"""
    def to_dto(self):
        item = transaction_dto()
        item.id=self.id
        item.nomenclature_id=self.nomenclature.id
        item.range_id=self.range.id
        item.storage_id=self.storage.id
        item.num=self.num
        item.date=self.date
        return item
    
    def __repr__(self):
        return "Transaction "+super().__repr__()


