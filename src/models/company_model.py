from core.validator import validator
from .abstract_model import abstract_model
from core.validator import argument_exception, operation_exception
class company_model(abstract_model):
    __INN:int = 0
    __account:int = 0
    __cor_account:int = 0
    __BIK:int = 0
    __type_of_own:str = ""
    
    #Вместо settings передается company,
    #Иначе возникает проблема цикличного импорта из settings_model в company_model и наоборот
    def __init__(self, company = None):
        if not company is None:
            fields = list(filter(lambda x: not x.startswith("_") , dir(self)))
            
            other_fields = list(filter(lambda x: not x.startswith("_") , dir(company)))
            try:
                for key in other_fields:
                    attr=getattr(company,key,None)
                    if not attr is None:
                        setattr(self, key, attr)
            except:
                raise operation_exception("Загруженные настройки организации содержат не все поля")

    @property
    def INN(self) -> int:
        return self.__INN

    @INN.setter
    def INN(self, value:int):
        if self.val.validate(value, int, 12):
            self.__INN = value
            
    @property
    def account(self) -> int:
        return self.__account

    @account.setter
    def account(self, value:int):
        if self.val.validate(value, int, 11):
            self.__account = value
    
    @property
    def cor_account(self) -> int:
        return self.__cor_account

    @cor_account.setter
    def cor_account(self, value:int):
        if self.val.validate(value, int, 11):
            self.__cor_account = value
    
    @property
    def BIK(self) -> int:
        return self.__BIK

    @BIK.setter
    def BIK(self, value:int):
        if self.val.validate(value, int, 9):
            self.__BIK = value

    @property
    def type_of_own(self) -> str:
        return self.__type_of_own
    @type_of_own.setter
    def type_of_own(self, value:str):
        if self.val.validate(value, str, 5):
            self.__type_of_own = value.strip()
    
    


            
