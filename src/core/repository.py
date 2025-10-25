class repository:
    __data:dict={}
    """Хранилище данных"""
    @property
    def data(self):
        return self.__data
    
    """Ключ доступа к единицам измерения"""
    @staticmethod
    def range_key():
        return "range_model"
    
    """Ключ доступа к группам номенклатуры"""
    @staticmethod
    def group_key():
        return "group_model"
    
    """Ключ доступа к номенклатурам"""
    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"
    
    """Ключ доступа к рецептам"""
    @staticmethod
    def receipt_key():
        return "receipt_model"
    
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(repository) if
                    callable(getattr(repository, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(repository, method)()
            result.append(key)

        return result

    
    """
    Инициализация
    """
    def initalize(self):
        keys = repository.keys()
        for key in keys:
            self.__data[ key ] = []
