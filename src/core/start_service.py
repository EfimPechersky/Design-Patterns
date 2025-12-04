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
from Dto.filter_dto import filter_dto
from Convert.convert_factory import convert_factory
from datetime import datetime
from Models.stock_model import stock_model
from Logics.prototype_report import prototype_report
from Core.observe_service import observe_service
from Core.event_type import event_type
class start_service:
    # Репозиторий
    __repo: repository = repository()
    #Дата блокировки
    __block_period:datetime = None

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    #Словарь для хранения дто и моделей относящихся к типу референса

    __references={
        repository.range_key():[range_dto,range_model],
        repository.storage_key():[storage_dto,storage_model],
        repository.nomenclature_key():[nomenclature_dto,nomenclature_model],
        repository.group_key():[group_dto, nomenclature_group_model],
        repository.transaction_key():[transaction_dto,transaction_model],
        repository.receipt_key():[receipt_dto,receipt_model]
        }

    # Наименование файла (полный путь)
    __full_file_name:str = ""
    
    
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
                    self.convert_any(settings, repository.range_key())
                    self.convert_any(settings, repository.storage_key())
                    self.convert_any(settings, repository.group_key())
                    self.convert_any(settings, repository.nomenclature_key())
                    self.convert_any(settings, repository.receipt_key())
                    self.convert_any(settings, repository.transaction_key())
                    return True
                    
                    

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
    

    #Добавить объект
    def add_reference(self,reference_type:str,data:dict):
        validator.validate(data, dict)
        validator.validate(reference_type,str)
        reference_dto=self.__references[reference_type][0]
        model=self.__references[reference_type][1]
        dto = reference_dto().create(data)
        item = model.from_dto(dto, self.__cache )
        if dto.id in self.__cache:
            return False
        self.__save_item(reference_type, dto, item )
        return True
    
    #Изменить объект
    def change_reference(self,reference_type:str,data:dict):
        validator.validate(data, dict)
        validator.validate(reference_type,str)
        reference_dto=self.__references[reference_type][0]
        model=self.__references[reference_type][1]
        dto = reference_dto().create(data)
        item = model.from_dto(dto, self.__cache )
        references=prototype_report(self.data[reference_type])
        filt=filter_dto()
        filt.field_name="id"
        filt.value=dto.id
        filt.condition="EQUALS"
        found_reference=references.filter(filt).data
        if len(found_reference)==0:
            return False
        fields = list(filter(lambda x: not x.startswith("_") , dir(found_reference[0])))
        
        for field in fields:
            attribute = getattr(found_reference[0].__class__,field)
            if isinstance(attribute, property):
                value = getattr(item, field)
                setattr(found_reference[0], field, value)
        return True

    #Преобразование референса любого типа
    def convert_any(self, data:dict, reference_type:str):
        validator.validate(data, dict)
        validator.validate(reference_type,str)
        if reference_type not in self.__references:
            return False
        references =  data[reference_type] if reference_type in data else []    
        if len(references) == 0:
            return False

        reference_dto=self.__references[reference_type][0]
        model=self.__references[reference_type][1]
        for category in references:
            dto = reference_dto().create(category)    
            item = model.from_dto(dto, self.__cache )
            self.__save_item(reference_type, dto, item )

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
    
    """
    Дата блокировки
    """
    @property
    def block_period(self):
        return self.__block_period   
    
    @block_period.setter
    def block_period(self, value):
        validator.validate(value, datetime)
        self.__block_period=value
        observe_service.create_event(event_type.change_block_period(),self.__block_period)

    @staticmethod
    def get_model_by_type(reference_type):
        if reference_type in start_service.__references:
            return start_service.__references[reference_type]
        return None
            

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
    
    """
    Создание ОСВ
    """
    def create_osv(self, start, end, storage_id):
        if start>end:
            raise argument_exception("Начальная дата ОСВ позже конечной даты")
        if self.__block_period!=None:
            if start<self.__block_period:
                raise argument_exception("Начальная дата ОСВ меньше даты блокировки")
        transactions=self.__repo.data[repository.transaction_key()]
        nomenclatures = self.__repo.data[repository.nomenclature_key()]
        stocks = self.__repo.data[repository.stock_key()]
        storage=self.__cache[storage_id] if storage_id in self.__cache else None
        validator.validate(storage, storage_model)
        osv=osv_model.create(storage,start,end,nomenclatures)
        osv.fill_rows(transactions,self.__block_period,stocks)
        return osv

    """
    Создание ОСВ при помощи фильтров
    """
    def create_osv_with_filters(self, filters):
        transactions=self.__repo.data[repository.transaction_key()]
        nomenclatures = self.__repo.data[repository.nomenclature_key()]
        stocks=self.__repo.data[repository.stock_key()]
        osv=osv_model.filters_osv(filters, transactions, nomenclatures, self.block_period, stocks)
        return osv
    """
    Основной метод для генерации эталонных данных
    """
    def start(self, file=False):
        self.__cache = {}
        self.__repo: repository = repository()
        self.__repo.initalize()
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