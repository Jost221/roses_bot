from bs_orm import Requests
import processing.models as models

def create_user(user_id):
    return models.User.add_if_not_exist(Id=user_id)

def create_bank(user_id):
    return models.Bank.add_if_not_exist(user_id=user_id)

def get_user_status(user_id):
    return models.User.search(Id=user_id)[0].status

def save_user_data(user_id: int, name_value: str, value, status=1):
    old_obj = models.User.search(Id=user_id)[0]
    new_status = old_obj.status+status
    new_data = {name_value: value}
    old_obj.update(status=new_status, **new_data)

def save_bank_data(user_id: int, name_value: str, value, status=1):
    old_usr = models.User.search(Id=user_id)[0]
    new_data = {name_value: value}
    bank = models.Bank.search(user_id=user_id)[0]
    bank.update(**new_data)
    old_usr.update(status=old_usr.status+status)


def get_magazin(user_id):
    return models.User.search(Id=user_id)[0].magazin

def get_count_roses(user_id):
    return models.User.search(Id=user_id)[0].cont_roses

def get_bank_info():
    obj = models.Bank.search()
    need_data = []
    for item in obj:
        need_data.append({
            'data': item.bank_data,
            'name': item.bank_name
        })
    return need_data

def set_status(user_id, status):
    usr = models.User.search(Id=user_id)[0]
    usr.update(status=status)

def set_magazin(user_id, magazin, count_roses):
    usr = models.User.search(Id=user_id)[0]
    usr.update(magazin_station=0, magazin=magazin, count_roses=count_roses)

def get_purchase_consent(user_id):
    return models.User.search(Id=user_id)[0]

def set_magazin_station(user_id, station):
    models.User.search(Id=user_id)[0].update(magazin_station=station)

def get_magazine_station(user_id):
    return models.User.search(Id=user_id)[0].magazine_station
    
