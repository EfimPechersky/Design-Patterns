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
from datetime import datetime
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

@app.app.route("/default/<type>", methods=['GET'])
def default_info(type):
    sm=settings_manager()
    sm.file_name=".\settings.json"
    sm.load()
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


if __name__ == '__main__':
    service.start(file=True)
    app.run(host="0.0.0.0", port = 8000)
