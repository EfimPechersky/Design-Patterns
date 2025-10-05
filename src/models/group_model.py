from .abstract_model import abstract_model
from Core.validator import validator
"""Класс, описывающий группу номенклатуры"""
class nomenclature_group_model(abstract_model):

    __group_storage:dict={}

    def __init__(self):
        super().__init__()

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
            nomenclature_group_model, None или Exception
        """
        validator.validate(key,str)
        if key in nomenclature_group_model.__group_storage:
            return nomenclature_group_model.__group_storage[key]
        return None
    
    def put_in_storage(key:str, value):
        """
        Запись значения в хранилище
        Args:
            key (str): Ключ значения
            value (nomenclature_group_model): Значение
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            None или Exception
        """
        validator.validate(key,str)
        validator.validate(value,nomenclature_group_model)
        nomenclature_group_model.__group_storage[key]=value

    """"Создание группы молочных продуктов"""
    @staticmethod
    def create_milk_products():
        return nomenclature_group_model.create("Молочные продукты")
    
    """"Создание группы продуктов животного происхлождения"""
    @staticmethod
    def create_animal_products():
        return nomenclature_group_model.create("Продукты животного происхождения")
    
    """"Создание группы продуктов помола зерна злаков"""
    @staticmethod
    def create_grain_products():
        return nomenclature_group_model.create("Продукты помола зерна злаков")
    
    """"Создание группы приправ и пряностей"""
    @staticmethod
    def create_seasoning_products():
        return nomenclature_group_model.create("Приправы и пряности")
    
    """"Создание группы сахара и кондитерских изделий из сахара"""
    @staticmethod
    def create_sugar_products():
        return nomenclature_group_model.create("Сахар и кондитерские изделия из сахара")

    """"Создание группы пищевых добавок"""
    @staticmethod
    def create_addition_products():
        return nomenclature_group_model.create("Пищевая добавка")
    @staticmethod
    def create(name:str):
        """"
        Создание группы
        Args:
            name (str): Название группы
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            nomenclature_group_model или Exception
        """
        nmg = nomenclature_group_model.get_from_storage(name)
        if nmg is None:
            nmg = nomenclature_group_model()
            nmg.name=name
            nomenclature_group_model.put_in_storage(name, nmg)
        return nmg