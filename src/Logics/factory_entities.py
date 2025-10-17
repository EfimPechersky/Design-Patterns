from Core.abstract_response import abstract_response
from Logics.response_csv import response_csv
from Logics.response_md import response_md
from Logics.response_json import response_json
from Logics.response_xml import response_xml
from Core.validator import operation_exception
from Models.settings_manager import settings_manager
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
    def create_default(self, filename) ->abstract_response:
        sm=settings_manager()
        sm.file_name=filename
        sm.load()
        return self.create(sm.settings().response_format)
