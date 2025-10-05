from .abstract_model import abstract_model
from Core.validator import validator
"""Класс, описывающий единицу измерения"""
class range_model(abstract_model):
    __base_range = None
    __coeff:float = 0.0
    __range_storage:dict = {}

    def get_from_storage(key:str):
        """
        Получение значения из хранилища
        Args:
            key (str): Ключ значения
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            range_model, None или Exception
        """
        validator.validate(key,str)
        if key in range_model.__range_storage:
            return range_model.__range_storage[key]
        return None
    
    def put_in_storage(key:str, value):
        """
        Запись значения в хранилище
        Args:
            key (str): Ключ значения
            value (range_model): Значение
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            None или Exception
        """
        validator.validate(key,str)
        validator.validate(value,range_model)
        range_model.__range_storage[key]=value
        
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
    @staticmethod
    def create_num():
        return range_model.create("штука",1.0)

    """Создание грамма"""
    @staticmethod
    def create_gramm():
        return range_model.create("грамм",1.0)
    
    """Создание килограмма"""
    @staticmethod
    def create_kilogramm():
        inner_gram = range_model.create_gramm()
        return range_model.create("килограмм",1000.0,inner_gram)
    
    """Создание литра"""
    @staticmethod
    def create_liter():
        return range_model.create("литр",1.0)
    
    """Создание миллилитра"""
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
        item = range_model.get_from_storage(name)
        if item is None:
            if not base is None:
                validator.validate(base,range_model)
            item = range_model(name,coeff,base)
            range_model.put_in_storage(name, item)
        return item

