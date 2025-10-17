from .abstract_model import abstract_model
from Core.validator import validator
from Core.repository import repository
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
    @staticmethod
    def create_num(repo=None):
        return range_model.create("штука",1.0, repo=repo)

    """Создание грамма"""
    @staticmethod
    def create_gramm(repo=None):
        return range_model.create("грамм",1.0,repo=repo)
    
    """Создание килограмма"""
    @staticmethod
    def create_kilogramm(repo=None):
        inner_gram = range_model.create_gramm(repo)
        return range_model.create("килограмм",1000.0,base=inner_gram,repo=repo)
    
    """Создание литра"""
    @staticmethod
    def create_liter(repo=None):
        return range_model.create("литр",1.0,repo=repo)
    
    """Создание миллилитра"""
    @staticmethod
    def create_milliliter(repo=None):
        inner_liter = range_model.create_liter(repo)
        return range_model.create("миллилитр",0.001,base=inner_liter,repo=repo)
    
    @staticmethod
    def create(name:str,coeff:float, base=None, repo=None):
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
        if repo!=None:
            validator.validate(repo, repository)
            for i in repo.data[repository.range_key]:
                if i.name==name:
                    return i
        if not base is None:
            validator.validate(base,range_model)
        item = range_model(name,coeff,base)
        return item

    def __repr__(self):
        return "Единица измерения "+super().__repr__()

