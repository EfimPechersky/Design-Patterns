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
app = connexion.FlaskApp(__name__)
service=start_service()
fe = factory_entities()

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"

@app.app.route("/info/<type>/<format>", methods=['GET'])
def show_info(type, format):
    rf=fe.create(format)
    instance = rf()
    if not type in service.repository.data:
        return flask.Response(response="Неправильный тип "+type, status=400, 
               content_type="text/plain;charset=utf-8")
    
    ct={"json":"application/json",
        "xml":"text/xml",
        "csv":"text/plain",
        "md":"text/plain"}

    return flask.Response(response=instance.build(format,service.repository.data[type]), status=200, 
               content_type=ct[format]+";charset=utf-8")

@app.route("/info/<type>/<format>", methods=['POST'])
def handle_post_data(type, format):
    data = request.get_json()

    if data is None:
        return flask.Response(response="Отсутствует JSON!", status=400, 
                              content_type="text/plain;charset=utf-8")
    
    filters=data["filters"] if "filters" in data else None
    if filters is None:
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
    
    return flask.Response(response=instance.build(format,prot.data), status=200, 
               content_type=ct[format]+";charset=utf-8")

@app.app.route("/report", methods=['POST'])
def get_filtered_report():
    data = request.get_json()
    if data is None:
        return flask.Response(response="Отсутствует JSON!", status=400, 
                              content_type="text/plain;charset=utf-8")
    
    filters=data["filters"] if "filters" in data else None
    if filters is None:
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
    return flask.Response(response=csv().build("csv",osv.osv_items), status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/block_period", methods=['POST'])
def set_block_period():
    data = request.get_json()
    if data is None:
        return flask.Response(response="Отсутствует JSON!", status=400, 
                              content_type="text/plain;charset=utf-8")
    
    block_period=data["block_period"] if "block_period" in data else None
    if block_period is None:
        return flask.Response(response="Отсутствует дата блокировки!", status=400, 
                              content_type="text/plain;charset=utf-8")
    service.block_period=datetime.strptime(block_period,"%d-%m-%Y")
    return flask.Response(response="Дата блокировки успешно обновлена!", status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/default/<type>", methods=['GET'])
def default_info(type):
    rf=fe.create_default(sm.settings())
    instance = rf()
    if not type in service.repository.data:
        return flask.Response(response="Неправильный тип "+type, status=400, 
               content_type="text/plain;charset=utf-8")
    
    ct={"json":"application/json",
        "xml":"text/xml",
        "csv":"text/plain",
        "md":"text/plain"}

    return flask.Response(response=instance.build(sm.settings().response_format,service.repository.data[type]), status=200, 
               content_type=ct[sm.settings().response_format]+";charset=utf-8")

@app.app.route("/GetReceipts", methods=['GET'])
def get_receipts():
    rf=fe.create('json')
    instance = rf()

    return flask.Response(response=instance.build("json",service.repository.data[repository.receipt_key()]), status=200, 
               content_type="application/json;charset=utf-8")

@app.app.route("/GetReceipt/<code>", methods=['GET'])
def get_receipt(code):
    rf=fe.create('json')
    instance = rf()
    res=service.repository.data[repository.receipt_key()]
    receipt=None
    for i in res:
        if i.id==code:
            receipt=i
    if receipt is None:
        return flask.Response(response="Неправильный код рецепта!", status=400, 
               content_type="text/plain;charset=utf-8")
    return flask.Response(response=instance.build("json",receipt), status=200, 
               content_type="application/json;charset=utf-8")

@app.app.route("/report/<code>/<start>/<end>", methods=['GET'])
def get_report(code,start,end):
    rf=fe.create('json')
    instance = rf()
    res=service.repository.data[repository.storage_key()]
    storage=None
    try:
        start_date=datetime.strptime(start,"%d-%m-%Y")
        end_date=datetime.strptime(end,"%d-%m-%Y")
    except:
        return flask.Response(response="Неправильный формат дат!", status=400, 
               content_type="text/plain;charset=utf-8")
    for i in res:
        if i.id==code:
            storage=i
    if storage is None:
        return flask.Response(response="Неправильный код склада!", status=400, 
               content_type="text/plain;charset=utf-8")
    osv=service.create_osv(start_date,end_date,storage.id)
    csv=factory_entities().create("csv")
    return flask.Response(response=csv().build("csv",osv.osv_items), status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/dump", methods=['POST'])
def dump():
    res=service.dump("newsettings.json")
    if res:
        return flask.Response(response="Info saved to file!", status=200, 
               content_type="text/plain;charset=utf-8")
    else:
        return flask.Response(response="Error with saving info!", status=400, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/stocks", methods=['GET'])
def get_stocks():
    res=service.repository.data[repository.stock_key()]
    csv=factory_entities().create("csv")
    return flask.Response(response=csv().build("csv",res), status=200, 
               content_type="text/plain;charset=utf-8")

@app.app.route("/block_period", methods=['GET'])
def get_block_period():
    block=service.block_period
    if block==None:
        res="Дата блокировки отсутствует"
    else:
        res=f"Дата блокировки равна {datetime_convertor.convert(block)}"
    return flask.Response(response=res, status=200, 
               content_type="text/plain;charset=utf-8")

if __name__ == '__main__':
    service.start(file=True)
    sm=settings_manager()
    sm.file_name=".\settings.json"
    sm.load()
    service.block_period=sm.settings().block_period
    app.run(host="0.0.0.0", port = 8000)
