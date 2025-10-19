from Core.validator import validator
import abc 
"""
Абстрактный класс, от которого наследуются все модели
"""
class abstract_model(abc.ABC):
    __id = ""
    __name:str = ""
    @abc.abstractmethod
    def __init__(self):
        pass

    def __eq__(self, other):
        """
            Сравнение по id
        Args:
            other (any): Сравниваемый объект
        Raises:
            TypeError
        Returns:
            True, False или Exception
        """
        if isinstance(other, abstract_model):
            return self.id==other.id
        else:
            raise TypeError

    """
    ID
    """
    @property
    def id(self) -> str:
        return self.__id

    """
    Валидация и присвоение ID
    """
    @id.setter
    def id(self, value:str):
        if validator.validate(value,str):
            self.__id = value.strip()
    
    """
    Наименование
    """
    @property
    def name(self) -> str:
        return self.__name

    """
    Валидация и присвоение наименования
    """
    @name.setter
    def name(self, value:str):
        if validator.validate(value, str, 50):
            self.__name = value.strip()
    def __repr__(self):
        return self.name