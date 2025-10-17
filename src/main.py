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
    keys = {
        "ranges":repository.range_key,
        "groups":repository.group_key,
        "nomenclatures":repository.nomenclature_key,
        "receipts":repository.receipt_key,
            }
    if not type in keys:
        return "Неправильный тип данных"
    
    ct={"json":"application/json",
        "xml":"text/xml",
        "csv":"text/plain",
        "md":"text/plain"}

    return flask.Response(response=instance.build(format,service.repository.data[keys[type]]), status=200, 
               content_type=ct[format]+";charset=utf-8")

@app.app.route("/default/<type>", methods=['GET'])
def default_info(type):
    rf=fe.create_default("D:\Design-Patterns\Design-Patterns\Src\settings.json")
    format="csv"
    if isinstance(rf,response_xml):
        format="xml"
    elif isinstance(rf,response_json):
        format="json"
    elif isinstance(rf,response_md):
        format="md"
    instance = rf()
    keys = {
        "ranges":repository.range_key,
        "groups":repository.group_key,
        "nomenclatures":repository.nomenclature_key,
        "receipts":repository.receipt_key,
            }
    if not type in keys:
        return "Неправильный тип данных"
    
    ct={"json":"application/json",
        "xml":"text/xml",
        "csv":"text/plain",
        "md":"text/plain"}

    return flask.Response(response=instance.build(format,service.repository.data[keys[type]]), status=200, 
               content_type=ct[format]+";charset=utf-8")

if __name__ == '__main__':
    service.start()
    app.run(host="0.0.0.0", port = 8000)
