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
#Сервис для создания, удаления и изменения объектов
class reference_service(abstract_logic):

    def __init__(self):
        super().__init__()
        self.service=start_service()
        # Подключение в наблюдение
        observe_service.add(self)

    #Добавить объект
    def add_reference(self,params):
        reference_type=params["reference_type"] if "reference_type" in params else None
        reference=params["reference"] if "reference" in params else None
        if not reference_type in repository.keys():
            raise argument_exception(f"Неизвестный тип {reference_type}!")
        result=self.service.add_reference(reference_type, reference)
        if result and reference_type==repository.transaction_key():
            self.service.create_stocks()
        return result
    #Изменить объект
    def change_reference(self,params):
        reference_type=params["reference_type"] if "reference_type" in params else None
        reference=params["reference"] if "reference" in params else None
        if not reference_type in repository.keys():
            raise argument_exception(f"Неизвестный тип {reference_type}!")
        result=self.service.change_reference(reference_type, reference)
        if result and reference_type==repository.transaction_key():
            self.service.create_stocks()
        return result
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
        stocks=prototype_report(self.service.data[repository.stock_key()])
        stocks_with_nom=stocks.filter(dto).data
        if len(stocks_with_nom)>0:
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

    #Удаление объекта
    def delete_reference(self,params):
        reference_type=params["reference_type"] if "reference_type" in params else None
        reference_id=params["reference_id"] if "reference_id" in params else None
        validator.validate(reference_type, str)
        validator.validate(reference_id, str)
        if reference_type not in self.service.data.keys():
            raise argument_exception(f"Неизвестный тип {reference_type}!")
        dto=filter_dto()
        dto.field_name="id"
        dto.value=reference_id
        dto.condition="EQUALS"
        references=prototype_report(self.service.data[reference_type])
        found_reference=references.filter(dto).data
        if len(found_reference)==0:
            raise argument_exception(f"Объект типа {reference_type} не был обнаружен по id {reference_id}!")
        if reference_type==repository.nomenclature_key() and self.check_nomenclatures(found_reference[0]): 
            return False
        if reference_type==repository.range_key() and self.check_ranges(found_reference[0]): 
            return False 
        if reference_type==repository.group_key() and self.check_groups(found_reference[0]): 
            return False
        if reference_type== repository.storage_key() and self.check_storages(found_reference[0]): 
            return False
        self.service.data[reference_type].remove(found_reference[0])
        if reference_type==repository.transaction_key():
            self.service.create_stocks()
        return True



    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)
        if event == event_type.add_new_reference():
            return self.add_reference(params)
        elif event == event_type.delete_reference():
            return self.delete_reference(params)
        elif event==event_type.change_reference():
            return self.change_reference(params)
