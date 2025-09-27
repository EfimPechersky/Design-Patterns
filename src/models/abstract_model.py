from core.validator import validator
class abstract_model:
    __id = ""
    __name:str = ""
    val:validator = validator()
    def __eq__(self, other):
        if isinstance(other, abstract_model):
            return self.id==other.id
        else:
            raise TypeError

    #ID
    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value:str):
        if value.strip()!="":
            self.__id = value.strip()
    
    #name
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        if self.val.validate(value, str, 50):
            self.__name = value.strip()