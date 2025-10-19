from Core.abstract_response import abstract_response
from Logics.response_csv import response_csv
from Logics.response_md import response_md
from Logics.response_json import response_json
from Logics.response_xml import response_xml
from Core.validator import operation_exception
from Models.settings_model import settings_model

#Класс создающий форматы
class factory_entities:
    __match = {
        "csv":  response_csv,
        "md":  response_md,
        "json":response_json,
        "xml":response_xml
    }


    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")
        
        return self.__match[format]
    
    #Получить формат из настроек
    def create_default(self, settings:settings_model) ->abstract_response:
        return self.create(settings.response_format)
