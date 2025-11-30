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
#Постобработчик для предотвращения удаления объекта
class reference_postprocessor(abstract_logic):

    def __init__(self):
        super().__init__()
        self.service=start_service()
        observe_service.add(self)
    #Проверить наличие номенклатуры в других объектах
    def check_nomenclatures(self, nomenclature):
        validator.validate(nomenclature, nomenclature_model)
        dto=filter_dto()
        dto.field_name="nomenclature.id"
        dto.value=nomenclature.id
        dto.condition="EQUALS"
        for receipt in self.service.data[repository.receipt_key()]:
            ingridients=prototype_report(receipt.ingridients)
            ingridients_with_nom=ingridients.filter(dto).data
            if len(ingridients_with_nom)>0:
                return True
        transactions=prototype_report(self.service.data[repository.transaction_key()])
        transactions_with_nom=transactions.filter(dto).data
        if len(transactions_with_nom)>0:
            return True
        return False
    #Проверить наличие склада в других объектах
    def check_storages(self, storage):
        validator.validate(storage, storage_model)
        dto=filter_dto()
        dto.field_name="storage.id"
        dto.value=storage.id
        dto.condition="EQUALS"
        transactions=prototype_report(self.service.data[repository.transaction_key()])
        transactions_with_storage=transactions.filter(dto).data
        if len(transactions_with_storage)>0:
            return True
        stocks=prototype_report(self.service.data[repository.stock_key()])
        stocks_with_storage=stocks.filter(dto).data
        if len(stocks_with_storage)>0:
            return True
        return False
    #Проверить наличие единицы измерения в других объектах
    def check_ranges(self,range):
        validator.validate(range, range_model)
        dto=filter_dto()
        dto.field_name="range_count.id"
        dto.value=range.id
        dto.condition="EQUALS"
        noms=prototype_report(self.service.data[repository.nomenclature_key()])
        noms_with_range=noms.filter(dto).data
        if len(noms_with_range)>0:
            return True
        dto.field_name="base_range.id"
        dto.value=range.id
        dto.condition="EQUALS"
        ranges=prototype_report(self.service.data[repository.stock_key()])
        ranges_with_base_range=ranges.filter(dto).data
        if len(ranges_with_base_range)>0:
            return True
        return False
    
    #Проверить наличие группы в других объектах
    def check_groups(self,group):
        validator.validate(group, nomenclature_group_model)
        dto=filter_dto()
        dto.field_name="group.id"
        dto.value=group.id
        dto.condition="EQUALS"
        noms=prototype_report(self.service.data[repository.nomenclature_key()])
        noms_with_group=noms.filter(dto).data
        if len(noms_with_group)>0:
            return True
        return False

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)
        if event == event_type.deleting_reference():
            reference_type=params["reference_type"]
            reference=params["reference"]
            if reference_type=="nomenclatures":
                if self.check_nomenclatures(reference):
                    raise Exception("Номенклатура используется в других объектах")
            elif reference_type=="ranges":
                if self.check_ranges(reference):
                    raise Exception("Единица измерения используется в других объектах")
            elif reference_type=="storages":
                if self.check_storages(reference):
                    raise Exception("Склад используется в других объектах")
            elif reference_type=="groups":
                if self.check_groups(reference):
                    raise Exception("Группа номенклатуры используется в других объектах")
