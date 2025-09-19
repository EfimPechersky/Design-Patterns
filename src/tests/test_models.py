from models.company_model import company_model
from models.settings_manager import settings_manager
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

    def test_INN_limit_companymodel(self):
        model = company_model()
        model.INN = "1"*12
        model.INN = "0"*13
        assert model.INN == "1"*12
    
    def test_account_limit_companymodel(self):
        model = company_model()
        model.account = "1"*11
        model.account = "0"*12
        assert model.account == "1"*11
    
    def test_cor_account_limit_companymodel(self):
        model = company_model()
        model.cor_account = "1"*11
        model.cor_account = "0"*12
        assert model.cor_account == "1"*11
    
    def test_BIK_limit_companymodel(self):
        model = company_model()
        model.BIK = "1"*9
        model.BIK = "0"*10
        assert model.BIK == "1"*9
    
    def test_type_of_own_limit_companymodel(self):
        model = company_model()
        model.type_of_own = "O"*3
        model.type_of_own = "A"*6
        assert model.type_of_own == "O"*3


    def test_load_createmodel_companymodel(self):
        filename = 'src/settings.json'
        sm = settings_manager(filename)
        #Действие
        result=sm.load()
        #Проверка
        assert result==True

    def test_compare_createmodel_companymodel(self):
        filename = "src/settings.json"
        sm1 = settings_manager(filename)
        sm2 = settings_manager(filename)
        sm1.load()
        sm2.load()
        #Действие
        model1 = sm1.company_setting()
        model2 = sm2.company_setting()

        #Проверка
        assert model1==model2
    
    def test_load_different_settings(self):
        filename1 = "src/settings.json"
        filename2 = "src/settings_folder/other_settings.json"
        #Действие
        sm1 = settings_manager(filename1)
        sm1.load()
        model1 = sm1.company_setting()

        sm2 = settings_manager(filename2)
        sm2.load()
        model2 = sm2.company_setting()

        #Проверка
        assert model1.name=="Romashka"
        assert model2.name=="Oduvanchik"
    
    

        
        



