from .company_model import company_model
import json
import os
class settings_manager:
    __filename:str=""
    __company:company_model = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager,cls).__new__(cls)
        return cls.instance
    
    def __init__(self,filename:str):
        self.__filename = filename
        self.default()

    def company_setting(self)->company_model:
        return self.__company
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
                    if 'name' in item:
                        self.__company.name=item['name']
                        return True
                return False
        except:
            return False
    
    def default(self):
        self.__company=company_model()
        self.__company.name="Company Name"

    
                    
        
        



