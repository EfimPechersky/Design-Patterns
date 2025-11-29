from Core.abstract_logic import abstract_logic
from Core.observe_service import observe_service
from Core.event_type import event_type

class print_service(abstract_logic):

    def __init__(self):
        super().__init__()

        # Подключение в наблюдение
        observe_service.add(self)

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  

        if   event == event_type.convert_to_json():
            #Александр Серегеевич, этот принт написали вы на паре, не четвертуйте, пжл,
            print( f"params:{ params } ")
        return True
