class company_model:
    __name:str = ""
    __INN:str = ""
    __account:str = ""
    __cor_account:str = ""
    __BIK:str = ""
    __type_of_own:str = ""


    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        if value.strip()!="":
            self.__name = value.strip()
    
    @property
    def INN(self) -> str:
        return self.__INN

    @INN.setter
    def INN(self, value:str):
        if value.strip()!="" and len(value.strip())<=12:
            self.__INN = value.strip()
    
    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value:str):
        if value.strip()!="" and len(value.strip())<=11:
            self.__account = value.strip()
    
    @property
    def cor_account(self) -> str:
        return self.__cor_account

    @cor_account.setter
    def cor_account(self, value:str):
        if value.strip()!="" and len(value.strip())<=11:
            self.__cor_account = value.strip()
    
    @property
    def BIK(self) -> str:
        return self.__BIK

    @BIK.setter
    def BIK(self, value:str):
        if value.strip()!="" and len(value.strip())<=9:
            self.__BIK = value.strip()

    @property
    def type_of_own(self) -> str:
        return self.__type_of_own
    @type_of_own.setter
    def type_of_own(self, value:str):
        if value.strip()!="" and len(value.strip())<=5:
            self.__type_of_own = value.strip()

            
