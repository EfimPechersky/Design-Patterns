from .abstract_model import abstract_model
from .range_model import range_model
from .group_model import nomenclature_group_model
from functools import lru_cache
from Core.validator import validator
"""Класс, описывающий номенклатуру на складе"""
class nomenclature_model(abstract_model):
    __full_name:str = ""
    __range_count:range_model = None
    __nomenclature_group:nomenclature_group_model = None

    def __init__(self):
        super().__init__()
    """Полное название номенклатуры"""
    @property
    def full_name(self) -> str:
        return self.__full_name

    """Валидация и присвоение полного названия номенклатуры"""
    @full_name.setter
    def full_name(self, value:str):
        if validator.validate(value, str, 255):
            self.__full_name = value.strip()
    
    """Единица измерения номенклатуры"""
    @property
    def range_count(self) -> str:
        return self.__range_count

    """Валидация и присвоение единицы измерения"""
    @range_count.setter
    def range_count(self, value:range_model):
        if validator.validate(value, range_model):
            self.__range_count = value
    
    """Группа номенклатуры"""
    @property
    def group(self) -> str:
        return self.__nomenclature_group

    """Валидация и присвоение группы номенклатуры"""
    @group.setter
    def group(self, value:nomenclature_group_model):
        if validator.validate(value, nomenclature_group_model):
            self.__nomenclature_group = value
    
    """Создание номенклатуры пшеничной муки"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_flour():
        group = nomenclature_group_model.create_grain_products()
        range = range_model.create_gramm()
        full_name="Пшеничная мука"
        return nomenclature_model.create(full_name,group,range)
    """Создание номенклатуры сахара"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_sugar():
        group = nomenclature_group_model.create_sugar_products()
        range = range_model.create_gramm()
        full_name="Сахар"
        return nomenclature_model.create(full_name,group,range)
    
    """Создание номенклатуры сливочного масла"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_butter():
        group = nomenclature_group_model.create_milk_products()
        range = range_model.create_gramm()
        full_name="Сливочное масло"
        return nomenclature_model.create(full_name,group,range)
    
    """Создание номенклатуры ванилина"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_vanilla():
        group = nomenclature_group_model.create_seasoning_products()
        range = range_model.create_gramm()
        full_name="Ванилин"
        return nomenclature_model.create(full_name,group,range)
    
    """Создание номенклатуры яиц"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_eggs():
        group = nomenclature_group_model.create_animal_products()
        range = range_model.create_num()
        full_name="Яйца"
        return nomenclature_model.create(full_name,group,range)
    
    """Создание номенклатуры сметаны"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_sour_cream():
        group = nomenclature_group_model.create_milk_products()
        range = range_model.create_milliliter()
        full_name="Сметана"
        return nomenclature_model.create(full_name,group,range)
    
    """Создание номенклатуры какао"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_cacao():
        group = nomenclature_group_model.create_grain_products()
        range = range_model.create_gramm()
        full_name="Какао"
        return nomenclature_model.create(full_name,group,range)
    
    """Создание номенклатуры соды"""
    @lru_cache(maxsize=None)
    @staticmethod
    def create_soda():
        group = nomenclature_group_model.create_addition_products()
        range = range_model.create_gramm()
        full_name="Сода"
        return nomenclature_model.create(full_name,group,range)

    @staticmethod
    def create(full_name, group, range):
        """"
        Создание номенклатуры
        Args:
            full_name (str): Название номенклатуры
            group (nomenclature_group_model): Группа номенклатуры
            range (range_model): Единица измерения
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            nomenclature_model или Exception
        """
        nm = nomenclature_model()
        nm.full_name=full_name
        nm.group=group
        nm.range_count=range
        return nm


    
