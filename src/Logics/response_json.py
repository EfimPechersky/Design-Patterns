from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Core.common import common
import json
#Формат ответа csv
class response_json(abstract_response):

        
    # Сформировать Json
    def build(self, format:str, data: list):
        
        dct=[]
        # Данные
        for i in data:
            dct+=[i.to_dto().to_dict()]
            
        return json.dumps(dct,ensure_ascii=False)