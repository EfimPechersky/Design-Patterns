from .abstract_model import abstract_model
from core.validator import validator
class range_model(abstract_model):
    __base_range = None
    __coeff:float = 0.0

    #Базовая единица измерения, необязательная для создания объекта
    @property
    def base_range(self):
        return self.__base_range
    
    #Валидация и присвоение базовой единицы измерения
    @base_range.setter
    def base_range(self, value):
        if validator.validate(value, range_model):
            self.__base_range=value
    
    #Коэффициент пересчёта
    @property
    def coeff(self):
        return self.__coeff
    
    #Валидация и присвоение коэффициента пересчёта
    @coeff.setter
    def coeff(self, value):
        if validator.validate(value, float):
            self.__coeff=value

    #Конструктор единицы измерения
    def __init__(self, name_val:str, coeff_val:float, base_range_val = None):
        self.name=name_val
        self.coeff = coeff_val
        if not base_range_val is None:
            self.base_range=base_range_val

