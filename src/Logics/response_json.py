from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Core.common import common
import json
#Формат ответа csv
class response_json(abstract_response):

    #Функция для конвертирования в словарь
    def turn_into_dict(self, obj):
        if isinstance(obj, list) or isinstance(obj, tuple):
            result=[]
            for i in obj:
                result+=[self.turn_into_dict(i)]
            return result
        elif issubclass(type(obj), abstract_model):
            dct={}
            fields = common.get_fields(obj)
            for field in fields:
                atr=getattr(obj,field)
                dct[field]=self.turn_into_dict(atr)
            return dct
        else:
            return obj
        
    # Сформировать Json
    def build(self, format:str, data: list):
        
        dct={}
        # Данные
        for i in data:
            dct[str(i)]=self.turn_into_dict(i)
            
        return json.dumps(dct,ensure_ascii=False)