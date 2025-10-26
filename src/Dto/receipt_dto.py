from Core.abstract_dto import abstract_dto
from Core.validator import validator,operation_exception
from .ingridient_dto import ingridient_dto
from Models.ingridient_model import ingridient_model
#Dto для модели рецепта
class receipt_dto(abstract_dto):
    def __init__(self):
        self.__steps = []  
        self.__ingridients = [] 


    # Шаги приготовления
    @property
    def steps(self) -> list:
        return self.__steps
    
    @steps.setter
    def steps(self, value):
        for i in value:
            if i.strip()!="":
                self.__steps+=[i.strip()]

    # Состав
    @property
    def ingridients(self) -> list:
        return self.__ingridients
    
    @ingridients.setter
    def ingridients(self, value):
        for i in value:
            self.__ingridients+=[ingridient_dto().create(i)]
    
    
    
