from .prototype import prototype
from Models.nomenclature_model import nomenclature_model
from Models.storage_model import storage_model
from Core.validator import validator
from Dto.filter_dto import filter_dto
from datetime import datetime
"""
Прототип ведомости
"""
class prototype_report(prototype):

    def __init__(self, data):
        super().__init__(data)
    
    """
    Клонирование прототипа
    """
    def clone(self, data:list=None)->prototype:
        return super().clone(data)
    
    """
    Фильтрация объектов
    """
    #@staticmethod
    def filter(report:prototype,filter:filter_dto)->prototype:
        validator.validate(report, prototype)
        result=prototype.filter(report, filter)
        return result
    
    