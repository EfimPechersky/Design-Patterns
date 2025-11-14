from .abstract_model import abstract_model
from Models.nomenclature_model import nomenclature_model
from Models.range_model import range_model
from Models.storage_model import storage_model
from Models.osv_item_model import osv_item_model
from Models.transaction_model import transaction_model
from Core.validator import validator, argument_exception, operation_exception
from Dto.osv_dto import osv_dto,osv_item_dto
from Logics.prototype_report import prototype_report
from Logics.prototype import prototype
from Dto.filter_dto import filter_dto
from datetime import datetime
# Модель ОСВ
class osv_model(abstract_model):
    __storage:storage_model
    __start_date:datetime
    __end_date:datetime
    __osv_items=[]
    __osv_dict={}
    def __init__(self):
        self.__osv_items=[]
        super().__init__()
    

    """Склад"""
    @property
    def storage(self):
        return self.__storage
    
    """Сеттер склада"""
    @storage.setter
    def storage(self,value):
        validator.validate(value,storage_model)
        self.__storage=value
    
    """Начальная дата"""
    @property
    def start_date(self):
        return self.__start_date
    
    """Сеттер начальной даты"""
    @start_date.setter
    def start_date(self,value):
        validator.validate(value,datetime)
        self.__start_date=value
    
    """Конечная дата"""
    @property
    def end_date(self):
        return self.__end_date
    
    """Сеттер конечной даты"""
    @end_date.setter
    def end_date(self,value):
        validator.validate(value,datetime)
        self.__end_date=value

    """Список строк ОСВ"""
    @property
    def osv_items(self):
        return self.__osv_items
    
    """Сеттер списка строк ОСВ"""
    @osv_items.setter
    def osv_items(self,value):
        validator.validate(value,list)
        for i in value:
            validator.validate(i,osv_item_model)
            self.osv_items.append(i)
    
    """
    Заполнение ОСВ
    """
    def fill_rows(self, transactions):
        dto=filter_dto()
        dto.field_name="storage.id"
        dto.value=self.storage.id
        dto.condition="EQUALS"
        new_prototype=prototype_report(transactions)
        new_prototype=prototype_report.filter(new_prototype,dto)
        dto.field_name="date"
        dto.value=self.end_date
        dto.condition="MORE"
        end_prototype=prototype_report.filter(new_prototype,dto)
        for item in self.osv_items:
            dto.field_name="nomenclature.name"
            dto.value=item.nomenclature.name
            dto.condition="EQUALS"
            nom_prototype=prototype_report.filter(end_prototype,dto)
            for transaction in nom_prototype.data:
                num=transaction.num
                if not transaction.range.base_range is None:
                    if transaction.range.base_range==item.range:
                        num=num*transaction.range.coeff
                if transaction.date<self.start_date:
                    item.start_num+=num
                else:
                    if num>0:
                        item.addition+=num
                    else:
                        item.substraction+=num
                
                item.end_num+=num
    """
    Создание ОСВ при помощи фильтров
    """
    @staticmethod
    def filters_osv(filters:dict, transactions, nomenclatures):
        osv=osv_model()
        osv.fill_empty_osv(nomenclatures)
        new_prototype=prototype_report(transactions)
        new_prototype=prototype_report.filter(new_prototype,filters["storage"])
        end_prototype=prototype_report.filter(new_prototype,filters["end_date"])
        start_prototype=prototype_report.filter(new_prototype,filters["start_date"])
        dto=filter_dto()
        for item in osv.osv_items:
            dto.field_name="nomenclature.name"
            dto.value=item.nomenclature.name
            dto.condition="EQUALS"
            nom_prototype=prototype_report.filter(start_prototype,dto)
            for transaction in nom_prototype.data:
                num=transaction.num
                if not transaction.range.base_range is None:
                    if transaction.range.base_range==item.range:
                        num=num*transaction.range.coeff
                item.start_num+=num
        for item in osv.osv_items:
            dto.field_name="nomenclature.name"
            dto.value=item.nomenclature.name
            dto.condition="EQUALS"
            nom_prototype=prototype_report.filter(end_prototype,dto)
            for transaction in nom_prototype.data:
                num=transaction.num
                if not transaction.range.base_range is None:
                    if transaction.range.base_range==item.range:
                        num=num*transaction.range.coeff
                if num>0:
                    item.addition+=num
                else:
                    item.substraction+=num
                item.end_num+=num
        return osv
    
    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(storage, start_date, end_date, nomenclatures):
        item = osv_model()
        item.storage=storage
        item.start_date = start_date
        item.end_date = end_date
        item.fill_empty_osv(nomenclatures)
        return item

    def fill_empty_osv(self,nomenclatures):
        osv_items=[]
        for nomenclature in nomenclatures:
            range=nomenclature.range_count
            if not nomenclature.range_count.base_range is None:
                range=nomenclature.range_count.base_range
            osv_items+=[osv_item_model.create(nomenclature,range,0.0,0.0,0.0,0.0)]
        self.osv_items=osv_items
    """
    Фабричный метод в Dto
    """
    def to_dto(self):
        item = osv_dto()
        osv_items=[]
        for i in self.osv_items:
            osv_items.append(i.to_dto())
        item.osv_items=osv_items
        item.start_date=self.start_date
        item.end_date = self.end_date
        item.storage_id = self.storage.id
        return item
    
    def __repr__(self):
        return "OSV "+super().__repr__()
        
    
