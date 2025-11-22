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
    def fill_rows(self, transactions, block_period=None,stocks=[]):
        dto=filter_dto()
        #Фильтруем транзакции после даты блокировки
        prot=prototype_report(transactions)
        dto.field_name="date"
        dto.value=block_period
        dto.condition="LESS"
        after_block_date_prototype=prot.filter(dto) if not block_period is None else prot
        stocks_prot=prototype_report(stocks)
        dto.field_name="storage.id"
        dto.value=self.storage.id
        dto.condition="EQUALS"
        #Фильтруем транзакции и остатки по складу
        storage_prototype=prototype_report.filter(after_block_date_prototype,dto)
        stocks_storage_prot=stocks_prot.filter(dto)
        dto.field_name="date"
        dto.value=self.end_date
        dto.condition="MORE"
        end_prototype=prototype_report.filter(storage_prototype,dto)
        for item in self.osv_items:
            dto.field_name="nomenclature.name"
            dto.value=item.nomenclature.name
            dto.condition="EQUALS"
            #Фильтруем транзакции и остатки по номенклатуре
            nom_prototype=prototype_report.filter(end_prototype,dto)
            stocks_nom_prot=stocks_storage_prot.filter(dto)
            #Учет остатков
            if len(stocks_nom_prot.data)==1:
                item.start_num=stocks_nom_prot.data[0].num
                item.end_num=stocks_nom_prot.data[0].num
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
    def filters_osv(filters:list, transactions, nomenclatures, block_period=None,  stocks=[]):
        osv=osv_model()
        osv.fill_empty_osv(nomenclatures)
        start_date_filter=None
        end_date_filter=None
        storage_filter=None
        for filter in filters:
            if "date" in filter.field_name:
                if end_date_filter is None:
                    end_date_filter=filter
                elif end_date_filter.value<filter.value:
                    end_date_filter=filter
                if start_date_filter is None:
                    if not end_date_filter is filter:
                        start_date_filter=filter
                elif start_date_filter.value>filter.value:
                    start_date_filter=filter
            if "storage.id" == filter.field_name:
                storage_filter=filter
        prot=prototype_report(transactions)
        dto=filter_dto()
        dto.field_name="date"
        dto.value=block_period
        dto.condition="LESS"
        #Фильтрация остатков по складу
        stocks_prot=prototype_report(stocks)
        stocks_storage_prot = stocks_prot.filter(storage_filter)
        #Фильтруем транзакции после даты блокировки
        after_block_date_prototype=prot.filter(dto) if not block_period is None else prot
        storage_prototype=after_block_date_prototype.filter(storage_filter) if not storage_filter is None else after_block_date_prototype
        start_prototype=storage_prototype.filter(start_date_filter) if not start_date_filter is None else prototype_report([])
        end_prototype=storage_prototype.filter(end_date_filter) if not end_date_filter is None else storage_filter
        for item in osv.osv_items:
            dto.field_name="nomenclature.name"
            dto.value=item.nomenclature.name
            dto.condition="EQUALS"
            nom_prototype=start_prototype.filter(dto)
            stocks_nom_prot=stocks_storage_prot.filter(dto)
            if len(stocks_nom_prot.data)==1:
                item.start_num=stocks_nom_prot.data[0].num
                item.end_num=stocks_nom_prot.data[0].num
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
            nom_prototype=end_prototype.filter(dto)
            for transaction in nom_prototype.data:
                if transaction in start_prototype.data:
                    continue
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
        
    
