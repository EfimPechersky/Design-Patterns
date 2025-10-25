from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Models.receipt_model import receipt_model
from Core.common import common

#Формат ответа csv
class response_csv(abstract_response):

    # Сформировать CSV
    def build(self, format:str, data: list):
        text = super().build(format, data)

        dct=[]
        # Данные
        for i in data:
            dct+=[i.to_dto().to_dict()]
        fields=[]
        for i in dct[0].keys():
            fields.append(i)
        # Шапка
        for field in fields:
            text += f"{field};"
        text += "\n"
        # Данные
        for i in dct:
            for field in fields:
                text+=f"{i[field]};"
            text+="\n"
        return text
