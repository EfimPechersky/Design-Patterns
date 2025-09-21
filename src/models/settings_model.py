from .company_model import company_model

class settings_model:
    __company:company_model = None

    @property
    def company(self) -> str:
        return self.__company
    @company.setter
    def company(self, value):
        if value!=None:
            self.__company = value