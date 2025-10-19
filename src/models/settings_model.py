from .company_model import company_model
from .abstract_model import abstract_model
from Core.validator import validator
from Core.abstract_response import abstract_response
"""Класс, описывающий настройки системы"""
class settings_model(abstract_model):
    __company:company_model = None
    __response_format:str = ""

    def __init__(self):
        super().__init__()
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
    
    def __repr__(self):
        return "Settings"+super().__repr__()