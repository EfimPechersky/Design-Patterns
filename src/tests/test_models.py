from models.company_model import company_model
from models.settings_manager import settings_manager
from models.storage_model import storage_model
from models.range_model import range_model
from models.group_model import nomenclature_group_model
from models.nomenclature_model import nomenclature_model
from models.settings_model import settings_model
from core.validator import validator,argument_exception,operation_exception
from contextlib import nullcontext as does_not_raise
import json
import uuid
import pytest
class TestModels:
    #Тестирование создания пустой модели организации
    def test_check_create_company_model(self):
        #Действие
        model = company_model()
        #Проверка
        assert model.name == ""

    #Тестирование заполнения полей модели организации
    @pytest.mark.parametrize("attr_name, attr_value, result", [
        ("name", "Romashka", does_not_raise()),
        ("name", "A"*51, pytest.raises(argument_exception)),
        ("name", 0, pytest.raises(argument_exception)),
        ("name", None, pytest.raises(argument_exception)),
        ("INN", 10**11, does_not_raise()),
        ("INN", 10**12, pytest.raises(argument_exception)),
        ("INN", "A", pytest.raises(argument_exception)),
        ("INN", None, pytest.raises(argument_exception)),
        ("account",10**10, does_not_raise()),
        ("account", 10**11, pytest.raises(argument_exception)),
        ("account", "A", pytest.raises(argument_exception)),
        ("account", None, pytest.raises(argument_exception)),
        ("cor_account",10**10, does_not_raise()),
        ("cor_account", 10**11, pytest.raises(argument_exception)),
        ("cor_account", "A", pytest.raises(argument_exception)),
        ("cor_account", None, pytest.raises(argument_exception)),
        ("BIK",10**8, does_not_raise()),
        ("BIK", 10**9, pytest.raises(argument_exception)),
        ("BIK", "A", pytest.raises(argument_exception)),
        ("BIK", None, pytest.raises(argument_exception)),
        ("type_of_own","O"*3, does_not_raise()),
        ("type_of_own", "O"*6, pytest.raises(argument_exception)),
        ("type_of_own", 0, pytest.raises(argument_exception)),
        ("type_of_own", None, pytest.raises(argument_exception))
        ])
    def test_input_fields_company_model(self,attr_name, attr_value, result ):
        #Подготовка
        model = company_model()
        #Проверка на наличие ошибки
        with result:
            #Действие
            setattr(model, attr_name, attr_value)
            #Проверка при отсутствии ошибок
            assert getattr(model,attr_name,None) == attr_value

    #Тестирование загрузки модели организации из файла
    def test_load_company_model(self):
        #Подготовка
        filename = './settings.json'
        sm = settings_manager()
        sm.file_name=filename
        #Действие
        result=sm.load()
        #Проверка
        assert result==True
    
    #Тестирование копирования настроек из загруженной модели организации
    def test_copy_company_model_from_settings_manager(self):
        #Подготовка
        filename = './settings.json'
        sm = settings_manager()
        sm.file_name=filename
        #Действие
        sm.load()
        #Проверка
        company = company_model(sm.settings().company)
        assert company.name == "Romashka"

    #Тестирование сравнение моделей организации загруженных из одного файла
    def test_compare_loaded_company_model(self):
        #Подгтовка
        filename = "./settings.json"
        sm1 = settings_manager()
        sm1.file_name=filename
        sm2 = settings_manager()
        sm2.file_name=filename

        #Действие
        sm1.load()
        sm2.load()
        model1 = sm1.company_setting()
        model2 = sm2.company_setting()

        #Проверка
        assert model1.name==model2.name

    #Тестирование загрузки настроек из файлов в разных директориях
    def test_load_different_settings(self):
        #Подготовка
        filename1 = "../src/settings.json"
        filename2 = "./settings_folder/other_settings.json"
        #Действие
        sm1 = settings_manager()
        sm1.file_name=filename1
        sm1.load()
        model1 = sm1.company_setting()

        sm2 = settings_manager()
        sm2.file_name=filename2
        sm2.load()
        model2 = sm2.company_setting()

        #Проверка
        assert model1.name=="Romashka"
        assert model2.name=="Oduvanchik"

    #Тестирование заполнения ID и сравнения моделей склада
    def test_set_id_storage_model(self):
        #Подготовка
        id = "2131231312"
        #Действие
        storage1 = storage_model()
        storage1.id=id
        storage2 = storage_model()
        storage2.id=id

        #Проверка
        assert storage1==storage2
    
    #Тестирование заполнения полей модели единицы измерения
    @pytest.mark.parametrize("name, coeff, result", [
        ("грамм", 1.0, does_not_raise()),
        ("A"*51, 1.0, pytest.raises(argument_exception)),
        (1, 1.0, pytest.raises(argument_exception)),
        ("грамм", 1, pytest.raises(argument_exception)),
        (None, 1.0, pytest.raises(argument_exception)),
        ("грамм", None, pytest.raises(argument_exception)),
        ])
    def test_input_fields_range_model(self, name, coeff, result):
        #Проверка на возникновение ошибок
        with result:
            #Действие
            rng = range_model(name, coeff)
            #Проверка
            assert rng.name == name
            assert rng.coeff == coeff
    
    #Тестирование присвоение базовой единицы измерения
    def test_use_base_range(self):
        #Подготовка
        base_range=range_model("грамм",1.0)
        #Действие
        other_range = range_model("Килограмм", 1000.0, base_range)
        #Проверка
        assert other_range.base_range.name == "грамм"
    
    #Тестирование заполнения полей в модели группы номенклатуры
    @pytest.mark.parametrize("name, result", [
        ("Продукты", does_not_raise()),
        ("A"*51, pytest.raises(argument_exception)),
        (1, pytest.raises(argument_exception)),
        (None, pytest.raises(argument_exception))
        ])
    def test_input_fields_nomenclature_group_model(self, name, result):
        #Подготовка
        gm = nomenclature_group_model()
        #Проверка на наличие ошибок
        with result:
            #Действие
            gm.name=name
            #Проверка
            assert gm.name==name
    
    #Тестирование заполнения полей в модели номенклатуры
    @pytest.mark.parametrize("attr_name, attr_value, result", [
        ("name","Белый хлеб",does_not_raise()),
        ("name","A"*51,pytest.raises(argument_exception)),
        ("name",1,pytest.raises(argument_exception)),
        ("name",None,pytest.raises(argument_exception)),
        ("full_name","Хлеб белый, Пшеничный, 3 сорт",does_not_raise()),
        ("full_name","A"*256,pytest.raises(argument_exception)),
        ("full_name",1,pytest.raises(argument_exception)),
        ("full_name",None,pytest.raises(argument_exception)),
        ("range_count",range_model("грамм",1.0),does_not_raise()),
        ("range_count",1,pytest.raises(argument_exception)),
        ("range_count",None,pytest.raises(argument_exception)),
        ("group",nomenclature_group_model(), does_not_raise()),
        ("group",1, pytest.raises(argument_exception)),
        ("group",None, pytest.raises(argument_exception))
    ])
    def test_input_fields_nomenclature_model(self, attr_name, attr_value, result):
        #Подготовка
        nm = nomenclature_model()
        #Проверка на наличие ошибок
        with result:
            #Действие
            setattr(nm, attr_name, attr_value)
            #Проверка
            assert getattr(nm,attr_name,None) == attr_value
    
    #Тестирование заполнения полей в модели настроек
    @pytest.mark.parametrize("attr_name, attr_value, result", [
        ("name","Настройки", does_not_raise()),
        ("name","A"*51, pytest.raises(argument_exception)),
        ("name",1, pytest.raises(argument_exception)),
        ("name",None, pytest.raises(argument_exception)),
        ("company",company_model(), does_not_raise()),
        ("company",1, pytest.raises(argument_exception)),
        ("company",None, pytest.raises(argument_exception))
        ])
    def test_input_fields_settings_model(self,attr_name, attr_value, result):
        #Подготовка
        sm = settings_model()
        #Проверка на наличие ошибок
        with result:
            #Действие
            setattr(sm, attr_name, attr_value)
            #Проверка
            assert getattr(sm,attr_name,None) == attr_value


        

    

    

    

        
        



