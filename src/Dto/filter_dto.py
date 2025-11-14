from Core.abstract_dto import abstract_dto
from Core.validator import argument_exception
class filter_dto(abstract_dto):
    __field_name:str=""
    __value:str=""
    __condition:str = ""
    __condition_variants={"EQUALS":lambda x,y:x==y,
                          "LIKE":lambda x,y:x in y,
                          "LESS":lambda x,y:x <= y,
                          "MORE":lambda x,y:x >= y,
                          "NOT EQUALS":lambda x,y:x != y
                          }

    @property
    def field_name(self):
        return self.__field_name
    @field_name.setter
    def field_name(self,value):
        self.__field_name=value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self,value):
        self.__value=value
    
    @property
    def condition(self):
        return self.__condition
    
    @staticmethod
    def get_condition_function(condition):
        return filter_dto.__condition_variants[condition]
    @condition.setter
    def condition(self,value):
        if value in self.__condition_variants:
            self.__condition=value
        else:
            raise argument_exception("Неверное значение условия фильтра!")