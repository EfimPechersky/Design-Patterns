from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Core.common import common

#Формат ответа csv
class response_xml(abstract_response):

    # Сформировать XML
    def build(self, format:str, data: list):
        text = super().build(format, data)
        
        item = data [0]
        fields = common.get_fields( item )
        # Данные
        text+=f"<List>\n"
        for i in data:
            text+=f"<{i.__repr__().replace(" ", "_")}>\n"
            for field in fields:
                atr=str(getattr(i,field))
                text+=f"\t<{field}>{atr}</{field}>\n"
            text+=f"</{i.__repr__().replace(" ", "_")}>\n"
        text+=f"</List>\n"
        return text