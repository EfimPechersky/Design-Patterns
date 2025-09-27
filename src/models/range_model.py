from .abstract_model import abstract_model
class range_model(abstract_model):
    __base_range = None
    __coeff:float = 0.0
    @property
    def base_range(self):
        return self.__base_range
    
    @base_range.setter
    def base_range(self, value):
        if self.val.validate(value, range_model):
            self.__base_range=value
    
    @property
    def coeff(self):
        return self.__coeff
    
    @coeff.setter
    def coeff(self, value):
        if self.val.validate(value, float):
            self.__coeff=value

    def __init__(self, name_val:str, coeff_val:float, base_range_val = None):
        self.name=name_val
        self.coeff = coeff_val
        if not base_range_val is None:
            self.base_range=base_range_val

