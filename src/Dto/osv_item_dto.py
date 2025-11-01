from Core.abstract_dto import abstract_dto
#Dto для ингридиента рецепта
class osv_item_dto(abstract_dto):
    __nomenclature_id:str = ""
    __range_id:str = ""
    __start_num:float = 0
    __end_num:float = 0
    __addition:float = 0
    __substraction:float = 0

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
    
    #начальный остаток
    @property
    def start_num(self) -> str:
        return self.__start_num

    @start_num.setter
    def start_num(self, value):
        self.__start_num = value
    
    #конечный остаток
    @property
    def end_num(self) -> str:
        return self.__end_num

    @end_num.setter
    def end_num(self, value):
        self.__end_num = value
    
    #Приход
    @property
    def addition(self) -> str:
        return self.__addition

    @addition.setter
    def addition(self, value):
        self.__addition = value
        
    #Расход
    @property
    def substraction(self) -> str:
        return self.__substraction

    @substraction.setter
    def substraction(self, value):
        self.__substraction = value
