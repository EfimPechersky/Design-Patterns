from .company_model import company_model
from .settings_model import settings_model
import json
import os
class settings_manager:
    __filename:str=""
    __settings:settings_model = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager,cls).__new__(cls)
        return cls.instance
    
    def __init__(self,filename:str):
        self.__filename = os.path.relpath(filename)
        print(self.__filename)
        self.default()

    def settings(self)->settings_model:
        return self.__settings
    
    def company_setting(self)->company_model:
        return self.__settings.company
        
    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, value:str):
        if value.strip()=="":
            return
        if os.path.exists(value):
            self.__filename = value.strip()
        
    
    def load(self) -> bool:
        if self.filename.strip()=="":
            raise Exception("No filename!")
        try:
            with open(self.filename,'r') as file:
                data = json.load(file)
                if "company" in data:
                    item=data["company"]
                    #Проверку наличия параметров перенёс в company_model
                    res = self.__settings.company.load_from_dict(item)
                    return res
                return False
        except:
            return False
    
    def default(self):
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Company Name"
        self.__settings.company.INN=0
        self.__settings.company.account=0
        self.__settings.company.cor_account=0
        self.__settings.company.BIK=0
        self.__settings.company.type_of_own="AAAAA"

    
                    
        
        



