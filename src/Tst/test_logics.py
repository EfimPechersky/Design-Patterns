import pytest
import json
import csv
import xml.etree.ElementTree as ET
from Models.group_model import nomenclature_group_model
from Models.range_model import range_model
from Models.abstract_model import abstract_model
from Logics.factory_entities import factory_entities
from Logics.response_csv import response_csv
from Logics.response_json import response_json
from Core.response_format import response_formats
from Core.validator import validator
from Core.abstract_response import abstract_response
from contextlib import nullcontext as does_not_raise

# Тесты для проверки логики 
class TestLogics:

    # Проверим формирование CSV
    def test_notNone_response_csv_build(self):
        # Подготовка
        response = response_csv()
        data = []
        entity = nomenclature_group_model()
        entity.name="test"
        data.append( entity )

        # Дейстие
        result = response.build( "csv", data)

        # Проверка
        assert result is not None
    
    # Проверим формирование XML
    def test_notNone_response_xml_build(self):
        # Подготовка
        response = response_csv()
        data = []
        entity = nomenclature_group_model()
        entity.name="test"
        data.append( entity )

        # Дейстие
        result = response.build( "xml", data)

        # Проверка
        assert result is not None
    
    # Проверим формирование Json
    def test_notNone_response_json_build(self):
        # Подготовка
        response = response_csv()
        data = []
        entity = nomenclature_group_model()
        entity.name="test"
        data.append( entity )

        # Дейстие
        result = response.build( "json", data)

        # Проверка
        assert result is not None
    
    # Проверим формирование Markdown
    def test_notNone_response_markdown_build(self):
        # Подготовка
        response = response_csv()
        data = []
        entity = nomenclature_group_model()
        entity.name="test"
        data.append( entity )

        # Дейстие
        result = response.build( "md", data)

        # Проверка
        assert result is not None

    #Проверка создания формата ответа
    def test_notNone_factory_create(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = nomenclature_group_model()
        entity.name="test"
        data.append( entity )

        # Действие
        logic = factory.create( response_formats.csv() )

        # Проверка
        assert logic is not None
        instance =  logic() # logic()
        validator.validate( instance,  response_csv)
        text = instance.build(response_formats.csv(), data)
        assert len(text) > 0 
    
    #Создание CSV файла
    def test_create_csv_file(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = range_model("test",1.0)
        second_entity = range_model("second_test",10.0,entity)
        data.append( entity )
        data.append( second_entity )

        # Действие
        logic = factory.create( response_formats.csv() )
        instance =  logic() # logic()
        text = instance.build(response_formats.csv(), data)
        with open("test_formats/test_file_csv.csv", 'w',encoding="UTF-8") as file:
            file.write(text)
        
        #Проверка
        with open("test_formats/test_file_csv.csv", 'r',encoding="UTF-8", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                assert row[0].count(";")==4
    
    #Создание XML файла
    def test_create_xml_file(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = range_model("test",1.0)
        second_entity = range_model("second_test",10.0,entity)
        data.append( entity )
        data.append( second_entity )

        # Действие
        logic = factory.create( response_formats.xml() )
        instance =  logic() # logic()
        text = instance.build(response_formats.xml(), data)
        with open("test_formats/test_file_xml.txt", 'w',encoding="UTF-8") as file:
            file.write(text)
        
        #Проверка
        with open("test_formats/test_file_xml.txt", 'r',encoding="UTF-8", newline='') as f:
            data = f.read()
            with does_not_raise():
                ET.fromstring(data)
    
    #Создание Json файла
    def test_create_json_file(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = range_model("test",1.0)
        second_entity = range_model("second_test",10.0,entity)
        data.append( entity )
        data.append( second_entity )

        # Действие
        logic = factory.create( response_formats.json() )
        instance =  logic() # logic()
        text = instance.build(response_formats.json(), data)
        with open("test_formats/test_file_json.json", 'w',encoding="UTF-8") as file:
            file.write(text)
        
        #Проверка
        with open("test_formats/test_file_json.json", 'r',encoding="UTF-8", newline='') as f:
            with does_not_raise():
                json.loads(f.read())

    #Создание Markdown файла
    def test_create_markdown_file(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = range_model("test",1.0)
        second_entity = range_model("second_test",10.0,entity)
        data.append( entity )
        data.append( second_entity )

        # Действие
        logic = factory.create( response_formats.md() )
        instance =  logic() # logic()
        text = instance.build(response_formats.md(), data)
        with open("test_formats/test_file_md.md", 'w',encoding="UTF-8") as file:
            file.write(text)
        
        #Проверка
        with open("test_formats/test_file_md.md", 'r',encoding="UTF-8", newline='') as f:
            for row in f.read().split("\n")[-1]:
                assert row[0].count("|")==5        
            