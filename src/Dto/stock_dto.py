from Core.abstract_dto import abstract_dto
#Dto для остатка номенклатуры
class stock_dto(abstract_dto):
    __nomenclature_id:str = ""
    __range_id:str = ""
    __num:float = 0
    __storage_id:str=""
    #ID единицы измерения
    @property
    def range_id(self) -> str:
        return self.__range_id

    @range_id.setter
    def range_id(self, value):
        self.__range_id = value

    #ID номенклатуры
    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        self.__nomenclature_id = value
    
    #остаток
    @property
    def num(self) -> str:
        return self.__num

    @num.setter
    def num(self, value):
        self.__num = value
    
    #ID склада
    @property
    def storage_id(self) -> str:
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value):
        self.__storage_id = value
    
