from .company_model import company_model
from .settings_model import settings_model
from core.validator import validator, operation_exception, argument_exception
from .abstract_model import abstract_model
import json
import os
class settings_manager:
    __full_file_name:str = ""
    __settings:settings_model = None
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager,cls).__new__(cls)
        return cls.instance
    
    #Конструктор менеджера настроек
    def __init__(self):
        self.default()

    #Возвращение загруженных настроек
    def settings(self)->settings_model:
        return self.__settings
    
    #Возвращение загруженных настроек организации
    def company_setting(self)->company_model:
        return self.__settings.company
        
    #Путь к файлу
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    #Валидация и присвоение пути к файлу
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)        
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')
        
    #Запись настроек из словаря в company_model
    def convert(self,data:dict)->bool:
        validator.validate(data, dict)

        fields = list(filter(lambda x: not x.startswith("_") , dir(self.__settings.company))) 
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self.__settings.company, key, data[key])
        except:
            return False        

        return True
    
    #Выгрузка настроек из файла в словарь
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open( self.__full_file_name, 'r') as file_instance:
                settings = json.load(file_instance)

                if "company" in settings.keys():
                    data = settings["company"]
                    return self.convert(data)

            return False
        except:
            return False
    
    #Дефолтные значения настроек
    def default(self):
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Company Name"
        self.__settings.company.INN=0
        self.__settings.company.account=0
        self.__settings.company.cor_account=0
        self.__settings.company.BIK=0
        self.__settings.company.type_of_own="AAAAA"

    
                    
        
        



