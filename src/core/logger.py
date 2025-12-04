from Core.abstract_logic import abstract_logic
from Core.observe_service import observe_service
from Core.event_type import event_type
from Core.validator import validator,argument_exception
from datetime import datetime
class logger(abstract_logic):
    types_of_output=["CONSOLE", "FILE"]
    output="CONSOLE"
    levels_of_logging=[event_type.debug(),event_type.info(),event_type.error()]
    log_level=event_type.error()
    def __init__(self):
        super().__init__()

        # Подключение в наблюдение
        observe_service.add(self)

    #Задание типа вывода
    def set_output(self,output):
        validator.validate(output,str)
        if not output in self.types_of_output:
            self.log(event_type.error(), "Wrong log output")
            raise argument_exception("Неверный тип вывода логов")
        self.output=output

    #Задание уровня логирования
    def set_log_level(self,level):
        validator.validate(level,str)
        if not level in self.levels_of_logging:
            self.log(event_type.error(), "Wrong log level")
            raise argument_exception("Неверный тип вывода логов")
        self.log_level=level

    #Логирование
    def log(self,type,params):
        if self.levels_of_logging.index(type)<self.levels_of_logging.index(self.log_level):
            return
        now=datetime.now()
        data=f"{now.strftime("%H:%M:%S")}|{type}: {params}"
        if self.output=="CONSOLE":
            #Вывод в консоль!
            print(data)
        elif self.output=="FILE":
            filename=now.strftime("%Y_%m_%d")+".log"
            with open(filename,"a") as file:
                file.write(data+"\n")
    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  
        if event in self.levels_of_logging:
            self.log(event, params)
        elif event in [event_type.add_new_reference(),event_type.deleted_reference(),event_type.deleting_reference(),event_type.change_reference()]:
            self.log(event_type.info(),event +" "+ params.id)
        elif event ==event_type.convert_to_json():
            self.log(event_type.info(),event +" "+params)
        elif event ==event_type.change_block_period():
            self.log(event_type.info(),event +" "+params.strftime("%d-%m-%Y"))
        elif event == event_type.set_logs_output():
            self.set_output(params)
            self.log(event_type.info(),event +" "+params)
        elif event == event_type.set_log_level():
            self.set_log_level(params)
            self.log(event_type.info(),event +" "+params)