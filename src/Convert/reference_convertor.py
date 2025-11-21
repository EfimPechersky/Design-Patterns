from .abstract_convertor import abstract_convertor
from Core.validator import validator, operation_exception
from Models.abstract_model import abstract_model
from Models.range_model import range_model
from Models.nomenclature_model import nomenclature_model
from Models.ingridient_model import ingridient_model
from Models.group_model import nomenclature_group_model
from Models.receipt_model import receipt_model
from Models.transaction_model import transaction_model
from Models.storage_model import storage_model
from Models.osv_item_model import osv_item_model
from Models.osv_model import osv_model
from Core.abstract_dto import abstract_dto
from Models.stock_model import stock_model
from Core.common import common
#Класс для преобразования объекта типа наследуюемого от abstract_model
class reference_convertor(abstract_convertor):
    #Список конвертируемых типов
    convertible_data:list=abstract_model.__subclasses__()+abstract_dto.__subclasses__()
    def convert(self, raw_data):
        dict={}
        data=super().convert(raw_data)
        dto=data
        if issubclass(type(data),abstract_model):
            dto=data.to_dto()
        fields = common.get_fields(dto)
        try:
            for field in fields:
                atr=getattr(dto, field)
                dict[field]=atr
        except:
            raise operation_exception("Невозможно преобразовать данные!")    

        return dict