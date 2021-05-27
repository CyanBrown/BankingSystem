import os
import time

from users import *

import blessed
import stdiomask
from typing import List
from decimal import *
import mysql.connector

from datetime import date

term = blessed.Terminal()


class UserDb():
    def __init__(self):

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="my-secret-pw",
            database="BankingSystem"
        )

        self.cursor = self.db.cursor()

    def create_user_from_tuple(self, tup):
        tup = list(tup)

        if tup[6] is not None and tup[6] != 0:
            return Administrator(tup[1], tup[4], tup[5], id=tup[0])

        else:

            return NormalUser(tup[1], tup[2].strftime("%Y-%m-%d"), tup[4], tup[5], initial_deposit=tup[3], id=tup[0])

    def login_user(self, username: str, pwd: str):

        self.cursor.execute(f"select * from NormalUsers where username = '{username}' and password = '{pwd}'")

        cur = [i for i in self.cursor]

        if len(cur) == 1:
            user = cur[0]
            return self.create_user_from_tuple(user)
        else:
            return None



    def save_user(self, user):

        # print(f'insert into NormalUsers values {user.get_tuple()}')
        print(f"insert into NormalUsers values{user.get_tuple()}")

        try:
            self.cursor.execute(f"insert into NormalUsers values{user.get_tuple()}")
        except mysql.connector.errors.IntegrityError:
            self.cursor.execute(f"update NormalUsers set {user.get_update()} where id={user.id}")
        self.db.commit()


class BankingSystem():
    def __init__(self, userdb: UserDb):
        self.users = userdb
        self.error_str = ""
        self.main_loop()
        self.user = None

    def request_login(self, limit):

        # only return user object

        for i in range(limit):
            os.system('cls')
            print("Log into the ATM system.")
            username = input("Username: ")
            password = stdiomask.getpass()

            # this will be replaced with a search alg
            person = self.users.login_user(username, password)
            if person is not None:
                os.system('cls')
                return person

        print(term.red + 'You have run out of attempts' + term.red)
        quit()

    def get_command(self):
        commands = input("What would you like to do (type 'help' for more info): ").replace("$", '').split()

        if len(commands) == 0:
            self.error_str = "No command was given"

        else:
            return commands

    def deposit(self, command):
        try:
            if self.user.type == 'normal':
                self.user.add_balance(float(command))
                self.users.save_user(self.user)

            else:
                self.error_str = "Administrators cannot deposit."

        except TypeError:
            self.error_str = "Amount of money to deposit is invalid."

    def withdraw(self, command):
        try:
            if self.user.type == 'normal':
                self.user.add_balance(-float(command))
                self.users.save_user(self.user)

            else:
                self.error_str = "Administrators cannot withdraw."

        except TypeError:
            self.error_str = "Amount of money to withdraw is invalid."

    def create_user(self):
        print()
        user_type = input("What type of user do you want to create? (administrator / normal): ")

        if user_type == 'normal':
            self.users.save_user(
                NormalUser(input("NAME: "), input("BIRTHDATE: "), input("USERNAME: "), input("PASSWORD: "),
                           float(input("INITIAL DEPOSIT: "))))

        elif user_type == 'administrator':
            self.users.save_user(Administrator(input("NAME: "), input("USERNAME: "), input("PASSWORD: ")))

        else:
            self.error_str = f"{user_type} is not a valid input to create a user."

    def modify_user(self, person):

        while True:
            os.system('cls')
            what = input("What would you like to modify (exit to leave): ")

            if what == 'exit':
                break

            exchange = input("What would you like to exchange it with: ")

            if what == "name":
                person.name = exchange
            elif what == 'id':
                person.id = int(exchange)
            elif what == 'birthdate':
                person.birthdate = exchange
            elif what == 'username':
                person.username = exchange
            elif what == 'password':
                person.password = exchange
            elif what == 'balance':
                person.balance = float(exchange)
            else:
                self.error_str = "Improper field for modification."

        self.users.save_user(person)

    def main_loop(self):
        # login user
        print(f"{term.home}{term.black_on_skyblue}{term.clear}")

        self.user = self.request_login(limit=3)

        while True:

            os.system('cls')

            print(self.error_str)
            print(self.user)
            print()

            self.error_str = ""

            commands = self.get_command()

            if commands[0] == 'deposit':
                self.deposit(commands[1])

            elif commands[0] == 'withdraw':
                self.withdraw(commands[1])

            elif " ".join(commands) == "create user":
                if self.user.type == 'admin':
                    self.create_user()

                else:
                    self.error_str = "You do not have permission to create users."

            elif " ".join(commands) == "modify user":
                if self.user.type == 'admin':
                    modify_person = self.request_login(limit=10)
                    self.modify_user(modify_person)

                else:
                    self.error_str = "You do not have permission to modify users."

            elif commands[0] == 'logout':
                self.main_loop()
                break

            elif commands[0] == 'exit':
                break


if __name__ == "__main__":
    users = UserDb()

    bank = BankingSystem(users)
