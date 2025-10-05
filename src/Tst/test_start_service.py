from Core.start_service import start_service
from Models.range_model import range_model
from Models.group_model import nomenclature_group_model
from Models.nomenclature_model import nomenclature_model
from Models.receipt_model import receipt_model
from Core.repository import repository
import pytest
#Тестирование работы сервиса
class TestStartService:
    __start_service = start_service()
    __start_service.start()
        
    #Тестирование на пустые значения единиц измерения
    def test_start_service_range_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.range_key]) != 0
    
    #Тестирование на одинаковые адреса у модели единицы измерения
    def test_same_gramm_model(self):
        # проверка
        assert self.__start_service.repository.data[repository.range_key][1].base_range is self.__start_service.repository.data[repository.range_key][0]
    
    #Тестирование на пустые значения групп номенклатур
    def test_start_service_groups_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.group_key]) != 0

    #Тестирование на пустые значения номенклатур
    def test_start_service_nomenclature_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.nomenclature_key]) != 0
    
    #Тестирование на одинаковые адреса у моделей единицы измерения в номенклатуре
    def test_same_range_in_nomenclature_model(self):
        # проверка
        assert self.__start_service.repository.data[repository.nomenclature_key][0].range_count is self.__start_service.repository.data[repository.range_key][0]
    
    #Тестирование на пустые значения рецептов
    def test_start_service_receipt_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.receipt_key]) != 0
    
