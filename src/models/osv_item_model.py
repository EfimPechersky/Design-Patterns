from .abstract_model import abstract_model
from Models.nomenclature_model import nomenclature_model
from Models.range_model import range_model
from Models.nomenclature_model import nomenclature_model
from Core.validator import validator, argument_exception
from Dto.osv_item_dto import osv_item_dto
from datetime import datetime
# Модель строки ОСВ
class osv_item_model(abstract_model):
    __nomenclature:nomenclature_model
    __range:range_model
    __start_num:float
    __end_num:float
    __addition:float
    __substraction:float

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
    Начальный остаток
    """
    @property
    def start_num(self) -> float:
        return self.__start_num
    
    @start_num.setter
    def start_num(self, value: float):
        validator.validate(value,float)
        self.__start_num = value

    """
    Конечный остаток
    """
    @property
    def end_num(self) -> float:
        return self.__end_num
    
    @end_num.setter
    def end_num(self, value: float):
        validator.validate(value,float)
        self.__end_num = value
    
    """
    Приход
    """
    @property
    def addition(self) -> float:
        return self.__addition
    
    @addition.setter
    def addition(self, value: float):
        validator.validate(value,float)
        self.__addition = value
    
    """
    Расход
    """
    @property
    def substraction(self) -> float:
        return self.__substraction
    
    @substraction.setter
    def substraction(self, value: float):
        validator.validate(value,float)
        self.__substraction = value
    

    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(nomenclature:nomenclature_model, range:range_model, start_num:float, end_num:float,addition:float,substraction:float ):
        item = osv_item_model()
        item.range = range
        item.nomenclature = nomenclature
        item.start_num = start_num
        item.end_num = end_num
        item.addition = addition
        item.substraction = substraction
        return item
    """
    Фабричный метод из Dto
    """
    def from_dto(dto:osv_item_dto, cache:dict):
        validator.validate(dto, osv_item_dto)
        validator.validate(cache, dict)
        nomenclature = cache[ dto.nomenclature_id ] if dto.nomenclature_id in cache else None
        range = cache[ dto.range_id ] if dto.range_id in cache else None
        item = osv_item_model.create(nomenclature,range, dto.start_num,dto.end_num,dto.addition, dto.substraction)
        return item

    """
    Фабричный метод в Dto
    """
    def to_dto(self):
        item = osv_item_dto()
        item.nomenclature_id=self.nomenclature.id
        item.range_id = self.range.id
        item.start_num = self.start_num
        item.end_num = self.end_num
        item.addition = self.addition
        item.substraction = self.substraction
        return item
    
    def __repr__(self):
        return "Row "+super().__repr__()

    
