from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Core.common import common
from Convert.convert_factory import convert_factory
#Формат ответа csv
class response_md(abstract_response):

    # Сформировать Markdown
    def build(self, format:str, data: list):
        text = super().build(format, data)
        ab=convert_factory()
        dct=ab.rec_convert(data)
        
        fields=[]
        for i in dct[0].keys():
            fields.append(i)
        for field in fields:
            text += f"|{field}"
        text += "|\n"
        for field in fields:
            text += f"|{len(field)*"-"}"
        text += "|\n"
        # Данные
        for i in dct:
            for field in fields:
                text+=f"|{i[field]}"
            text+="|\n"
        return text