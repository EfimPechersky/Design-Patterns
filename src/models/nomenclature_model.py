from .abstract_model import abstract_model
from .range_model import range_model
from .group_model import nomenclature_group_model
from Core.validator import validator
#Класс, описывающий номенклатуру на складе
class nomenclature_model(abstract_model):
    __full_name:str = ""
    __range_count:range_model = None
    __nomenclature_group:nomenclature_group_model = None

    #Полное название номенклатуры
    @property
    def full_name(self) -> str:
        return self.__full_name

    #Валидация и присвоение полного названия номенклатуры
    @full_name.setter
    def full_name(self, value:str):
        if validator.validate(value, str, 255):
            self.__full_name = value.strip()
    
    #Единица измерения номенклатуры
    @property
    def range_count(self) -> str:
        return self.__range_count

    #Валидация и присвоение единицы измерения
    @range_count.setter
    def range_count(self, value:range_model):
        if validator.validate(value, range_model):
            self.__range_count = value
    
    #Группа номенклатуры
    @property
    def group(self) -> str:
        return self.__nomenclature_group

    #Валидация и присвоение группы номенклатуры
    @group.setter
    def group(self, value:nomenclature_group_model):
        if validator.validate(value, nomenclature_group_model):
            self.__nomenclature_group = value

    
