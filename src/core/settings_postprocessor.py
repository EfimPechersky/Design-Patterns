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
from Convert.convert_factory import convert_factory
import json
#Постобработчик для записи изменений в файл
class settings_postprocessor(abstract_logic):

    def __init__(self):
        super().__init__()
        self.service=start_service()
        observe_service.add(self)

    """
    Выгрузка данных
    """
    def dump(self, filename):
        try:
            alldata={}
            cf=convert_factory()
            for k in repository.keys():
                alldata[k]=[]
                for i in self.service.data[k]:
                    alldata[k]+=[cf.rec_convert(i)]
            with open(filename, 'w', encoding="UTF-8") as file_instance:
                json.dump(alldata,file_instance,ensure_ascii=False,indent=4)
            return True
        except Exception as e:
            error_message = str(e)
            return False

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  
        if event in [event_type.change_block_period(), event_type.deleted_reference(),event_type.add_new_reference(),event_type.change_reference()]:
            self.dump("appsettings.json")