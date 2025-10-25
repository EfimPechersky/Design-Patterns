from Core.abstract_dto import abstract_dto

class ingridient_dto(abstract_dto):
    __nomenclature_id:str = ""
    __range_id:str = ""
    __value:float = 0


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
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
