from Core.validator import validator,argument_exception
from Core.repository import repository
from Models.nomenclature_model import nomenclature_model
from Models.range_model import range_model
from Models.group_model import nomenclature_group_model
from Models.receipt_model import receipt_model
class start_service:
    __repository: repository = repository()
    __instance = None

    def __init__(self):
        self.__repository.data[repository.range_key] = []
        self.__repository.data[repository.group_key] = []
        self.__repository.data[repository.nomenclature_key] = []
        self.__repository.data[repository.receipt_key] = []

    """
    Реализация Singleton
    """
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(start_service, cls).__new__(cls)
        return cls.__instance
    
    """Репозиторий с данными"""
    @property
    def repository(self):
        return self.__repository
    

    
    """Запись дефолтных значений единицы измерения"""
    def default_create_range(self):
        self.__repository.data[repository.range_key].append(range_model.create_gramm(self.__repository))
        self.__repository.data[repository.range_key].append(range_model.create_kilogramm(self.__repository))
        self.__repository.data[repository.range_key].append(range_model.create_num(self.__repository))
        self.__repository.data[repository.range_key].append(range_model.create_liter(self.__repository))
        self.__repository.data[repository.range_key].append(range_model.create_milliliter(self.__repository))

    """Запись дефолтных значений групп"""
    def default_create_group(self):
        self.__repository.data[repository.group_key].append(nomenclature_group_model.create_animal_products(self.__repository))
        self.__repository.data[repository.group_key].append(nomenclature_group_model.create_sugar_products(self.__repository))
        self.__repository.data[repository.group_key].append(nomenclature_group_model.create_milk_products(self.__repository))
        self.__repository.data[repository.group_key].append(nomenclature_group_model.create_grain_products(self.__repository))
        self.__repository.data[repository.group_key].append(nomenclature_group_model.create_seasoning_products(self.__repository))
        self.__repository.data[repository.group_key].append(nomenclature_group_model.create_addition_products(self.__repository))
    """Запись дефолтных значений номенклатуры"""
    def default_create_nomenclature(self):
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_butter(self.__repository))
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_eggs(self.__repository))
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_flour(self.__repository))
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_sugar(self.__repository))
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_vanilla(self.__repository))
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_cacao(self.__repository))
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_soda(self.__repository))
        self.__repository.data[repository.nomenclature_key].append(nomenclature_model.create_sour_cream(self.__repository))
    """Запись дефолтных значений рецептов"""
    def default_create_receipt(self):
        self.__repository.data[repository.receipt_key].append(receipt_model.create_waffles_receipt(self.__repository))
        self.__repository.data[repository.receipt_key].append(receipt_model.create_pie_receipt(self.__repository))
    """Запуск сервиса"""
    def start(self):
        self.default_create_range()
        self.default_create_group()
        self.default_create_nomenclature()
        self.default_create_receipt()
    
    """Добавление ингридиента в список"""
    def add_new_proportion(receipt, nomenclature, number,range):
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(number, float)
        validator.validate(range,range_model)
        receipt.ingridients+=[(nomenclature,number,range)]

    """Добавление шага приготовления"""
    def add_step(receipt, step, number=-1):
        validator.validate(step,str)
        validator.validate(number, int)
        if number<-1 or number>len(receipt.steps):
            raise argument_exception("Номер шага рецепта неверен")
        if number != -1 and number<len(receipt.steps):
            receipt.steps = receipt.steps[:number] +[step] + receipt.steps[number:]
        else:
            receipt.steps+=[step]
    
