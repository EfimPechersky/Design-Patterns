from .abstract_model import abstract_model
from Models.nomenclature_model import nomenclature_model
from Models.range_model import range_model
from Models.storage_model import storage_model
from Models.osv_item_model import osv_item_model
from Models.transaction_model import transaction_model
from Core.validator import validator, argument_exception, operation_exception
from Dto.osv_dto import osv_dto,osv_item_dto
from datetime import datetime
# Модель ОСВ
class osv_model(abstract_model):
    __storage:storage_model
    __start_date:datetime
    __end_date:datetime
    __osv_items=[]
    def __init__(self):
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
    
    def find_item_by_nomenclature(self,nomencalture):
        for item in self.osv_items:
            if item.nomenclature == nomencalture:
                return item
        raise operation_exception("Строка не найдена!")
    
    def fill_rows(self, transactions, nomenclatures):
        osv_items=[]
        for nomenclature in nomenclatures:
            range=nomenclature.range_count
            if not nomenclature.range_count.base_range is None:
                range=nomenclature.range_count.base_range
            osv_items+=[osv_item_model.create(nomenclature,range,0.0,0.0,0.0,0.0)]
        self.osv_items=osv_items
        for transaction in transactions:
            if transaction.storage.id==self.storage.id and transaction.date<=self.end_date:
                num=transaction.num
                item=self.find_item_by_nomenclature(transaction.nomenclature)
                if not transaction.range.base_range is None:
                    if transaction.range.base_range==item.range:
                        num=num*transaction.range.coeff
                if transaction.date<=self.start_date:
                    item.start_num+=num
                if transaction.date>=self.start_date:
                    if transaction.num>0:
                        item.addition+=num
                    else:
                        item.substraction+=num
                item.end_num+=num
    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(storage, start_date, end_date):
        item = osv_model()
        item.storage=storage
        item.start_date = start_date
        item.end_date = end_date
        item.osv_items=[]
        return item

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
        
    
