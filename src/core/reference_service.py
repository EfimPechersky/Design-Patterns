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
from Core.reference_postprocessor import reference_postprocessor
#Сервис для создания, удаления и изменения объектов
class reference_service():


    def __init__(self):
        self.service=start_service()

    #Добавить объект
    def add_reference(self,reference_type, reference):
        if not reference_type in repository.keys():
            raise argument_exception(f"Неизвестный тип {reference_type}!")
        reference_dto=start_service.get_model_by_type(reference_type)[0]
        dto=reference_dto().create(reference)
        result=self.service.add_reference(reference_type, reference)
        observe_service.create_event(event_type.add_new_reference(),dto)
        return result
    
    #Изменить объект
    def change_reference(self,reference_type, reference):
        if not reference_type in repository.keys():
            raise argument_exception(f"Неизвестный тип {reference_type}!")
        result=self.service.change_reference(reference_type, reference)
        reference_dto=start_service.get_model_by_type(reference_type)[0]
        dto=reference_dto().create(reference)
        observe_service.create_event(event_type.change_reference(),dto)
        return result

    #Удаление объекта
    def delete_reference(self,reference_type, reference_id):
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
        observe_service.create_event(event_type.deleting_reference(),found_reference[0].to_dto())
        self.service.data[reference_type].remove(found_reference[0])
        observe_service.create_event(event_type.deleted_reference(), found_reference[0].to_dto())
        return True
        
