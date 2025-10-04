from .abstract_model import abstract_model
from Core.validator import validator
from functools import lru_cache
"""Класс, описывающий единицу измерения"""
class range_model(abstract_model):
    __base_range = None
    __coeff:float = 0.0

    """Базовая единица измерения, необязательна для создания объекта, нужна для сравнения с другими единицами"""
    @property
    def base_range(self):
        return self.__base_range
    
    """Валидация и присвоение базовой единицы измерения"""
    @base_range.setter
    def base_range(self, value):
        if validator.validate(value, range_model):
            self.__base_range=value
    
    """Коэффициент пересчёта, нужен для перевода в базовую единицу измерения"""
    @property
    def coeff(self):
        return self.__coeff
    
    """Валидация и присвоение коэффициента пересчёта"""
    @coeff.setter
    def coeff(self, value):
        if validator.validate(value, float):
            self.__coeff=value

    """Конструктор единицы измерения"""
    def __init__(self, name_val:str, coeff_val:float, base_range_val = None):
        self.name=name_val
        self.coeff = coeff_val
        if not base_range_val is None:
            self.base_range=base_range_val
    
    """Создание штук"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_num():
        return range_model.create("штука",1.0)

    """Создание грамма"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_gramm():
        return range_model.create("грамм",1.0)
    
    """Создание килограмма"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_kilogramm():
        inner_gram = range_model.create_gramm()
        return range_model.create("килограмм",1000.0,inner_gram)
    
    """Создание литра"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_liter():
        return range_model.create("литр",1.0)
    
    """Создание миллилитра"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_milliliter():
        inner_liter = range_model.create_liter()
        return range_model.create("миллилитр",0.001,inner_liter)

    
    @staticmethod
    def create(name:str,coeff:float, base=None):
        """
        Создание единицы измерения
        Args:
            name (str): Имя единицы измерения
            coeff (float): Коэффициент перерасчёта
            base (any): базовая единица измерения
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            range_model или Exception
        """
        if not base is None:
            validator.validate(base,range_model)
        item = range_model(name,coeff,base)
        return item

