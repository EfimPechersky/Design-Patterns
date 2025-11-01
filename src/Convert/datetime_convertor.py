from .abstract_convertor import abstract_convertor
from Core.validator import validator, operation_exception
from Core.common import common
from datetime import datetime
#Класс для преобразования объектов типа datetime
class datetime_convertor(abstract_convertor):
    #Список конвертируемых типов
    convertible_data:list=[datetime]
    def convert(self, data):
        checked_data = super().convert(data)
        
        return f"{checked_data.day}-{checked_data.month}-{checked_data.year}"