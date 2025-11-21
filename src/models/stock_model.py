from .abstract_model import abstract_model
from Models.nomenclature_model import nomenclature_model
from Models.range_model import range_model
from Models.nomenclature_model import nomenclature_model
from Core.validator import validator, argument_exception
from Models.storage_model import storage_model
from Dto.stock_dto import stock_dto
from datetime import datetime
# Модель остатков товаров
class stock_model(abstract_model):
    __nomenclature:nomenclature_model
    __range:range_model
    __storage:storage_model
    __num:float

    def __init__(self):   
        super().__init__()
    
    """
    Единицы измерения количества номенклатуры
    """
    @property
    def range(self):
        return self.__range
    
    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    """
    Вид номенклатуры
    """
    @property
    def nomenclature(self):
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    """
    Остаток
    """
    @property
    def num(self) -> float:
        return self.__num
    
    @num.setter
    def num(self, value: float):
        validator.validate(value,float)
        self.__num = value
    
    """
    Склад
    """
    @property
    def storage(self) -> storage_model:
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value,storage_model)
        self.__storage = value
    

    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(nomenclature:nomenclature_model, range:range_model, storage:storage_model, num:float):
        item = stock_model()
        item.range = range
        item.nomenclature = nomenclature
        item.num = num
        item.storage=storage
        return item
    
    """
    Фабричный метод в Dto
    """
    def to_dto(self):
        item = stock_dto()
        item.nomenclature_id=self.nomenclature.id
        item.range_id = self.range.id
        item.num = self.num
        item.num = self.num
        item.storage_id = self.storage.id
        return item

    def __repr__(self):
        return "Stock "+super().__repr__()

    
