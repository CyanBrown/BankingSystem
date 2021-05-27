import json
import random
from datetime import date, datetime
from decimal import *

class User:

    used_id = []

    def __init__(self, type, name, username, password, id=None):
        self.name = name
        self.username = username
        self.password = password

        self.type = type

        if id is None:
            self.id = User.generate_id()

        else:
            self.id = id

    def check_username_password(self, username, password):
        return self.username == username and self.password == password

    @staticmethod
    def generate_id():
        #TODO: make sure that id doesn't already exist
        return int("".join([str(random.randint(0,9)) for i in range(6)]))



class NormalUser(User):

    def __init__(self, name, bday, username, password, initial_deposit=0.0, id=None):
        super().__init__("normal", name, username, password, id=id)

        self.birthdate = bday
        self.balance = initial_deposit

    def get_tuple(self):
        return (self.id, self.name, self.birthdate, self.balance, self.username, self.password, False)

    def get_update(self):
        return f"name='{self.name}', balance={self.balance}, username='{self.username}',password='{self.password}', is_admin=0"

    def add_balance(self, amount):
        self.balance += amount
        self.balance = round(self.balance, 2)

    def __eq__(self, other):
        return other.id == self.id

    def __str__(self):
        return f"\nID: {str(self.id)}\nNAME: {self.name}\nBIRTHDATE: {self.birthdate}\nBALANCE: ${str(self.balance)}"


class Administrator(User):
    def __init__(self, name, username, password, id=None):
        super().__init__("admin", name, username, password, id=id)

    def get_tuple(self):
        return (self.id, self.name, '2001-01-01', 0.0, self.username, self.password, True)

    def get_update(self):
        return f"name='{self.name}', balance=0.0, username='{self.username}', password='{self.password}', is_admin=1"

    def __str__(self):
        return "\nID: "+str(self.id)+"\nNAME: "+self.name+"\n"

    @staticmethod
    def create_normal_user():
        user = NormalUser(input("NAME: "), input("BIRTHDATE: "), input("USERNAME: "), input('PASSWORD: '), float(input("INITIAL DEPOSIT: ")))

        return user

    @staticmethod
    def create_admin_user():
        user = Administrator(input("NAME: "), input("USERNAME: "), input("PASSWORD: "))

        return user
