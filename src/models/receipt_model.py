from .abstract_model import abstract_model
from .nomenclature_model import nomenclature_model
from Core.validator import validator, operation_exception, argument_exception
from Core.repository import repository
from Models.range_model import range_model
import os
"""Класс, описывающий рецепты"""
class receipt_model(abstract_model):
    __ingridients:list=[]
    __steps:list=[]

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
            if len(i)<3:
                raise argument_exception("Недостаточно параметров ингридиента")
            validator.validate(i[0],nomenclature_model)
            validator.validate(i[1],float)
            validator.validate(i[2],range_model)
        self.__ingridients=other

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
    
    @staticmethod
    def create(name, ingridients, steps, repo=None):
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
        if repo!=None:
            validator.validate(repo, repository)
            for i in repo.data[repository.receipt_key]:
                if i.name==name:
                    return i
        rm = receipt_model()
        rm.name = name
        rm.ingridients = ingridients
        rm.steps = steps
        return rm
    
    """Создание рецепта вафель"""
    @staticmethod
    def create_waffles_receipt(repo=None):
        name = "ВАФЛИ ХРУСТЯЩИЕ В ВАФЕЛЬНИЦЕ"

        products = []
        products+=[(nomenclature_model.create_butter(repo),70.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_sugar(repo),80.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_flour(repo),100.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_eggs(repo),1.0,range_model.create_num(repo))]
        products+=[(nomenclature_model.create_vanilla(repo),5.0,range_model.create_gramm(repo))]

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
        return receipt_model.create(name, products, steps,repo=repo)
    
    """Создание рецепта пирога"""
    @staticmethod
    def create_pie_receipt(repo=None):
        name = "ПИРОГ ЗЕБРА"

        products = []
        products+=[(nomenclature_model.create_butter(repo),150.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_sugar(repo),240.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_flour(repo),250.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_eggs(repo),5.0,range_model.create_num(repo))]
        products+=[(nomenclature_model.create_soda(repo),5.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_cacao(repo),20.0,range_model.create_gramm(repo))]
        products+=[(nomenclature_model.create_sour_cream(repo),200.0,range_model.create_milliliter(repo))]

        steps = [
        "Яйца взбить с сахаром до белой пены.",
        "Добавить просеянную муку, соду (можно погасить), растопленное остывшее сливочное масло, сметану и тщательно перемешать (лучше миксером).",
        "Тесто разделить на две равные части. В одну часть добавить 2 ст. ложки муки.В другую 2 ст. ложки какао.",
        "Перемешать, чтобы не было комочков.",
        "Тесто должно быть консистенции негустой сметаны.",
        "Широкую форму (26-28 см) смазать маслом. Вливать в центр поочередно небольшие порции разного теста (по столовой ложке). Не перемешивать!",
        "Выпекать пирог «Зебра» в предварительно разогретой духовке при температуре 190-200 градусов в течение получаса. Постоянно поглядывать. Если верх пирога уже пропечется, а середина еще нет - следует накрыть пирог фольгой, уменьшить температуру до 180 градусов и выпекать пирог «Зебра» до готовности."]
        return receipt_model.create(name, products, steps,repo=repo)

    def __repr__(self):
        return "Рецепт "+super().__repr__()




        



