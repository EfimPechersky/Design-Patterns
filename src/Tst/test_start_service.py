from Core.start_service import start_service
from Models.range_model import range_model
from Models.group_model import nomenclature_group_model
from Models.nomenclature_model import nomenclature_model
from Models.receipt_model import receipt_model
from Models.ingridient_model import ingridient_model
from Core.repository import repository
from Core.validator import validator,argument_exception,operation_exception
from contextlib import nullcontext as does_not_raise
from Dto.receipt_dto import receipt_dto
from Logics.response_csv import response_csv
from Core.settings_postprocessor import settings_postprocessor
from Core.stock_postprocessor import stock_postprocessor
from Core.observe_service import observe_service
import pytest
from datetime import datetime
#Тестирование работы сервиса
class TestStartService:
    __start_service = start_service()
    __start_service.start(file=True)
    #Тестирование на пустые значения единиц измерения
    def test_start_service_range_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.range_key()]) != 0
    
    #Тестирование на одинаковые адреса у модели единицы измерения
    def test_same_gramm_model(self):
        # проверка
        assert self.__start_service.repository.data[repository.range_key()][2].base_range is self.__start_service.repository.data[repository.range_key()][0]
    
    #Тестирование на наличие всех дефолтных единиц измерения
    @pytest.mark.parametrize("ind, range",[
        (0,range_model.create_gramm(__start_service.repository)),
        (1,range_model.create_num(__start_service.repository)),
        (2,range_model.create_kilogramm(__start_service.repository)),
        (3,range_model.create_liter(__start_service.repository)),
        (4,range_model.create_milliliter(__start_service.repository))
    ])
    def test_start_service_range_is_right(self,ind, range):
        # проверка
        assert self.__start_service.repository.data[repository.range_key()][ind] == range

    #Тестирование на пустые значения групп номенклатур
    def test_start_service_groups_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.group_key()]) != 0

    #Тестирование на наличие всех дефолтных групп номенклатур
    @pytest.mark.parametrize("ind, group",[
        (1,nomenclature_group_model.create_animal_products(__start_service.repository)),
        (2,nomenclature_group_model.create_grain_products(__start_service.repository)),
        (0,nomenclature_group_model.create_milk_products(__start_service.repository)),
        (3,nomenclature_group_model.create_seasoning_products(__start_service.repository)),
        (4, nomenclature_group_model.create_sugar_products(__start_service.repository)),
        (5, nomenclature_group_model.create_addition_products(__start_service.repository))
    ])
    def test_start_service_groups_is_right(self, ind, group):
        # проверка
        assert self.__start_service.repository.data[repository.group_key()][ind] == group

    #Тестирование на пустые значения номенклатур
    def test_start_service_nomenclature_not_empty(self):
        print(self.__start_service.repository.data[repository.nomenclature_key()])
        # проверка
        assert len(self.__start_service.repository.data[repository.nomenclature_key()]) != 0
    
    #Тестирование на одинаковые адреса у моделей единицы измерения в номенклатуре
    def test_same_range_in_nomenclature_model(self):
        # проверка
        assert self.__start_service.repository.data[repository.nomenclature_key()][0].range_count == self.__start_service.repository.data[repository.range_key()][2]
    #Тестирование на наличие всех дефолтных номенклатур
    @pytest.mark.parametrize("ind, nomenclature",[
        (0,nomenclature_model.create_flour(__start_service.repository)),
        (1,nomenclature_model.create_sugar(__start_service.repository)),
        (2,nomenclature_model.create_butter(__start_service.repository)),
        (3,nomenclature_model.create_eggs(__start_service.repository)),
        (4,nomenclature_model.create_vanilla(__start_service.repository)),
        (5,nomenclature_model.create_sour_cream(__start_service.repository)),
        (6,nomenclature_model.create_cacao(__start_service.repository)),
        (7,nomenclature_model.create_soda(__start_service.repository))
    ])
    def test_start_service_nomenclature_is_right(self, ind, nomenclature):
        # проверка
        assert self.__start_service.repository.data[repository.nomenclature_key()][ind] == nomenclature
    #Тестирование на пустые значения рецептов
    def test_start_service_receipt_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.receipt_key()]) != 0
    #Тестирование на наличие всех дефолтных рецептов
    @pytest.mark.parametrize("ind, receipt",[
        (0,receipt_model.create_waffles_receipt(__start_service.repository))
    ])
    def test_start_service_receipt_is_right(self, ind, receipt):
        # проверка
        assert self.__start_service.repository.data[repository.receipt_key()][ind] == receipt

    #Тестирование создания ОСВ
    def test_create_osv(self):
        #Подготовка
        start=datetime.strptime("10-10-2025", "%d-%m-%Y")
        end=datetime.strptime("01-11-2025", "%d-%m-%Y")
        storage_id=self.__start_service.data[repository.storage_key()][0].id
        #Действие
        osv=self.__start_service.create_osv(start, end, storage_id)
        #Проверка
        assert len(osv.osv_items)==len(self.__start_service.data[repository.nomenclature_key()])
    

    #Тестирование создания ОСВ
    def test_block_period(self):
        self.__start_service.start(file=True)
        set=stock_postprocessor()
        print(observe_service.handlers)
        #Подготовка
        self.__start_service.block_period=datetime.strptime("01-11-2025", "%d-%m-%Y")
        #Проверка
        assert len(self.__start_service.data[repository.stock_key()])==len(self.__start_service.data[repository.nomenclature_key()])
        self.__start_service.block_period=datetime.strptime("01-01-2024", "%d-%m-%Y")
        observe_service.delete(set)

    
    #Тестирование даты блокировки
    def test_block_period_same_osv(self):
        self.__start_service.start(file=True)
        set=stock_postprocessor
        #Подготовка
        self.__start_service.block_period=datetime.strptime("01-12-2024", "%d-%m-%Y")
        start=datetime.strptime("10-10-2025", "%d-%m-%Y")
        end=datetime.strptime("01-11-2025", "%d-%m-%Y")
        storage_id=self.__start_service.data[repository.storage_key()][0].id
        #Действие
        osv1=self.__start_service.create_osv(start, end, storage_id)
        csv1=response_csv().build("csv",osv1.osv_items)
        self.__start_service.block_period=datetime.strptime("01-01-2024", "%d-%m-%Y")
        osv2=self.__start_service.create_osv(start, end, storage_id)
        csv2=response_csv().build("csv",osv2.osv_items)
        #Проверка
        assert csv1==csv2
        observe_service.delete(set)

        