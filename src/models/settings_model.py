from .company_model import company_model
from .abstract_model import abstract_model
from Core.validator import validator
"""Класс, описывающий настройки системы"""
class settings_model(abstract_model):
    __company:company_model = None

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