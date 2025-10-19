from .abstract_model import abstract_model
from Core.validator import validator
from Core.repository import repository
"""Класс, описывающий группу номенклатуры"""
class nomenclature_group_model(abstract_model):

    __group_storage:dict={}

    def __init__(self):
        super().__init__()

    """"Создание группы молочных продуктов"""
    @staticmethod
    def create_milk_products(repo=None):
        return nomenclature_group_model.create("Молочные продукты",repo=repo)
    
    """"Создание группы продуктов животного происхлождения"""
    @staticmethod
    def create_animal_products(repo=None):
        return nomenclature_group_model.create("Продукты животного происхождения",repo=repo)
    
    """"Создание группы продуктов помола зерна злаков"""
    @staticmethod
    def create_grain_products(repo=None):
        return nomenclature_group_model.create("Продукты помола зерна злаков",repo=repo)
    
    """"Создание группы приправ и пряностей"""
    @staticmethod
    def create_seasoning_products(repo=None):
        return nomenclature_group_model.create("Приправы и пряности",repo=repo)
    
    """"Создание группы сахара и кондитерских изделий из сахара"""
    @staticmethod
    def create_sugar_products(repo=None):
        return nomenclature_group_model.create("Сахар и кондитерские изделия из сахара",repo=repo)

    """"Создание группы пищевых добавок"""
    @staticmethod
    def create_addition_products(repo=None):
        return nomenclature_group_model.create("Пищевая добавка",repo=repo)
    @staticmethod
    def create(name:str,repo=None):
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
        if repo!=None:
            validator.validate(repo, repository)
            for i in repo.data[repo.group_key]:
                if i.name==name:
                    return i
        nmg = nomenclature_group_model()
        nmg.name=name
        return nmg
    def __repr__(self):
        return "Group "+super().__repr__()