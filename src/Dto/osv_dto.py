from Core.abstract_dto import abstract_dto
from Core.validator import validator,operation_exception
from .ingridient_dto import ingridient_dto
from Models.ingridient_model import ingridient_model
from .osv_item_dto import osv_item_dto
from datetime import datetime
#Dto для модели рецепта
class osv_dto(abstract_dto):
    __storage_id:str
    __start_date:datetime
    __end_date:datetime
    def __init__(self): 
        self.__osv_items = [] 


    """Склад"""
    @property
    def storage_id(self):
        return self.__storage_id
    
    """Сеттер склада"""
    @storage_id.setter
    def storage_id(self,value):
        self.__storage_id=value
    
    """Начальная дата"""
    @property
    def start_date(self):
        return self.__start_date
    
    """Сеттер начальной даты"""
    @start_date.setter
    def start_date(self,value):
        self.__start_date=value
    
    """Конечная дата"""
    @property
    def end_date(self):
        return self.__end_date
    
    """Сеттер конечной даты"""
    @end_date.setter
    def end_date(self,value):
        self.__end_date=value

    # Строки ОСВ
    @property
    def osv_items(self) -> list:
        return self.__osv_items
    
    @osv_items.setter
    def osv_items(self, value):
        for i in value:
            self.__osv_items+=[i]
    
    
    
