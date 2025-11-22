from Core.start_service import start_service
from Core.repository import repository
from Models.transaction_model import transaction_model
from datetime import datetime
import time
service = start_service()
service.start(file=True)
#Создание ОСВ
def osv_example(serv):
    start_date=datetime.strptime(f"01-10-2025", "%d-%m-%Y")
    end_date=datetime.strptime(f"10-11-2025", "%d-%m-%Y")
    storage=serv.data[repository.storage_key()][0]
    osv=serv.create_osv(start_date,end_date,storage.id)
    return osv

#Создание транзакции
def transaction_example(serv,it):
    Y=2020+(it//28)//12
    m=1+it//28%12
    d=1+it%28
    date=datetime.strptime(f"{d}-{m}-{Y}", "%d-%m-%Y")
    nomenclature=serv.data[repository.nomenclature_key()][it%len(serv.data[repository.nomenclature_key()])]
    storage=serv.data[repository.storage_key()][0]
    range=nomenclature.range_count
    if not range.base_range is None:
        range=range.base_range
    return transaction_model.create(date, nomenclature, storage,10.0,range)

for it in range(0,1000):
    service.data[repository.transaction_key()].append(transaction_example(service,it))

service.block_period=datetime.strptime(f"01-01-2024", "%d-%m-%Y")
t1=time.time()
osv1 = osv_example(service)
t1=time.time()-t1
service.block_period=datetime.strptime(f"01-01-2020", "%d-%m-%Y")
t2=time.time()
osv2 =osv_example(service)
t2=time.time()-t2
service.block_period=datetime.strptime(f"01-01-2022", "%d-%m-%Y")
t3=time.time()
osv3 = osv_example(service)
t3=time.time()-t3
