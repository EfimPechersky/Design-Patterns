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
                name=None
                if not issubclass(type(i), abstract_model):
                    name=type(i).__name__
                text+=self.turn_into_xml(i,name)
            return text
            
        elif issubclass(type(obj), abstract_model):
            fields = common.get_fields(obj)
            text+=f"<{str(obj).split(" ")[0].lower()}>\n"
            for field in fields:
                atr=getattr(obj,field)
                text+=f"\t<{field}>{self.turn_into_xml(atr)}</{field}>\n"
            text+=f"</{str(obj).split(" ")[0].lower()}>\n"
            return text
        else:
            if name!=None:
                return f"<{name}>"+str(obj)+f"</{name}>"
            return str(obj)
    
    # Сформировать XML
    def build(self, format:str, data: list):
        text = super().build(format, data)
        
        item = data [0]
        fields = common.get_fields( item )
        text+="<List>"
        text+=self.turn_into_xml(data)
        text+="</List>"
        return text
        