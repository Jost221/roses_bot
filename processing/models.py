from bs_orm.DataTypes import *
from bs_orm.Requests import *

class User(Table):
    Id = Integer(primary_key=True)
    username = String(nullable=True)
    phone = Integer(nullable=True)
    purchase_consent = Integer(nullable=True)
    status = Integer(default=0)  # Первые 5 значений выделены для прохождения стартового опроса 
    magazin = String(nullable=True)
    transfer = Integer(default=0)
    cont_roses = Integer(nullable=True)
    magazin_station = Integer(default=0)


class Bank(Table):
    Id = Integer(primary_key=True)
    user_id = ForeignKey('User.Id')
    bank_name = String(nullable=True)
    bank_data = Integer(nullable=True)