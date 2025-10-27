from .abstract_convertor import abstract_convertor
from Core.validator import validator, operation_exception
from Core.common import common
from datetime import datetime
#Класс для преобразования объектов типа datetime
class datetime_convertor(abstract_convertor):
    #Список конвертируемых типов
    convertible_data:list=[datetime]
    def convert(self, data):
        dict={}
        checked_data = super().convert(data)
        fields = list(filter(lambda x: not x.startswith("_") , dir(checked_data)))
        try:
            for field in fields:
                atr=getattr(checked_data, field)
                if not isinstance(atr,int):
                    continue
                dict[field]=atr
        except:
            raise operation_exception("Невозможно преобразовать данные!")    

        return dict