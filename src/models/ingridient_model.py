from .abstract_model import abstract_model
from Models.nomenclature_model import nomenclature_model
from Models.range_model import range_model
from Core.validator import validator, argument_exception
from Dto.ingridient_dto import ingridient_dto
# Модель элемента рецепта
class ingridient_model(abstract_model):
    __nomenclature:nomenclature_model
    __range:range_model
    __value:float

    def __init__(self):
        super().__init__()

    # Фабричный метод
    def create(nomenclature:nomenclature_model, range:range_model,  value:float):
        item = ingridient_model()
        item.__nomenclature = nomenclature
        item.__range = range
        item.__value = value
        return item

    """
    Единицы измерения количества номенклатуры
    """
    @property
    def range(self):
        return self.__range
    
    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    """
    Вид номенклатуры
    """
    @property
    def nomenclature(self):
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    """
    Количество номенклатуры
    """
    @property
    def value(self) -> float:
        return self.__value
    
    @value.setter
    def value(self, value: float):
        validator.validate(value,float)
        if value <= 0:
             raise argument_exception("Некорректный аргумент!")
        self.__value = value

    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(nomenclature:nomenclature_model, range:range_model, value:float ):
        item = ingridient_model()
        item.range = range
        item.nomenclature = nomenclature
        item.value = value
        return item
    
    """
    Фабричный метод из Dto
    """
    def from_dto(dto:ingridient_dto, cache:dict):
        validator.validate(dto, ingridient_dto)
        validator.validate(cache, dict)
        nomenclature = cache[ dto.nomenclature_id ] if dto.nomenclature_id in cache else None
        range = cache[ dto.range_id ] if dto.range_id in cache else None
        item = ingridient_model.create(nomenclature,range, dto.value)
        return item

    """
    Фабричный метод в Dto
    """
    def to_dto(self):
        item = ingridient_dto()
        item.nomenclature_id=self.nomenclature.id
        item.range_id = self.range.id
        item.value=self.value
        return item
    
    def __repr__(self):
        return "Ingridient "+super().__repr__()