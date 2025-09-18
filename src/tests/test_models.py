from models.company_model import company_model
from models.model_loader import settings_manager
import json

class TestModels:
    def test_check_create_company_model(self):
        model = company_model()
        assert model.name == ""

    #Проверка создания модели и задания именя объекта
    def test_not_empty_create_model_company_model(self):
        #подготовка
        model=company_model()
        #задание имени
        model.name="test"
        #проверка
        assert model.name=="test"
    def test_load_createmodel_companymodel(self):
        filename = "D:/Design-Patterns/Design-patterns/src/settings.json"
        sm = settings_manager(filename)
        #Действие
        result=sm.load()
        #Проверка
        assert result==True

    def test_compare_createmodel_companymodel(self):
        filename = "D:/Design-Patterns/Design-patterns/src/settings.json"
        sm1 = settings_manager(filename)
        sm2 = settings_manager(filename)
        sm1.load()
        sm2.load()
        #Действие
        model1 = sm1.company_setting()
        model2 = sm2.company_setting()

        #Проверка
        assert model1==model2


