from Core.abstract_dto import abstract_dto

# Модель единицы измерения (dto)
# Пример
#                "name":"Грамм",
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "base_id":null,
#                "value":1
class range_dto(abstract_dto):
    __base_id:str = None
    __coeff:float = 1.0

    @property
    def base_id(self) -> str:
        return self.__base_id    
    
    @base_id.setter
    def base_id(self, value):
        self.__base_id = value

    @property
    def coeff(self) -> int:
        return self.__coeff    
    
    @coeff.setter
    def coeff(self, value):
        self.__coeff = value