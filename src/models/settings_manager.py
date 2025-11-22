from .company_model import company_model
from .settings_model import settings_model
from Core.validator import validator, operation_exception, argument_exception
from .abstract_model import abstract_model
import json
import os
from datetime import datetime
"""Класс для загрузки настроек"""
class settings_manager:
    __full_file_name:str = ""
    __settings:settings_model = None
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager,cls).__new__(cls)
        return cls.instance
    
    """Конструктор менеджера настроек"""
    def __init__(self):
        self.default()

    """Возвращение загруженных настроек"""
    def settings(self)->settings_model:
        return self.__settings
    
    """Возвращение загруженных настроек организации"""
    def company_setting(self)->company_model:
        return self.__settings.company
        
    """Путь к файлу, нужен для загрузки настроек"""
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    """Валидация и присвоение пути к файлу"""
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)        
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')
        
    """Запись настроек из словаря в company_model"""
    def convert(self,data:dict)->bool:
        validator.validate(data, dict)
        if "company" not in data.keys():
            return False
        validator.validate(data["company"], dict)
        if "response_format" not in data.keys():
            return False
        validator.validate(data["response_format"], str)
        self.__settings.response_format=data["response_format"]
        if "block_period" in data.keys():
            validator.validate(data["response_format"], str)
            self.__settings.block_period=datetime.strptime(data["block_period"],"%d-%m-%Y")
        fields = list(filter(lambda x: not x.startswith("_") , dir(self.__settings.company))) 
        matching_keys = list(filter(lambda key: key in fields, data["company"].keys()))
        try:
            for key in matching_keys:
                setattr(self.__settings.company, key, data["company"][key])
        except:
            return False        

        return True

    """Выгрузка настроек из файла в словарь"""
    def load(self) -> bool:
        fields=["company","response_format"]
        data={}
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")
        try:
            with open( self.__full_file_name, 'r', encoding="UTF-8") as file_instance:
                settings = json.load(file_instance)
                for i in fields:
                    if i in settings.keys():
                        data[i] = settings[i]
                if len(data.keys())>0:
                    return self.convert(data)

            return False
        except:
            return False
    
    """Дефолтные значения настроек"""
    def default(self):
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Company Name"
        self.__settings.company.INN=0
        self.__settings.company.account=0
        self.__settings.company.cor_account=0
        self.__settings.company.BIK=0
        self.__settings.company.type_of_own="AAAAA"
        self.__settings.response_format="csv"
        self.__settings.block_period=datetime.strptime("01-01-1990","%d-%m-%Y")

    
                    
        
        



