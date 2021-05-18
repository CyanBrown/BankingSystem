import os

from users import *

import blessed
import stdiomask
from typing import List
from decimal import *
import mysql.connector

from datetime import datetime

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

    def login_user(self, username: str, pwd: str):

        self.cursor.execute(f"select * from NormalUsers where username = '{username}' and password = '{pwd}'")

        cur = [i for i in self.cursor]

        if len(cur) == 1:
            user = cur[0]
            print(user)

        print("incorrect")

        # load one user at a time




    def save_users(self, user : User):

        # save given user
        pass


class BankingSystem():
    def __init__(self, userdb: UserDb):
        self.users = userdb
        self.error_str = ""
        self.main_loop()

    def request_login(self, limit):

        #only return user object

        for i in range(limit):
            os.system('cls')
            print("Log into the ATM system.")
            username = input("Username: ")
            password = stdiomask.getpass()

            # this will be replaced with a search alg
            person_idx = self.users.login_user(username, password)
            if person_idx is not None:
                os.system('cls')
                return person_idx

        print(term.red + 'You have run out of attempts' + term.red)
        quit()

    def get_command(self):
        commands = input("What would you like to do (type 'help' for more info): ").replace("$", '').split()

        if len(commands) == 0:
            self.error_str = "No command was given"

        else:
            return commands

    def deposit(self, idx, command):
        try:
            if self.users.users[idx].type == 'normal':
                self.users.users[idx].add_balance(float(command))

            else:
                self.error_str = "Administrators cannot deposit."

        except TypeError:
            self.error_str = "Amount of money to deposit is invalid."

    def withdraw(self, idx, command):
        try:
            if self.users.users[idx].type == 'normal':
                self.users.users[idx].add_balance(-float(command))

            else:
                self.error_str = "Administrators cannot withdraw."

        except TypeError:
            self.error_str = "Amount of money to withdraw is invalid."

    def create_user(self):
        print()
        user_type = input("What type of user do you want to create? (administrator / normal): ")

        if user_type == 'normal':
            self.users.users.append(
                NormalUser(input("NAME: "), input("BIRTHDATE: "), input("USERNAME: "), input("PASSWORD: "),
                           float(input("INITIAL DEPOSIT: "))))

        elif user_type == 'administrator':
            self.users.users.append(Administrator(input("NAME: "), input("USERNAME: "), input("PASSWORD: ")))

        else:
            self.error_str = f"{user_type} is not a valid input to create a user."

    def modify_user(self, idx):

        while True:
            os.system('cls')
            what = input("What would you like to modify (exit to leave): ")

            if what == 'exit':
                break

            exchange = input("What would you like to exchange it with: ")

            if what == "name":
                self.users.users[idx].name = exchange
            elif what == 'id':
                self.users.users[idx].id = int(exchange)
            elif what == 'birthdate':
                self.users.users[idx].birthdate = exchange
            elif what == 'username':
                self.users.users[idx].username = exchange
            elif what == 'password':
                self.users.users[idx].password = exchange
            elif what == 'balance':
                self.users.users[idx].balance = float(exchange)
            else:
                self.error_str = "Improper field for modification."

    def main_loop(self):
        # login user
        print(f"{term.home}{term.black_on_skyblue}{term.clear}")

        idx = self.request_login(limit=3)

        while True:
            self.users.load_users()
            os.system('cls')

            print(self.error_str)
            print(self.users.users[idx])
            print()

            self.error_str = ""

            commands = self.get_command()

            if commands[0] == 'deposit':
                self.deposit(idx, commands[1])

            elif commands[0] == 'withdraw':
                self.withdraw(idx, commands[1])

            elif " ".join(commands) == "create user":
                if self.users.users[idx].type == 'admin':
                    self.create_user()

                else:
                    self.error_str = "You do not have permission to create users."

            elif " ".join(commands) == "modify user":
                if self.users.users[idx].type == 'admin':
                    new_idx = self.request_login(limit=10)
                    self.modify_user(new_idx)

                else:
                    self.error_str = "You do not have permission to modify users."

            elif commands[0] == 'logout':
                self.main_loop()
                break

            elif commands[0] == 'exit':
                break

            self.users.save_users()


if __name__ == "__main__":
    users = UserDb()

    bank = BankingSystem(users)
