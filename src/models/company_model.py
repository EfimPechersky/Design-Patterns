from Core.validator import validator
from .abstract_model import abstract_model
from Core.validator import argument_exception, operation_exception
"""
Класс, описывающий параметры организации
"""
class company_model(abstract_model):
    __inn:int = 0
    __account:int = 0
    __cor_account:int = 0
    __bik:int = 0
    __type_of_own:str = ""
    
    
    def __init__(self, company = None):
        """
        Копирование настроек компании из seetings_model
        Args:
            company (any): загруженные настройки компании
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            None или Exception
        """
        if not company is None and validator.validate(company, company_model):
            fields = list(filter(lambda x: not x.startswith("_") , dir(self)))
            
            other_fields = list(filter(lambda x: not x.startswith("_") , dir(company)))
            try:
                for key in other_fields:
                    if key=="id" or key not in fields:
                        continue
                    attr=getattr(company,key,None)
                    if not attr is None:
                        setattr(self, key, attr)
            except:
                raise operation_exception("Загруженные настройки организации содержат не все поля")

    """
    ИНН
    """
    @property
    def inn(self) -> int:
        return self.__inn

    """
    Валидация и присвоение ИНН
    """
    @inn.setter
    def inn(self, value:int):
        if validator.validate(value, int, 12):
            self.__inn = value

    """Счёт"""        
    @property
    def account(self) -> int:
        return self.__account

    """Валидация и присвоение счёта"""
    @account.setter
    def account(self, value:int):
        if validator.validate(value, int, 11):
            self.__account = value
    
    """Корреспондентский счёт"""
    @property
    def cor_account(self) -> int:
        return self.__cor_account

    """Валидация и присвоение корреспондентского счёта"""
    @cor_account.setter
    def cor_account(self, value:int):
        if validator.validate(value, int, 11):
            self.__cor_account = value
    
    """БИК"""
    @property
    def bik(self) -> int:
        return self.__bik

    """Валидация и присвоение БИК"""
    @bik.setter
    def bik(self, value:int):
        if validator.validate(value, int, 9):
            self.__bik = value

    """Форма собственности"""
    @property
    def type_of_own(self) -> str:
        return self.__type_of_own
    
    """Валидация и присвоение формы собственности"""
    @type_of_own.setter
    def type_of_own(self, value:str):
        if validator.validate(value, str, 5):
            self.__type_of_own = value.strip()

    def __repr__(self):
        return "Company "+super().__repr__()
    
    


            
