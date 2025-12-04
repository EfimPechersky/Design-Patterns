import connexion
from flask import request
import flask
from Logics.factory_entities import factory_entities
from Logics.response_csv import response_csv
from Logics.response_xml import response_xml
from Logics.response_json import response_json
from Logics.response_md import response_md
from Core.start_service import start_service
from Core.repository import repository
from Models.settings_manager import settings_manager
from Dto.filter_dto import filter_dto
from Logics.prototype_report import prototype_report
from datetime import datetime
from Convert.datetime_convertor import datetime_convertor
from Core.reference_service import reference_service
from Core.observe_service import observe_service
from Core.event_type import event_type
from Core.reference_postprocessor import reference_postprocessor
from Core.stock_postprocessor import stock_postprocessor
from Core.settings_postprocessor import settings_postprocessor
from Core.logger import logger
app = connexion.FlaskApp(__name__)
service=start_service()
fe = factory_entities()
refservice=reference_service()
ref=reference_postprocessor()
stp=stock_postprocessor()
sep=settings_postprocessor()
log = logger()
"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"

@app.app.route("/info/<type>/<format>", methods=['GET'])
def show_info(type, format):
    observe_service.create_event(event_type.info(), "Got request to show info about reference")
    rf=fe.create(format)
    instance = rf()
    if not type in service.repository.data:
        observe_service.create_event(event_type.error(), f"Wrong type {type}")
        return flask.Response(response="Неправильный тип "+type, status=400, 
               content_type="text/plain;charset=utf-8")
    
    ct={"json":"application/json",
        "xml":"text/xml",
        "csv":"text/plain",
        "md":"text/plain"}
    observe_service.create_event(event_type.debug(), f"Succesfully showed info about reference")
    return flask.Response(response=instance.build(format,service.repository.data[type]), status=200, 
               content_type=ct[format]+";charset=utf-8")

@app.route("/info/<type>/<format>", methods=['POST'])
def handle_post_data(type, format):
    observe_service.create_event(event_type.info(), "Got request to send info with filters")
    data = request.get_json()
    if data is None:
        observe_service.create_event(event_type.error(), "JSON data is missing!")
        return flask.Response(response="Отсутствует JSON!", status=400, 
                              content_type="text/plain;charset=utf-8")
    
    filters=data["filters"] if "filters" in data else None
    if filters is None:
        observe_service.create_event(event_type.error(), "Filters is missing!")
        return flask.Response(response="Отсутствуют фильтры!", status=400, 
                              content_type="text/plain;charset=utf-8")

    dtos=[]
    for filter in filters:
        dto=filter_dto()
        dto.field_name=filter["field_name"]
        dto.value=filter["value"]
        if dto.value.isdigit():
            dto.value=float(dto.value)
        dto.condition=filter["condition"]
        dtos.append(dto)
    
    rf=fe.create(format)
    instance = rf()
    if not type in service.repository.data:
        observe_service.create_event(event_type.error(), f"Wrong type {type}")
        return flask.Response(response="Неправильный тип "+type, status=400, 
               content_type="text/plain;charset=utf-8")
    
    ct={"json":"application/json",
        "xml":"text/xml",
        "csv":"text/plain",
        "md":"text/plain"}
    data = service.repository.data[type]
    prot = prototype_report(data)
    for filter in dtos:
        prot=prot.filter(filter)
    observe_service.create_event(event_type.debug(), f"Succesfully sended filtered data!")
    return flask.Response(response=instance.build(format,prot.data), status=200, 
               content_type=ct[format]+";charset=utf-8")

@app.app.route("/report", methods=['POST'])
def get_filtered_report():
    observe_service.create_event(event_type.info(), f"Got request to send filtered OSV!")
    data = request.get_json()
    if data is None:
        observe_service.create_event(event_type.error(), "JSON data is missing!")
        return flask.Response(response="Отсутствует JSON!", status=400, 
                              content_type="text/plain;charset=utf-8")
    
    filters=data["filters"] if "filters" in data else None
    if filters is None:
        observe_service.create_event(event_type.error(), "Filters is missing!")
        return flask.Response(response="Отсутствуют фильтры!", status=400, 
                              content_type="text/plain;charset=utf-8")
    dtos=[]
    for filter in filters:
        dto=filter_dto()
        dto.field_name=filter["field_name"]
        if "date" in dto.field_name:
            dto.value=datetime.strptime(filter["value"],"%d-%m-%Y")
        else:
            dto.value=filter["value"]
        dto.condition=filter["condition"]
        dtos+=[dto]
    
    osv=service.create_osv_with_filters(dtos)
    csv=factory_entities().create("csv")
    observe_service.create_event(event_type.debug(), f"Succesfully sended filtered OSV!")
    return flask.Response(response=csv().build("csv",osv.osv_items), status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/block_period", methods=['POST'])
def set_block_period():
    observe_service.create_event(event_type.info(), f"Got request to change block period!")
    data = request.get_json()
    if data is None:
        observe_service.create_event(event_type.error(), "JSON data is missing!")
        return flask.Response(response="Отсутствует JSON!", status=400, 
                              content_type="text/plain;charset=utf-8")
    
    block_period=data["block_period"] if "block_period" in data else None
    if block_period is None:
        observe_service.create_event(event_type.error(), "Block period is missing!")
        return flask.Response(response="Отсутствует дата блокировки!", status=400, 
                              content_type="text/plain;charset=utf-8")
    service.block_period=datetime.strptime(block_period,"%d-%m-%Y")
    observe_service.create_event(event_type.debug(), f"Succesfully changed block period!")
    return flask.Response(response="Дата блокировки успешно обновлена!", status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/default/<type>", methods=['GET'])
def default_info(type):
    observe_service.create_event(event_type.info(), f"Got request to send info in default format!")
    rf=fe.create_default(sm.settings())
    instance = rf()
    if not type in service.repository.data:
        observe_service.create_event(event_type.error(), f"Wrong type {type}")
        return flask.Response(response="Неправильный тип "+type, status=400, 
               content_type="text/plain;charset=utf-8")
    
    ct={"json":"application/json",
        "xml":"text/xml",
        "csv":"text/plain",
        "md":"text/plain"}
    observe_service.create_event(event_type.debug(), f"Succesfully sended info in default format!")
    return flask.Response(response=instance.build(sm.settings().response_format,service.repository.data[type]), status=200, 
               content_type=ct[sm.settings().response_format]+";charset=utf-8")

@app.app.route("/GetReceipts", methods=['GET'])
def get_receipts():
    observe_service.create_event(event_type.info(), f"Got request to get list of receipts")
    rf=fe.create('json')
    instance = rf()
    observe_service.create_event(event_type.debug(), f"Succesfully sended info about receipts!")
    return flask.Response(response=instance.build("json",service.repository.data[repository.receipt_key()]), status=200, 
               content_type="application/json;charset=utf-8")

@app.app.route("/GetReceipt/<code>", methods=['GET'])
def get_receipt(code):
    observe_service.create_event(event_type.info(), f"Got request to get receipt by id")
    rf=fe.create('json')
    instance = rf()
    res=service.repository.data[repository.receipt_key()]
    receipt=None
    for i in res:
        if i.id==code:
            receipt=i
    if receipt is None:
        observe_service.create_event(event_type.error(), f"Wrong id {code}!")
        return flask.Response(response="Неправильный код рецепта!", status=400, 
               content_type="text/plain;charset=utf-8")
    observe_service.create_event(event_type.debug(), f"Succesfully sended receipt with id {code}!")
    return flask.Response(response=instance.build("json",receipt), status=200, 
               content_type="application/json;charset=utf-8")

@app.app.route("/report/<code>/<start>/<end>", methods=['GET'])
def get_report(code,start,end):
    observe_service.create_event(event_type.info(), f"Got request to get OSV")
    rf=fe.create('json')
    res=service.repository.data[repository.storage_key()]
    storage=None
    try:
        start_date=datetime.strptime(start,"%d-%m-%Y")
        end_date=datetime.strptime(end,"%d-%m-%Y")
    except:
        observe_service.create_event(event_type.error(), f"Wrong date format!")
        return flask.Response(response="Неправильный формат дат!", status=400, 
               content_type="text/plain;charset=utf-8")
    for i in res:
        if i.id==code:
            storage=i
    if storage is None:
        observe_service.create_event(event_type.error(), f"Wrong storage id!")
        return flask.Response(response="Неправильный код склада!", status=400, 
               content_type="text/plain;charset=utf-8")
    osv=service.create_osv(start_date,end_date,storage.id)
    csv=factory_entities().create("csv")
    observe_service.create_event(event_type.debug(), f"Succesfully sended OSV!")
    return flask.Response(response=csv().build("csv",osv.osv_items), status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/dump", methods=['POST'])
def dump():
    observe_service.create_event(event_type.info(), f"Got request to dump info to file")
    res=stp.dump("newsettings.json")
    if res:
        observe_service.create_event(event_type.debug(), f"Info saved to file!")
        return flask.Response(response="Info saved to file!", status=200, 
               content_type="text/plain;charset=utf-8")
    else:
        observe_service.create_event(event_type.error(), f"Error with saving info!")
        return flask.Response(response="Error with saving info!", status=400, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/stocks", methods=['GET'])
def get_stocks():
    observe_service.create_event(event_type.info(), f"Got request to get stocks")
    res=service.repository.data[repository.stock_key()]
    csv=factory_entities().create("csv")
    observe_service.create_event(event_type.debug(), f"Succesfully sended stocks!")
    return flask.Response(response=csv().build("csv",res), status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/block_period", methods=['GET'])
def get_block_period():
    observe_service.create_event(event_type.info(), f"Got request to change block period")
    block=service.block_period
    if block==None:
        observe_service.create_event(event_type.error(), f"Block period is missing!")
        res="Дата блокировки отсутствует"
    else:
        res=f"Дата блокировки равна {datetime_convertor.convert(block)}"
    observe_service.create_event(event_type.debug(), f"Block period changed!")
    return flask.Response(response=res, status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/api/<reference_type>", methods=['GET'])
def get_reference(reference_type):
    observe_service.create_event(event_type.info(), f"Got request to get reference")
    data = request.get_json()
    id=data["id"]
    filter=filter_dto()
    filter.field_name="id"
    filter.value=id
    filter.condition="EQUALS"
    if reference_type not in repository.keys():
        observe_service.create_event(event_type.error(), f"Wrong type {reference_type}")
        return flask.Response(response=f"Неверный тип объекта", status=400, 
               content_type="text/plain;charset=utf-8")
    prot=prototype_report(service.data[reference_type])
    references=prot.filter(filter).data
    if len(references)==0:
        observe_service.create_event(event_type.error(), f"Reference with id {id} not found!")
        return flask.Response(response=f"Не найдено ни одного объекта с id {id}", status=400, 
               content_type="text/plain;charset=utf-8")
    json=factory_entities().create("json")
    observe_service.create_event(event_type.debug(), f"Succesfully sended reference!")
    return flask.Response(response=json().build("json",references), status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/api/<reference_type>", methods=['PUT'])
def add_reference(reference_type):
    observe_service.create_event(event_type.info(), f"Got request to add new reference")
    data = request.get_json()
    if reference_type not in repository.keys():
        observe_service.create_event(event_type.error(), f"Wrong type {reference_type}")
        return flask.Response(response=f"Неверный тип объекта", status=400, 
               content_type="text/plain;charset=utf-8")
    res=refservice.add_reference(reference_type,data)
    if res:
        observe_service.create_event(event_type.debug(), f"Succesfully added new reference!")
        return flask.Response(response="Успешно добавлен новый объект!", status=200, 
               content_type="text/plain;charset=utf-8")
    observe_service.create_event(event_type.error(), f"Error with adding new reference!")
    return flask.Response(response="Возникла ошибка с добавлением объекта!", status=400, 
            content_type="text/plain;charset=utf-8")

@app.app.route("/api/<reference_type>", methods=['DELETE'])
def delete_reference(reference_type):
    observe_service.create_event(event_type.info(), f"Got request to delete reference")
    data = request.get_json()
    reference_id=data["id"]
    if reference_type not in repository.keys():
        observe_service.create_event(event_type.error(), f"Wrong type {reference_type}")
        return flask.Response(response=f"Неверный тип объекта", status=400, 
               content_type="text/plain;charset=utf-8")
    res=refservice.delete_reference(reference_type,reference_id)
    if res:
        observe_service.create_event(event_type.debug(), f"Succesfully deleted reference!")
        return flask.Response(response="Успешно удален объект!", status=200, 
               content_type="text/plain;charset=utf-8")
    observe_service.create_event(event_type.error(), f"Error with deleting reference!")
    return flask.Response(response="Возникла ошибка с удалением объекта!", status=400, 
            content_type="text/plain;charset=utf-8")

@app.app.route("/api/<reference_type>", methods=['PATCH'])
def change_reference(reference_type):
    observe_service.create_event(event_type.info(), f"Got request to change reference")
    data = request.get_json()
    if reference_type not in repository.keys():
        observe_service.create_event(event_type.error(), f"Wrong type {reference_type}")
        return flask.Response(response=f"Неверный тип объекта", status=400, 
               content_type="text/plain;charset=utf-8")
    res=refservice.change_reference(reference_type,data)
    if res:
        observe_service.create_event(event_type.debug(), f"Succesfully changed reference!")
        return flask.Response(response="Успешно изменен объект!", status=200, 
               content_type="text/plain;charset=utf-8")
    observe_service.create_event(event_type.error(), f"Error with changing reference!")
    return flask.Response(response="Возникла ошибка с изменением объекта!", status=400, 
            content_type="text/plain;charset=utf-8")

if __name__ == '__main__':
    service.start(file=True)
    sm=settings_manager()
    sm.file_name=".\settings.json"
    sm.load()
    service.block_period=sm.settings().block_period
    app.run(host="0.0.0.0", port = 8000)
