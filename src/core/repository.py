class repository:
    __data:dict={}
    """Хранилище данных"""
    @property
    def data(self):
        return self.__data
    
    """Ключ доступа к единицам измерения"""
    @property
    def range_key(self):
        return "range_model"
    
    """Ключ доступа к группам номенклатуры"""
    @property
    def group_key(self):
        return "group_model"
    
    """Ключ доступа к номенклатурам"""
    @property
    def nomenclature_key(self):
        return "nomenclature_model"
    
    """Ключ доступа к рецептам"""
    @property
    def receipt_key(self):
        return "receipt_model"
