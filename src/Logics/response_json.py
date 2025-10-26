from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Convert.convert_factory import convert_factory
from Core.common import common
import json
#Формат ответа csv
class response_json(abstract_response):

        
    # Сформировать Json
    def build(self, format:str, data: list):
        ab=convert_factory()
        dct=ab.rec_convert(data)
        return json.dumps(dct,ensure_ascii=False)