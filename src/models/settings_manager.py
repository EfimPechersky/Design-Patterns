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
        self.__filename = filename
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
        fields=["name", "INN", "account", "cor_account", "BIK", "type_of_own"]
        if self.filename.strip()=="":
            raise Exception("No filename!")
        try:
            with open(self.filename,'r') as file:
                data = json.load(file)
                if "company" in data:
                    item=data["company"]
                    for i in fields:
                        if i not in item:
                            return False
                    self.__settings.company.name=item['name']
                    self.__settings.company.INN=item['INN']
                    self.__settings.company.account=item['account']
                    self.__settings.company.cor_account=item['cor_account']
                    self.__settings.company.BIK=item['BIK']
                    self.__settings.company.type_of_own=item['type_of_own']
                    return True
                return False
        except:
            return False
    
    def default(self):
        self.__settings = settings_model()
        self.__settings.company = company_model()
        self.__settings.company.name = "Company Name"
        self.__settings.company.INN="000000000000"
        self.__settings.company.account="00000000000"
        self.__settings.company.cor_account="00000000000"
        self.__settings.company.BIK="000000000"
        self.__settings.company.type_of_own="AAAAA"

    
                    
        
        



