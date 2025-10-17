from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Core.common import common

#Формат ответа csv
class response_json(abstract_response):

    # Сформировать Json
    def build(self, format:str, data: list):
        text = super().build(format, data)
        
        item = data [0]
        fields = common.get_fields( item )
        # Данные
        text+="{\n"
        for i in data:
            text+=f"\t\"{i.name}\":"+"{\n"
            for field in fields:
                if field=="name":
                    continue
                atr=str(getattr(i,field))
                text+=f"\t\t\"{field}\":"
                if isinstance(atr,str):
                    text+=f"\"{atr}\""
                else:
                    text+=f"{atr}"
                text+=",\n"

            text=text[:-2]+"\n\t},\n"
        text=text[:-2]+"\n}"
        return text