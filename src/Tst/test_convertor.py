from Convert.basic_convertor import basic_convertor
from Convert.datetime_convertor import datetime_convertor
from Convert.reference_convertor import reference_convertor
from Convert.convert_factory import convert_factory
from Models.range_model import range_model
from Models.abstract_model import abstract_model
from Models.nomenclature_model import nomenclature_model
from Models.ingridient_model import ingridient_model
from Models.group_model import nomenclature_group_model
from Models.receipt_model import receipt_model
from datetime import datetime
from Core.validator import validator, argument_exception
import pytest
class TestConvertor:

    @pytest.mark.parametrize("obj", [(1),("string"),(1.0),False])
    def test_basic_convertor_convert(self,obj):
        #Подготовка
        bc=basic_convertor()
        #Проверка
        assert bc.convert(obj)==obj
    def test_basic_convertor_wrong_type_error(self):
        #Подготовка
        bc=basic_convertor()
        #Проверка
        with pytest.raises(argument_exception):
            bc.convert(["list"])

    def test_datetime_convertor_convert(self):
        #Подготовка
        dc=datetime_convertor()
        obj=datetime(2025,12,31)
        res={'day': 31, 'fold': 0, 'hour': 0, 'microsecond': 0, 'minute': 0, 'month': 12, 'second': 0, 'year': 2025}
        #Проверка
        assert dc.convert(obj)==res
    
    def test_datetime_convertor_wrong_type_error(self):
        #Подготовка
        dc=datetime_convertor()
        #Проверка
        with pytest.raises(argument_exception):
            dc.convert(1)
    

    @pytest.mark.parametrize("obj, name", [
        (range_model.create_gramm(), "грамм"),
        (nomenclature_group_model.create_milk_products(), "Молочные продукты"),
        (nomenclature_model.create_butter(), "Сливочное масло"),
        (receipt_model.create_waffles_receipt(), "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ")])
    def test_reference_convertor_convert(self,obj,name):
        #Подготовка
        rc=reference_convertor()
        #Проверка
        assert rc.convert(obj)["name"]==name
    
    def test_reference_convertor_wrong_type_error(self):
        #Подготовка
        rc=reference_convertor()
        #Проверка
        with pytest.raises(argument_exception):
           rc.convert(1)
    
    @pytest.mark.parametrize("obj, num", [
        ([range_model.create_gramm(),range_model.create_kilogramm(),range_model.create_liter()],3),
        ([nomenclature_group_model.create_milk_products(),nomenclature_group_model.create_addition_products()],2),
        ([nomenclature_model.create_butter(),nomenclature_model.create_cacao(),nomenclature_model.create_eggs()], 3),
        ([receipt_model.create_waffles_receipt(),receipt_model.create_pie_receipt()], 2)])
    def test_convert_factory_convertation(self, obj, num):
        #Подготовка
        cf=convert_factory()
        #Проверка
        assert len(cf.rec_convert(obj))==num