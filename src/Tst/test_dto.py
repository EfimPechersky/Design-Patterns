from Core.start_service import start_service
from Models.range_model import range_model
from Models.group_model import nomenclature_group_model
from Models.nomenclature_model import nomenclature_model
from Models.receipt_model import receipt_model
from Models.ingridient_model import ingridient_model
from Core.repository import repository
from Core.validator import validator,argument_exception,operation_exception
from contextlib import nullcontext as does_not_raise
from Dto.receipt_dto import receipt_dto
from Dto.range_dto import range_dto
from Dto.group_dto import group_dto
from Dto.nomenclature_dto import nomenclature_dto
from Dto.ingridient_dto import ingridient_dto
import pytest
#Тестирование Dto
class TestDto:
    #Тестирование создания Dto
    @pytest.mark.parametrize("dto_type, data, name, result", [
        (range_dto,{"name":"грамм","id":"adb7510f-687d-428f-a697-26e53d3f65b7","base_id":None,"coeff":1.0},"грамм", does_not_raise()),
        (range_dto,1,"грамм",pytest.raises(argument_exception)),
        (group_dto,{"name":"Молочные продукты","id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918"},"Молочные продукты", does_not_raise()),
        (group_dto,1,"Молочные продукты", pytest.raises(argument_exception)),
        (nomenclature_dto,{"name":"Пшеничная мука","range_id":"a33dd457-36a8-4de6-b5f1-40afa6193346","group_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8920","id":"0c101a7e-5934-4155-83a6-d2c388fcc11a"},"Пшеничная мука", does_not_raise()),
        (nomenclature_dto,1,"Пшеничная мука", pytest.raises(argument_exception)),
        (ingridient_dto,{"nomenclature_id":"0c101a7e-5934-4155-83a6-d2c388fcc11a","range_id":"adb7510f-687d-428f-a697-26e53d3f65b7","value":100.0},"", does_not_raise()),
        (ingridient_dto,1,"", pytest.raises(argument_exception)),
        (receipt_dto,{"name":"Вафли", "ingridients":[
            {
                "nomenclature_id":"0c101a7e-5934-4155-83a6-d2c388fcc11a",
                "range_id":"adb7510f-687d-428f-a697-26e53d3f65b7",
                "value":100.0
            },
            {
                "nomenclature_id":"39d9349d-28fa-4c7b-ad92-5c5fc7cf93da",
                "range_id":"adb7510f-687d-428f-a697-26e53d3f65b7",
                "value":80.0
            }], 'steps':["step1",'step2']},"Вафли", does_not_raise()),
        (receipt_dto,1,"Вафли", pytest.raises(argument_exception)),
    ])
    def test_dto_creation(self,dto_type, data, name, result):
        with result:
            dto = dto_type().create(data)
            assert dto.name==name
    