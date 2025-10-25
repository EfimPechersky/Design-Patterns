from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Core.common import common

#Формат ответа csv
class response_xml(abstract_response):


    
    #Функция для конвертирования в xml
    def turn_into_xml(self, obj, name=None):
        text=""
        if isinstance(obj, list) or isinstance(obj, tuple):
            for i in obj:
                text+=f"<{name}>"
                text+=self.turn_into_xml(i)
                text+=f"</{name}>"
            return text
            
        elif isinstance(obj, dict):
            for field in obj.keys():
                text+=f"\t<{field}>{self.turn_into_xml(obj[field], field[:-1])}</{field}>\n"
            return text
        else:
            return str(obj)
    
    # Сформировать XML
    def build(self, format:str, data: list):
        text = super().build(format, data)
        dct=[]
        # Данные
        for i in data:
            dct+=[i.to_dto().to_dict()]
        text+="<List>"
        text+=self.turn_into_xml(dct,str(data[0]).split()[0].lower())
        text+="</List>"
        return text
        