from Core.validator import validator
#Абстрактный класс, от которого наследуются все модели
class abstract_model:
    __id = ""
    __name:str = ""
    def __eq__(self, other):
        if isinstance(other, abstract_model):
            return self.id==other.id
        else:
            raise TypeError

    #ID
    @property
    def id(self) -> str:
        return self.__id

    #Валидация и присвоение ID
    @id.setter
    def id(self, value:str):
        if validator.validate(value,str):
            self.__id = value.strip()
    
    #Наименование
    @property
    def name(self) -> str:
        return self.__name

    #Валидация и присвоение наименования
    @name.setter
    def name(self, value:str):
        if validator.validate(value, str, 50):
            self.__name = value.strip()