from .abstract_model import abstract_model
from .nomenclature_model import nomenclature_model
from Core.validator import validator, operation_exception, argument_exception
import os
"""Класс, описывающий рецепты"""
class receipt_model(abstract_model):
    __ingridients:list=[]
    __steps:list=[]
    __receipt_storage={}

    def __init__(self):
        super().__init__()

    """Список ингридиентов"""
    @property
    def ingridients(self):
        return self.__ingridients
    
    """Валидация и присвоение списка ингридтиентов"""
    @ingridients.setter
    def ingridients(self, other):
        validator.validate(other,list)
        for i in other:
            validator.validate(i, tuple)
            validator.validate(i[0],nomenclature_model)
            validator.validate(i[1],float)
        self.__ingridients=other
    
    """Добавление ингридиента в список"""
    def add_new_proportion(self, nomenclature, number):
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(number, float)
        self.__ingridients+=[(nomenclature,number)]

    """Шаги пригтовления"""
    @property
    def steps(self):
        return self.__steps
    
    """Валидация и присвоение шагов приготовления"""
    @steps.setter
    def steps(self, other):
        validator.validate(other,list)
        for i in other:
            validator.validate(i,str)
        self.__steps=other
    
    """Добавление шага приготовления"""
    def add_step(self, step, number=-1):
        validator.validate(step,str)
        validator.validate(number, int)
        if number<-1 or number>len(self.steps):
            raise argument_exception("Номер шага рецепта неверен")
        if number != -1 and number<len(self.steps):
            self.steps = self.steps[:number] +[step] + self.steps[number:]
        else:
            self.steps+=[step]
    
    
    @staticmethod
    def create(name, ingridients, steps):
        """
        Создание нового рецепта
        Args:
            name (str): Имя рецепта
            ingridients (list): Список ингридиентов
            steps (list): Список шагов приготовления
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Неулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            receipt_model или Exception
        """
        rm = receipt_model()
        rm.name = name
        rm.ingridients = ingridients
        rm.steps = steps
        return rm
    
    """Создание рецепта вафель"""
    @staticmethod
    def create_waffles_receipt():
        name = "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ"

        products = []
        products+=[(nomenclature_model.create_butter(),70.0)]
        products+=[(nomenclature_model.create_sugar(),80.0)]
        products+=[(nomenclature_model.create_flour(),100.0)]
        products+=[(nomenclature_model.create_eggs(),1.0)]
        products+=[(nomenclature_model.create_vanilla(),5.0)]

        steps = [
        "Как испечь вафли хрустящие в вафельнице? Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.",
        "Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.",
        "Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.",
        "Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.",
        "Всыпьте муку, добавьте ванилин.",
        "Перемешайте массу венчиком до состояния гладкого однородного теста.",
        "Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно! Я не смазываю вафельницу маслом, в тесте достаточно жира, да и к ней уже давно ничего не прилипает. Но вы смотрите по своей модели. Выкладывайте тесто по столовой ложке. Можно класть немного меньше теста, тогда вафли будут меньше и их получится больше.",
        "Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик."
        ]
        return receipt_model.create(name, products, steps)
    
    """Создание рецепта пирога"""
    @staticmethod
    def create_pie_receipt():
        name = "ПИРОГ ЗЕБРА"

        products = []
        products+=[(nomenclature_model.create_butter(),150.0)]
        products+=[(nomenclature_model.create_sugar(),240.0)]
        products+=[(nomenclature_model.create_flour(),250.0)]
        products+=[(nomenclature_model.create_eggs(),5.0)]
        products+=[(nomenclature_model.create_soda(),5.0)]
        products+=[(nomenclature_model.create_cacao(),20.0)]
        products+=[(nomenclature_model.create_sour_cream(),200.0)]

        steps = [
        "Яйца взбить с сахаром до белой пены.",
        "Добавить просеянную муку, соду (можно погасить), растопленное остывшее сливочное масло, сметану и тщательно перемешать (лучше миксером).",
        "Тесто разделить на две равные части. В одну часть добавить 2 ст. ложки муки.В другую 2 ст. ложки какао.",
        "Перемешать, чтобы не было комочков.",
        "Тесто должно быть консистенции негустой сметаны.",
        "Широкую форму (26-28 см) смазать маслом. Вливать в центр поочередно небольшие порции разного теста (по столовой ложке). Не перемешивать!",
        "Выпекать пирог «Зебра» в предварительно разогретой духовке при температуре 190-200 градусов в течение получаса. Постоянно поглядывать. Если верх пирога уже пропечется, а середина еще нет - следует накрыть пирог фольгой, уменьшить температуру до 180 градусов и выпекать пирог «Зебра» до готовности."]
        return receipt_model.create(name, products, steps)




        



