from Core.abstract_logic import abstract_logic
from Core.observe_service import observe_service
from Core.event_type import event_type
from Core.start_service import start_service
from Core.validator import validator,argument_exception
from Logics.prototype_report import prototype_report
from Dto.filter_dto import filter_dto
from Core.repository import repository
from Models.nomenclature_model import nomenclature_model
from Models.storage_model import storage_model
from Models.range_model import range_model
from Models.group_model import nomenclature_group_model
from Models.stock_model import stock_model
from datetime import datetime
#Постобработчик для перерасчёта остатков
class stock_postprocessor(abstract_logic):

    def __init__(self):
        super().__init__()
        self.service=start_service()
        observe_service.add(self)

    #Создание остатков
    def create_stocks(self):
        self.service.data[repository.stock_key()].clear()
        prot=prototype_report(self.service.data[repository.transaction_key()])
        dto=filter_dto()
        #Берем все транзакции до даты блокировки
        dto.field_name="date"
        dto.value=self.service.block_period
        dto.condition="MORE"
        before_block_date_prot=prot.filter(dto)
        #Берем все транзакции до даты блокировки после 01-01-1990
        dto.field_name="date"
        dto.value=datetime.strptime("01-01-1990", "%d-%m-%Y")
        dto.condition="LESS"
        block_period_prot=before_block_date_prot.filter(dto)
        #Создаем остатки номенклатуры отдельно для каждого склада
        for storage in self.service.data[repository.storage_key()]:
            dto.field_name="storage.id"
            dto.value=storage.id
            dto.condition="EQUALS"
            stor_prot=block_period_prot.filter(dto)
            for nomenclature in self.service.data[repository.nomenclature_key()]:
                dto.field_name="nomenclature.id"
                dto.value=nomenclature.id
                dto.condition="EQUALS"
                nom_prot=stor_prot.filter(dto)
                range=nomenclature.range_count
                if not range.base_range is None:
                    range=range.base_range
                stock=stock_model.create(nomenclature, range, storage, 0.0)
                for transaction in nom_prot.data:
                    num=transaction.num
                    if transaction.range!=range:
                        num*=transaction.range.coeff
                    stock.num=stock.num+num
                self.service.data[repository.stock_key()].append(stock)

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  
        if event in [event_type.change_block_period(), event_type.deleted_reference(),event_type.add_new_reference(),event_type.change_reference()]:
            self.create_stocks()