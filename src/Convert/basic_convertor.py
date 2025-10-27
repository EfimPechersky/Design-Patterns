from .abstract_convertor import abstract_convertor

#Класс для преобразования данных простых типов
class basic_convertor(abstract_convertor):
    #Список конвертируемых данных
    convertible_data:list=[int, str, float,bool]