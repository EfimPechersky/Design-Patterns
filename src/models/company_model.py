class company_model:
    __name:str = ""
    #Изменил тип на целочисленный
    __INN:int = 0
    __account:int = 0
    __cor_account:int = 0
    __BIK:int = 0
    __type_of_own:str = ""


    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        if value.strip()!="":
            self.__name = value.strip()
    
    @property
    def INN(self) -> int:
        return self.__INN

    @INN.setter
    def INN(self, value:int):
        if value>0 and len(str(value))<=12:
            self.__INN = value
            
    @property
    def account(self) -> int:
        return self.__account

    @account.setter
    def account(self, value:int):
        if value>0 and len(str(value))<=11:
            self.__account = value
    
    @property
    def cor_account(self) -> int:
        return self.__cor_account

    @cor_account.setter
    def cor_account(self, value:int):
        if value>0 and len(str(value))<=11:
            self.__cor_account = value
    
    @property
    def BIK(self) -> int:
        return self.__BIK

    @BIK.setter
    def BIK(self, value:int):
        if value>0 and len(str(value))<=9:
            self.__BIK = value

    @property
    def type_of_own(self) -> str:
        return self.__type_of_own
    @type_of_own.setter
    def type_of_own(self, value:str):
        if value.strip()!="" and len(value.strip())<=5:
            self.__type_of_own = value.strip()
    
    def load_from_dict(self,data:dict)->bool:
        fields=["name", "INN", "account", "cor_account", "BIK", "type_of_own"]
        for i in fields:
            if i not in data:
                return False
        self.name=data['name']
        self.INN=data['INN']
        self.account=data['account']
        self.cor_account=data['cor_account']
        self.BIK=data['BIK']
        self.type_of_own=data['type_of_own']
        return True


            
