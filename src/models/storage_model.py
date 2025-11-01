from .abstract_model import abstract_model
from Core.validator import validator
from Dto.storage_dto import storage_dto
"""Класс, описывающий модель склада"""
class storage_model(abstract_model):
    def __init__(self):
        super().__init__()

    """Фабричный метод из Dto"""
    def from_dto(dto:storage_dto, cache:dict):
        item = storage_model()
        item.name=dto.name
        item.id=dto.id
        return item
    
    """Фабричный метод в Dto"""
    def to_dto(self):
        item = storage_dto()
        item.name=self.name
        item.id=self.id
        return item
    
    def __repr__(self):
        return "Storage "+super().__repr__()