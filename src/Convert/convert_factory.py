from .basic_convertor import basic_convertor
from .datetime_convertor import datetime_convertor
from .reference_convertor import reference_convertor
from .abstract_convertor import abstract_convertor
from Models.abstract_model import abstract_model
from datetime import datetime
#Класс преобразующий любой объект в формат удобный для конвертации в json
class convert_factory:
    #Все конвертеры
    __convertors:list=abstract_convertor.__subclasses__()
    #Рекурсивная функция для ковертации данных
    def rec_convert(self,data):
        if isinstance(data,list) or isinstance(data,tuple):
            converted_data=[]
            for i in data:
                converted_data.append(self.rec_convert(i))
            return converted_data
        elif isinstance(data,dict):
            converted_data={}
            for i in data.keys():
                res=self.rec_convert(data[i])
                if isinstance(res,str):
                    if res=="":
                        continue
                converted_data[i]=res
            return converted_data
        else:
            converted_data=self.convert_data(data)
            if isinstance(converted_data,dict):
                return self.rec_convert(converted_data)
            return converted_data

    #Функция для определения типа данных и последующей конвертации
    def convert_data(self,data):
        for convertor in self.__convertors:
            obj=convertor()
            if obj.is_convertible(data):
                return obj.convert(data)
        
    