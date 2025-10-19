from Core.abstract_response import abstract_response
from Models.abstract_model import abstract_model
from Models.receipt_model import receipt_model
from Core.common import common

#Формат ответа csv
class response_csv(abstract_response):

    # Сформировать CSV
    def build(self, format:str, data: list):
        text = super().build(format, data)

        # Шапка
        item = data [ 0 ]
        fields = common.get_fields( item )
        for field in fields:
            text += f"{field};"
        text += "\n"
        # Данные
        for i in data:
            for field in fields:
                atr=str(getattr(i,field))
                text+=f"{atr};"
            text+="\n"
        return text
