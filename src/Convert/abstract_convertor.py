import abc
from Core.common import common
from Core.validator import validator,argument_exception, operation_exception
#Абстрактный класс ковертеров
class abstract_convertor:

    #Типы данных для конвертации
    convertible_data:list
    #Метод для проверки типа передаваемого типа
    @abc.abstractmethod
    def is_convertible(self,data) -> bool:
        for type in self.convertible_data:
            if isinstance(data,type):
                return True
        return False
    # Универсальный фабричный метод для загрузки словаря
    @abc.abstractmethod
    def convert(self,data) -> dict:
        if self.is_convertible(data):
            return data
        raise argument_exception("Неправильный тип данных для преобразования!")