from Core.abstract_dto import abstract_dto
from datetime import datetime
#Dto для транзакции
class transaction_dto(abstract_dto):
    __nomenclature_id:str = ""
    __storage_id:str = ""
    __date:datetime = None
    __range_id:str = ""
    __num:float = 0


    @property
    def range_id(self) -> str:
        return self.__range_id

    @range_id.setter
    def range_id(self, value):
        self.__range_id = value

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        self.__nomenclature_id = value
    
    @property
    def num(self) -> str:
        return self.__num

    @num.setter
    def num(self, value):
        self.__num = value

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value
    
    @property
    def storage_id(self) -> str:
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value):
        self.__storage_id = value

        