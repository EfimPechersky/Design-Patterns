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
    def test_check_create_company_model(self):
        model = company_model()
        assert model.name == ""

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
    def test_different_parameters_company_model(self,attr_name, attr_value, result ):
        with result:
            model = company_model()
            setattr(model, attr_name, attr_value)
            assert getattr(model,attr_name,None) == attr_value

    def test_load_createmodel_companymodel(self):
        filename = './settings.json'
        sm = settings_manager()
        sm.file_name=filename
        #Действие
        result=sm.load()
        #Проверка
        assert result==True
    
    def test_copy_from_settings_companymodel(self):
        filename = './settings.json'
        sm = settings_manager()
        sm.file_name=filename
        #Действие
        sm.load()
        #Проверка
        company = company_model(sm.settings().company)
        assert company.name == "Romashka"

    def test_compare_createmodel_companymodel(self):
        filename = "./settings.json"
        sm1 = settings_manager()
        sm1.file_name=filename
        sm2 = settings_manager()
        sm2.file_name=filename
        sm1.load()
        sm2.load()
        #Действие
        model1 = sm1.company_setting()
        model2 = sm2.company_setting()

        #Проверка
        assert model1.name==model2.name

    #Проверка относительных путей
    def test_load_different_settings(self):
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

    def test_inputs_storage_model_create(self):
        #Подготовка
        id = "2131231312"
        storage1 = storage_model()
        storage1.id=id
        storage2 = storage_model()
        storage2.id=id

        #Действие
        assert storage1==storage2
    
    @pytest.mark.parametrize("name, coeff, result", [
        ("грамм", 1.0, does_not_raise()),
        ("A"*51, 1.0, pytest.raises(argument_exception)),
        (1, 1.0, pytest.raises(argument_exception)),
        ("грамм", 1, pytest.raises(argument_exception)),
        (None, 1.0, pytest.raises(argument_exception)),
        ("грамм", None, pytest.raises(argument_exception)),
        ])
    def test_create_range_model(self, name, coeff, result):
        with result:
            rng = range_model(name, coeff)
            assert rng.name == name
            assert rng.coeff == coeff
    
    def test_use_base_range(self):
        base_range=range_model("грамм",1.0)
        other_range = range_model("Килограмм", 1000.0, base_range)
        assert other_range.base_range.name == "грамм"
    
    @pytest.mark.parametrize("name, result", [
        ("Продукты", does_not_raise()),
        ("A"*51, pytest.raises(argument_exception)),
        (1, pytest.raises(argument_exception)),
        (None, pytest.raises(argument_exception))
        ])
    def test_create_nomenclature_group_model(self, name, result):
        gm = nomenclature_group_model()
        with result:
            gm.name=name
            assert gm.name==name
    
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
    def test_create_nomenclature_model(self, attr_name, attr_value, result):
        with result:
            nm = nomenclature_model()
            setattr(nm, attr_name, attr_value)
            assert getattr(nm,attr_name,None) == attr_value
    
    @pytest.mark.parametrize("attr_name, attr_value, result", [
        ("name","Настройки", does_not_raise()),
        ("name","A"*51, pytest.raises(argument_exception)),
        ("name",1, pytest.raises(argument_exception)),
        ("name",None, pytest.raises(argument_exception)),
        ("company",company_model(), does_not_raise()),
        ("company",1, pytest.raises(argument_exception)),
        ("company",None, pytest.raises(argument_exception))
        ])
    def test_create_settings_model(self,attr_name, attr_value, result):
        sm = settings_model()
        with result:
            setattr(sm, attr_name, attr_value)
            assert getattr(sm,attr_name,None) == attr_value

        

    

    

    

        
        



