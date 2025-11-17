from Core.validator import validator
from Dto.filter_dto import filter_dto
from abc import ABC,abstractmethod
from Core.common import common
from Core.validator import argument_exception
"""
Шаблон прототипа
"""
class prototype(ABC):
    
    __data:list=[]
    
    def __init__(self,data:list):
        self.data=data
    
    @property
    def data(self)->list:
        return self.__data
    
    @data.setter
    def data(self,value:list):
        validator.validate(value,list)
        self.__data=value
    
    """
    Клонирование прототипа
    """
    def clone(self,data:list=None)->"prototype":
        inner_data=None
        if data is None:
            inner_data=self.data
        else:
            inner_data=data
        instance=prototype(inner_data)
        return instance
    
    """
    Получение значения поля (включая вложенные поля)
    """
    def get_value_from_field(object, field):
        complicated_fields=field.split(".")
        value=object
        for i in complicated_fields:
            fields_list=common.get_fields(value)
            if i in fields_list:
                value=getattr(value,i)
            else:
                raise argument_exception(f"Неверное поле {i} в объекте {value}!")
        return value
    
    """
    Фильтрация значений
    """
    #@staticmethod
    def filter(prot:"prototype", filter:filter_dto)->list:
        data=prot.data
        if len(data)==0:
            return prot.clone(data)
        result=[]
        for item in data:
            value=prototype.get_value_from_field(item, filter.field_name)
            if filter.get_condition_function(filter.condition)(filter.value,value):
                result.append(item)
        return prot.clone(result)
