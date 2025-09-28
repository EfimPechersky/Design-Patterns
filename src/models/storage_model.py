from .abstract_model import abstract_model
from core.validator import validator
class storage_model(abstract_model):
    __name: str = ""

    #Наименование склада
    @property
    def name(self) -> str:
        return self.__name

    #Валидация и присвоение наименования склада
    @name.setter
    def name(self, value:str):
        if validator.validate(value, str, 50):
            self.__name = value.strip()
    
