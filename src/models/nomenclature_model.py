from .abstract_model import abstract_model
from .range_model import range_model
from .group_model import nomenclature_group_model
from Core.validator import validator
from Core.repository import repository
"""Класс, описывающий номенклатуру на складе"""
class nomenclature_model(abstract_model):
    __full_name:str = ""
    __range_count:range_model = None
    __nomenclature_group:nomenclature_group_model = None
    __nomenclature_storage:dict = {}
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
    @staticmethod
    def create_flour(repo=None):
        group = nomenclature_group_model.create_grain_products()
        range = range_model.create_gramm(repo)
        full_name="Пшеничная мука"
        return nomenclature_model.create(full_name,group,range,repo=repo)
        
    """Создание номенклатуры сахара"""
    @staticmethod
    def create_sugar(repo=None):
        group = nomenclature_group_model.create_sugar_products()
        range = range_model.create_gramm(repo)
        full_name="Сахар"
        return nomenclature_model.create(full_name,group,range,repo=repo)
    
    """Создание номенклатуры сливочного масла"""
    @staticmethod
    def create_butter(repo=None):
        group = nomenclature_group_model.create_milk_products()
        range = range_model.create_gramm(repo)
        full_name="Сливочное масло"
        return nomenclature_model.create(full_name,group,range,repo=repo)
    
    """Создание номенклатуры ванилина"""
    @staticmethod
    def create_vanilla(repo=None):
        group = nomenclature_group_model.create_seasoning_products()
        range = range_model.create_gramm(repo)
        full_name="Ванилин"
        return nomenclature_model.create(full_name,group,range,repo=repo)
    
    """Создание номенклатуры яиц"""
    @staticmethod
    def create_eggs(repo=None):
        group = nomenclature_group_model.create_animal_products()
        range = range_model.create_num(repo)
        full_name="Яйца"
        return nomenclature_model.create(full_name,group,range,repo=repo)
    
    """Создание номенклатуры сметаны"""
    @staticmethod
    def create_sour_cream(repo=None):
        group = nomenclature_group_model.create_milk_products()
        range = range_model.create_milliliter(repo)
        full_name="Сметана"
        return nomenclature_model.create(full_name,group,range,repo=repo)
    
    """Создание номенклатуры какао"""
    @staticmethod
    def create_cacao(repo=None):
        group = nomenclature_group_model.create_grain_products()
        range = range_model.create_gramm(repo)
        full_name="Какао"
        return nomenclature_model.create(full_name,group,range,repo=repo)
    
    """Создание номенклатуры соды"""
    @staticmethod
    def create_soda(repo=None):
        group = nomenclature_group_model.create_addition_products()
        range = range_model.create_gramm(repo)
        full_name="Сода"
        return nomenclature_model.create(full_name,group,range,repo=repo)

    @staticmethod
    def create(full_name, group, range, repo=None):
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
        if repo!=None:
            validator.validate(repo, repository)
            for i in repo.data[repository.nomenclature_key]:
                if i.full_name==full_name:
                    return i
        nm = nomenclature_model()
        nm.full_name=full_name
        nm.name=full_name
        nm.group=group
        nm.range_count=range
        return nm
    def __repr__(self):
        return "Номенклатура "+super().__repr__()


    
