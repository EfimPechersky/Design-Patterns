from .company_model import company_model
from .abstract_model import abstract_model
from Core.validator import validator
from Core.abstract_response import abstract_response
from Core.observe_service import observe_service
from Core.event_type import event_type
from datetime import datetime
"""Класс, описывающий настройки системы"""
class settings_model(abstract_model):
    __company:company_model = None
    __response_format:str = ""
    __block_period:datetime = None
    __logs_output:str
    __log_level:str
    def __init__(self):
        super().__init__()

    #Уровень логирования
    @property
    def log_level(self) -> str:
        return self.__log_level
    #Вывод логов
    @log_level.setter
    def log_level(self,value):
        validator.validate(value,str)
        observe_service.create_event(event_type.set_log_level(),value)
        self.__log_level=value

    #Вывод логов
    @property
    def logs_output(self) -> str:
        return self.__logs_output
    #Вывод логов
    @logs_output.setter
    def logs_output(self,value):
        validator.validate(value,str)
        observe_service.create_event(event_type.set_logs_output(),value)
        self.__logs_output=value
    """Настройки модели организации"""
    @property
    def company(self) -> str:
        return self.__company
    
    """Валидация и присвоение настроек организации"""
    @company.setter
    def company(self, value):
        if validator.validate(value, company_model):
            self.__company = value
    
    """Формат ответа"""
    @property
    def response_format(self) -> str:
        return self.__response_format
    
    """Валидация и присвоение формата ответа"""
    @response_format.setter
    def response_format(self, value):
        validator.validate(value, str)
        self.__response_format = value

    """Дата блокировки"""
    @property
    def block_period(self) -> str:
        return self.__block_period
    
    """Валидация и присвоение даты блокировки"""
    @block_period.setter
    def block_period(self, value):
        validator.validate(value, datetime)
        self.__block_period = value

    def __repr__(self):
        return "Settings"+super().__repr__()