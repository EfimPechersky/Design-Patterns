from Core.abstract_dto import abstract_dto
from Core.validator import validator,operation_exception
from .ingridient_dto import ingridient_dto

class receipt_dto(abstract_dto):
    # Шаги приготовления
    def __init__(self):
        self.__steps = []  # Теперь это атрибут экземпляра
        self.__ingridients = []  # Добавил инициализацию для ingridients


    # Шаги приготовления
    @property
    def steps(self) -> list:
        return self.__steps
    
    @steps.setter
    def steps(self, value):
        for i in value:
            if i.strip()!="":
                self.__steps+=[i.strip()]

    # Состав
    @property
    def ingridients(self) -> list:
        return self.__ingridients

    def create(self, data) -> "receipt_dto":
        validator.validate(data, dict)
        try:
            self.name=data["name"]
            self.steps=data["steps"]
            for i in data["ingridients"]:
                self.ingridients.append(ingridient_dto().create(i))
        except:
            raise   operation_exception("Невозможно загрузить данные!")    

        return self
    
    # Универсальный фабричный метод для загрузщки dto из словаря
    def to_dict(self) -> "abstract_dto":
        dict={}
        try:
            dict["name"]=self.name
            dict["ingridients"]=[]
            dict["steps"]=[]
            for i in self.steps:
                if str(i).strip()!="":
                    dict["steps"]+=[str(i).strip()]
            for i in self.ingridients:
                dict["ingridients"].append(i.to_dict())
        except:
            raise   operation_exception("Невозможно преобразовать данные!") 
        return dict
    
    
