from .abstract_model import abstract_model
from Core.validator import validator
"""Класс, описывающий группу номенклатуры"""
class nomenclature_group_model(abstract_model):

    __group_storage:dict={}

    def __init__(self):
        super().__init__()

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
        nmg = nomenclature_group_model()
        nmg.name=name
        return nmg