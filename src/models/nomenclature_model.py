from .abstract_model import abstract_model
from .range_model import range_model
from .group_model import nomenclature_group_model
class nomenclature_model(abstract_model):
    __full_name:str = ""
    __range_count:range_model = None
    __nomenclature_group:nomenclature_group_model = None
    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value:str):
        if self.val.validate(value, str, 255):
            self.__full_name = value.strip()
    
    @property
    def range_count(self) -> str:
        return self.__range_count

    @range_count.setter
    def range_count(self, value:range_model):
        if self.val.validate(value, range_model):
            self.__range_count = value
    
    @property
    def group(self) -> str:
        return self.__nomenclature_group

    @group.setter
    def group(self, value:nomenclature_group_model):
        if self.val.validate(value, nomenclature_group_model):
            self.__nomenclature_group = value

    
