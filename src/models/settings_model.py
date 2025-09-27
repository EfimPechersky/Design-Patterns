from .company_model import company_model
from .abstract_model import abstract_model
class settings_model(abstract_model):
    __company:company_model = None

    @property
    def company(self) -> str:
        return self.__company
    @company.setter
    def company(self, value):
        if self.val.validate(value, company_model):
            self.__company = value