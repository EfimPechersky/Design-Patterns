from Core.repository import repository
from Models.range_model import range_model
from Models.group_model import nomenclature_group_model
from Models.nomenclature_model import nomenclature_model
from Models.osv_model import osv_model
from Core.validator import validator, argument_exception, operation_exception
import os
import json
from Models.receipt_model import receipt_model
from Models.storage_model import storage_model
from Models.transaction_model import transaction_model
from Dto.nomenclature_dto import nomenclature_dto
from Dto.range_dto import range_dto
from Dto.group_dto import group_dto
from Dto.receipt_dto import receipt_dto
from Dto.storage_dto import storage_dto
from Dto.transaction_dto import transaction_dto
from Convert.convert_factory import convert_factory
class start_service:
    # Репозиторий
    __repo: repository = repository()

    # Рецепт по умолчанию
    __default_receipts: list

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # Наименование файла (полный путь)
    __full_file_name:str = ""

    def __init__(self):
        self.__repo.initalize()

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance 

    # Текущий файл
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)        
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open( self.__full_file_name, 'r', encoding="UTF-8") as file_instance:
                settings = json.load(file_instance)
                first_start=settings["first_start"] if "first_start" in settings else False
                if not first_start:
                    self.default_create_range()
                    self.default_create_group()
                    self.default_create_nomenclature()
                    self.default_create_receipt()
                    return True
                if "receipts" in settings.keys():
                    data = settings["receipts"]
                    self.__convert_ranges(settings)
                    self.__convert_groups(settings)
                    self.__convert_nomenclatures(settings)
                    rec_res=self.convert(data)
                    stor_res=self.__convert_storages(settings)
                    tran_res=self.__convert_transactions(settings)
                    return rec_res and stor_res and tran_res
                    
                    

            return False
        except Exception as e:
            error_message = str(e)
            return False
        
    # Сохранить элемент в репозитории
    def __save_item(self, key:str, dto, item):
        validator.validate(key, str)
        item.id = dto.id
        if not dto.id in self.__cache.keys():
            self.__cache.setdefault(dto.id, item)
            self.__repo.data[ key ].append(item)

    # Загрузить единицы измерений   
    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data['ranges'] if 'ranges' in data else []    
        if len(ranges) == 0:
            return False
         
        for range in ranges:
            dto = range_dto().create(range)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item( repository.range_key(), dto, item )

        return True

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        groups =  data['groups'] if 'groups' in data else []    
        if len(groups) == 0:
            return False

        for category in  groups:
            dto = group_dto().create(category)    
            item = nomenclature_group_model.from_dto(dto, self.__cache )
            self.__save_item( repository.group_key(), dto, item )

        return True

    # Загрузить номенклатуру
    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)      
        nomenclatures = data['nomenclatures'] if 'nomenclatures' in data else []   
        if len(nomenclatures) == 0:
            return False
        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item( repository.nomenclature_key(), dto, item )

        return True   

    def __convert_storages(self, data: dict) -> bool:
        validator.validate(data, dict)
        storages = data['storages'] if 'storages' in data else []
        if len(storages) == 0:
            return False
        for storage in storages:
            dto = storage_dto().create(storage)
            item = storage_model.from_dto(dto, self.__cache)
            self.__save_item( repository.storage_key(), dto, item )

        return True       

    def __convert_transactions(self, data: dict) -> bool:
        validator.validate(data, dict)      
        transactions = data['transactions'] if 'transactions' in data else []   
        if len(transactions) == 0:
            return False
        for transaction in transactions:
            dto = transaction_dto().create(transaction)
            item = transaction_model.from_dto(dto, self.__cache)
            self.__save_item( repository.transaction_key(), dto, item )

        return True 

    # Обработать полученный словарь    
    def convert(self, data: list) -> bool:
        validator.validate(data, list)
        for receipt in data:
            # Собираем рецепт
            dto=receipt_dto().create(receipt)
            default_receipt=receipt_model.from_dto(dto,self.__cache)
            # Сохраняем рецепт
            self.__repo.data[ repository.receipt_key() ].append(default_receipt)
        return True

    """
    Стартовый набор данных
    """
    @property
    def data(self):
        return self.__repo.data   

    """Репозиторий с данными"""
    @property
    def repository(self):
        return self.__repo
    

    
    """Запись дефолтных значений единицы измерения"""
    def default_create_range(self):
        self.__repo.data[repository.range_key()].append(range_model.create_gramm(self.__repo))
        self.__repo.data[repository.range_key()].append(range_model.create_kilogramm(self.__repo))
        self.__repo.data[repository.range_key()].append(range_model.create_num(self.__repo))
        self.__repo.data[repository.range_key()].append(range_model.create_liter(self.__repo))
        self.__repo.data[repository.range_key()].append(range_model.create_milliliter(self.__repo))

    
    """Запись дефолтных значений групп"""
    def default_create_group(self):
        self.__repo.data[repository.group_key()].append(nomenclature_group_model.create_animal_products(self.__repo))
        self.__repo.data[repository.group_key()].append(nomenclature_group_model.create_sugar_products(self.__repo))
        self.__repo.data[repository.group_key()].append(nomenclature_group_model.create_milk_products(self.__repo))
        self.__repo.data[repository.group_key()].append(nomenclature_group_model.create_grain_products(self.__repo))
        self.__repo.data[repository.group_key()].append(nomenclature_group_model.create_seasoning_products(self.__repo))
        self.__repo.data[repository.group_key()].append(nomenclature_group_model.create_addition_products(self.__repo))
    
    """Запись дефолтных значений номенклатуры"""
    def default_create_nomenclature(self):
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_flour(self.__repo))
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_sugar(self.__repo))
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_butter(self.__repo))
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_eggs(self.__repo))
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_vanilla(self.__repo))
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_sour_cream(self.__repo))
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_cacao(self.__repo))
        self.__repo.data[repository.nomenclature_key()].append(nomenclature_model.create_soda(self.__repo))
    
    """Запись дефолтных значений рецептов"""
    def default_create_receipt(self):
        self.__repo.data[repository.receipt_key()].append(receipt_model.create_waffles_receipt(self.__repo))
        self.__repo.data[repository.receipt_key()].append(receipt_model.create_pie_receipt(self.__repo))
    
        
    def create_osv(self, start, end, storage_id):
        transactions=self.__repo.data[repository.transaction_key()]
        nomenclatures = self.__repo.data[repository.nomenclature_key()]
        storage=self.__cache[storage_id] if storage_id in self.__cache else None
        validator.validate(storage, storage_model)
        osv=osv_model.create(storage,start,end,nomenclatures)
        osv.fill_rows(transactions)
        return osv

    def dump(self, filename):
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")
        try:
            alldata={}
            cf=convert_factory()
            for k in repository.keys():
                alldata[k]=[]
                for i in self.__repo.data[k]:
                    alldata[k]+=[cf.rec_convert(i)]
            with open(filename, 'w', encoding="UTF-8") as file_instance:
                json.dump(alldata,file_instance,ensure_ascii=False,indent=4)
            return True
        except Exception as e:
            error_message = str(e)
            return False
    """
    Основной метод для генерации эталонных данных
    """
    def start(self, file=False):
        if file:
            self.file_name = "./settings.json"
            result = self.load()
            if result == False:
                raise operation_exception("Невозможно сформировать стартовый набор данных!")
            return
        self.default_create_range()
        self.default_create_group()
        self.default_create_nomenclature()
        self.default_create_receipt()