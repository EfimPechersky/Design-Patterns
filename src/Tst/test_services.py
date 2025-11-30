from Core.observe_service import observe_service
from Core.reference_service import reference_service
from Core.print_service import print_service
from Core.event_type import event_type
from Models.range_model import range_model
from Core.start_service import start_service
from Core.repository import repository
from Core.reference_postprocessor import reference_postprocessor
from Core.settings_postprocessor import settings_postprocessor
import pytest
#Тестирование reference service
class TestService:
    service=start_service()
    reference=reference_service()
    delete_processor=reference_postprocessor()
    #Тестирование добавления нового объекта
    def test_add_new_object(self):
        self.service.start(file=True)
        prev_len=len(self.service.data[repository.nomenclature_key()])
        nom={
            "name":"Лопата",
            "range_id":"f8346e8b-7260-4db8-a673-c8c826ab08b7",
            "group_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8920",
            "id":"12345678-5934-4155-83a6-d2c388fcc11a"
        }
        self.reference.add_reference("nomenclatures", nom)
        new_len=len(self.service.data[repository.nomenclature_key()])
        assert prev_len+1==new_len
    #Тестирование удаления номенклатуры
    def test_delete_nomenclature(self):
        self.service.start(file=True)
        prev_len=len(self.service.data[repository.nomenclature_key()])
        nom={
            "name":"Лопата",
            "range_id":"f8346e8b-7260-4db8-a673-c8c826ab08b7",
            "group_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8920",
            "id":"12345678-5934-4155-83a6-d2c388fcc11a"
        }
        self.reference.add_reference("nomenclatures", nom)
        new_len=len(self.service.data[repository.nomenclature_key()])
        assert prev_len+1==new_len
        self.reference.delete_reference("nomenclatures", nom["id"])
        prev_len=new_len
        new_len=len(self.service.data[repository.nomenclature_key()])
        assert prev_len-1==new_len
        with pytest.raises(Exception):
            self.reference.delete_reference("nomenclatures","0c101a7e-5934-4155-83a6-d2c388fcc11a")
    #Тестирование удаления единицы измерения
    def test_delete_range(self):
        self.service.start(file=True)
        prev_len=len(self.service.data[repository.range_key()])
        range={
            "name":"ватт",
            "base_id":None,
            "coeff":100.0,
            "id":"12345678-5934-4155-0000-d2c388fcc11a"
        }
        self.reference.add_reference("ranges", range)
        new_len=len(self.service.data[repository.range_key()])
        assert prev_len+1==new_len
        self.reference.delete_reference("ranges","12345678-5934-4155-0000-d2c388fcc11a")
        prev_len=new_len
        new_len=len(self.service.data[repository.range_key()])
        assert prev_len-1==new_len
        with pytest.raises(Exception):
            self.reference.delete_reference("ranges", "f5j1u457-3p98-4dy2-b5f1-40afa9793346")
    #Тестирование удаления группы
    def test_delete_group(self):
        self.service.start(file=True)
        prev_len=len(self.service.data[repository.group_key()])
        group={
            "name":"Группа продуктов",
            "id":"12345678-5934-4155-1111-d2c388fcc11a"
        }
        self.reference.add_reference("groups", group)
        new_len=len(self.service.data[repository.group_key()])
        assert prev_len+1==new_len
        self.reference.delete_reference("groups","12345678-5934-4155-1111-d2c388fcc11a")
        prev_len=new_len
        new_len=len(self.service.data[repository.group_key()])
        assert prev_len-1==new_len
        with pytest.raises(Exception):
            self.reference.delete_reference("groups","7f4ecdab-0f01-4216-8b72-4c91d22b8918")
    #Тестирование удаления склада
    def test_delete_storage(self):
        self.service.start(file=True)
        prev_len=len(self.service.data[repository.storage_key()])
        storage={
            "name":"Запасной склад",
            "id":"12345678-5934-4155-2222-d2c388fcc11a"
        }
        self.reference.add_reference("storages", storage)
        new_len=len(self.service.data[repository.storage_key()])
        assert prev_len+1==new_len
        self.reference.delete_reference("storages","12345678-5934-4155-2222-d2c388fcc11a")
        prev_len=new_len
        new_len=len(self.service.data[repository.storage_key()])
        assert prev_len-1==new_len
        with pytest.raises(Exception):
            self.reference.delete_reference("storages", "ndet5a2x-6f2a-nv5z-f561-md7vb421")
    #Тестирование изменения объекта
    def test_change_reference(self):
        self.service.start(file=True)
        group={
            "name":"Группа продуктов",
            "id":"7f4ecdab-0f01-4216-8b72-4c91d22b8920"
        }
        self.reference.change_reference("groups",group)
        assert self.service.data[repository.group_key()][2].name==self.service.data[repository.nomenclature_key()][0].group.name
    