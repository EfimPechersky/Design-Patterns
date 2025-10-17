from Core.start_service import start_service
from Models.range_model import range_model
from Models.group_model import nomenclature_group_model
from Models.nomenclature_model import nomenclature_model
from Models.receipt_model import receipt_model
from Core.repository import repository
from Core.validator import validator,argument_exception,operation_exception
from contextlib import nullcontext as does_not_raise
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
    
    #Тестирование на наличие всех дефолтных единиц измерения
    @pytest.mark.parametrize("ind, range",[
        (0,range_model.create_gramm(__start_service.repository)),
        (1,range_model.create_kilogramm(__start_service.repository)),
        (2,range_model.create_num(__start_service.repository)),
        (3,range_model.create_liter(__start_service.repository)),
        (4,range_model.create_milliliter(__start_service.repository))
    ])
    def test_start_service_range_is_right(self,ind, range):
        # проверка
        assert self.__start_service.repository.data[repository.range_key][ind] is range

    #Тестирование на пустые значения групп номенклатур
    def test_start_service_groups_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.group_key]) != 0

    #Тестирование на наличие всех дефолтных групп номенклатур
    @pytest.mark.parametrize("ind, group",[
        (0,nomenclature_group_model.create_animal_products(__start_service.repository)),
        (3,nomenclature_group_model.create_grain_products(__start_service.repository)),
        (2,nomenclature_group_model.create_milk_products(__start_service.repository)),
        (4,nomenclature_group_model.create_seasoning_products(__start_service.repository)),
        (1, nomenclature_group_model.create_sugar_products(__start_service.repository)),
        (5, nomenclature_group_model.create_addition_products(__start_service.repository))
    ])
    def test_start_service_groups_is_right(self, ind, group):
        # проверка
        assert self.__start_service.repository.data[repository.group_key][ind] is group

    #Тестирование на пустые значения номенклатур
    def test_start_service_nomenclature_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.nomenclature_key]) != 0
    
    #Тестирование на одинаковые адреса у моделей единицы измерения в номенклатуре
    def test_same_range_in_nomenclature_model(self):
        # проверка
        assert self.__start_service.repository.data[repository.nomenclature_key][0].range_count is self.__start_service.repository.data[repository.range_key][0]
    #Тестирование на наличие всех дефолтных номенклатур
    @pytest.mark.parametrize("ind, nomenclature",[
        (0,nomenclature_model.create_butter(__start_service.repository)),
        (1,nomenclature_model.create_eggs(__start_service.repository)),
        (2,nomenclature_model.create_flour(__start_service.repository)),
        (4,nomenclature_model.create_vanilla(__start_service.repository)),
        (3,nomenclature_model.create_sugar(__start_service.repository)),
        (5,nomenclature_model.create_cacao(__start_service.repository)),
        (6,nomenclature_model.create_soda(__start_service.repository)),
        (7,nomenclature_model.create_sour_cream(__start_service.repository))
    ])
    def test_start_service_nomenclature_is_right(self, ind, nomenclature):
        # проверка
        assert self.__start_service.repository.data[repository.nomenclature_key][ind] is nomenclature
    #Тестирование на пустые значения рецептов
    def test_start_service_receipt_not_empty(self):
        # проверка
        assert len(self.__start_service.repository.data[repository.receipt_key]) != 0
    #Тестирование на наличие всех дефолтных рецептов
    @pytest.mark.parametrize("ind, receipt",[
        (0,receipt_model.create_waffles_receipt(__start_service.repository)),
        (1,receipt_model.create_pie_receipt(__start_service.repository))
    ])
    def test_start_service_receipt_is_right(self, ind, receipt):
        # проверка
        assert self.__start_service.repository.data[repository.receipt_key][ind] is receipt
    

    #Тестирование добавления нового ингридиента
    @pytest.mark.parametrize("nomenclature, number,range, result", [
        (nomenclature_model.create_eggs(), 1.0,range_model.create_num(), does_not_raise()),
        ("nomenclature_model.create_eggs()", 1.0,range_model.create_num(), pytest.raises(argument_exception)),
        (nomenclature_model.create_eggs(), "1",range_model.create_num(), pytest.raises(argument_exception)),
        (None, 1.0,range_model.create_num(), pytest.raises(argument_exception)),
        (nomenclature_model.create_eggs(), None,range_model.create_num(), pytest.raises(argument_exception))
    ])
    def test_add_new_ingridient_to_receipt(self,nomenclature, number,range, result):
        #Подготовка
        rm = receipt_model()
        #Проверка на наличие ошибок
        with result:
            #Действие
            start_service.add_new_proportion(rm,nomenclature,number,range)
            #Проверка
            assert rm.ingridients[0][0]==nomenclature
            assert rm.ingridients[0][1]==number
    
    #Тестирование добавление нового шага в рецепт
    @pytest.mark.parametrize("step, number, result", [
        ("Шаг 1", 0, does_not_raise()),
        ("Шаг 1", -1, does_not_raise()),
        ("Шаг 1", "1", pytest.raises(argument_exception)),
        ("Шаг 1", 10, pytest.raises(argument_exception)),
        ("Шаг 1", -10, pytest.raises(argument_exception)),
        (1, 0, pytest.raises(argument_exception)),
        (None, 1, pytest.raises(argument_exception)),
        ("Шаг 1", None, pytest.raises(argument_exception))
    ])
    def test_add_new_step_to_receipt(self,step, number, result):
        #Подготовка
        rm = receipt_model()
        #Проверка на наличие ошибок
        with result:
            #Действие
            start_service.add_step(rm,step,number)
            #Проверка
            assert rm.steps[number]==step