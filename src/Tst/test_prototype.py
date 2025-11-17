from Logics.prototype import prototype
from Logics.prototype_report import prototype_report
from Core.start_service import start_service
from Core.repository import repository
from datetime import datetime
from Dto.filter_dto import filter_dto
import pytest
#Тестирование класса прототипа
class TestPrototype:
    start = start_service()
    start.start(file=True)
    #Тестирование создание прототипа
    def test_create_prototype(self):
        #Подготовка
        nom=self.start.data[repository.nomenclature_key()]
        #Действие
        prot=prototype_report(nom)
        #Проверка
        assert len(prot.data)==len(nom)
    
    #Тестирование клонирования прототипа
    def test_clone_prototype(self):
        #Подготовка
        nom=self.start.data[repository.nomenclature_key()]
        rang=self.start.data[repository.range_key()]
        #Действие
        prot1=prototype_report(rang)
        prot2=prot1.clone(nom)
        prot3=prot1.clone(None)
        #Проверка
        assert len(prot2.data)==len(nom)
        assert len(prot3.data)==len(rang)
    
    #Тестирование фильтрации
    def test_prototype_filter(self):
        start_prototype=prototype_report(self.start.data[repository.transaction_key()])
        print(self.start.data)
        find_nomenclature = self.start.data[repository.nomenclature_key()][0]
        dto=filter_dto()
        dto.field_name="nomenclature.name"
        dto.condition="EQUALS"
        dto.value=find_nomenclature.name
        #Действие
        test_nom_prototype = prototype_report.filter(start_prototype,dto)
        dto.field_name="num"
        dto.condition="LESS"
        dto.value=0
        test_add_prototype=prototype_report.filter(test_nom_prototype,dto)
        #Проверка
        assert len(test_nom_prototype.data)==2
        assert len(test_add_prototype.data)==1
    
    #Тестирование фильтрации при помощи вызова функции у объекта прототипа
    def test_prototype_chain(self):
        start_prototype=prototype_report(self.start.data[repository.transaction_key()])
        print(self.start.data)
        find_nomenclature = self.start.data[repository.nomenclature_key()][0]
        dto=filter_dto()
        dto.field_name="nomenclature.name"
        dto.condition="EQUALS"
        dto.value=find_nomenclature.name
        #Действие
        test_nom_prototype = start_prototype.filter(dto)
        dto.field_name="num"
        dto.condition="LESS"
        dto.value=0
        test_add_prototype=test_nom_prototype.filter(dto)
        #Проверка
        assert len(test_nom_prototype.data)==2
        assert len(test_add_prototype.data)==1


