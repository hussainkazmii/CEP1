import json
import os
import random
import string
import ast
from datetime import datetime
from abc import ABC, abstractmethod


class Account(ABC):                              # Abstract Class
    def __init__(self,balance=0):
        self.balance = balance
        self.acc_number = username_ + ''.join(random.choices(string.digits, k=5))

    @abstractmethod                              # Abstract Method
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):                 # Method Overridden in every sub-class
        pass

    def balanceEnquiry(self):
        pass


class Transaction:
    trans_count = 0

    def __init__(self, trans_type, trans_amount, acc_type, acc_number):
        self.date = datetime.now()
        Transaction.trans_count += 1
        self.trans_ID = Transaction.trans_count
        self.trans_type = trans_type
        self.trans_amount = trans_amount
        self.all_trans = []
        self.acc_type = acc_type
        self.acc_number = acc_number

        tr = [f'Transaction: {self.trans_ID}', f'Transaction Type: {self.trans_type}', f'Amount: {self.trans_amount}',
              f'Timestamp: {self.date}', f'Account Number: {self.acc_number}']
        with open(f'{username_}.txt', 'a+') as f1:
            f1.write(str(tr)+'\n')
            print(f1)
        self.all_trans += tr          # Operator Overloading- List concatenation

    def displayTransaction(self):
        print("Transaction ID:", self.trans_ID)
        print("Transaction Type:", self.trans_type)
        print("Amount:", self.trans_amount)
        print("Timestamp:", self.date)


class CheckingAccount(Account):                  # Inheritance
    def __init__(self, acc_number, balance=0, credit_limit=1500, overdraft_fee=0):
        super().__init__(acc_number)
        self.credit_limit = credit_limit
        self.overdraft_fee = overdraft_fee
        h = Transaction('Deposit', amount, 'Saving Account', self.acc_number)
        d = {'Account Number': self.acc_number,
             'Account Type': 'Saving',
             'Balance': self.balance,
             'Transaction': h}

    def deposit(self, amount):
        self.balance += amount
        Transaction('Deposit', amount, 'Checking Account', self.acc_number)
        return self.balance

    def withdraw(self, amount):
        if self.balance + self.credit_limit >= amount:
            self.balance -= amount
            Transaction('Withdraw', amount, 'Checking', self.acc_number)
        else:
            print('Insufficient balance')

    def deduct_overdraft_fee(self):
        if self.balance < 0:
            overdraft_fee = abs(self.balance) * self.overdraft_fee
            self.balance -= overdraft_fee

    def balanceEnquiry(self):
        return f'Balance:{self. balance}'


class SavingAccount(Account):
    def __init__(self, acc_number, interest_rate=0.0, balance=0, n=0):
        super().__init__(acc_number, balance)
        self.acc_number = username_ + ''.join(random.choices(string.digits, k=5))
        self.interest = 0
        self.interest_rate = interest_rate      #monthly
        self.months = n
        h = Transaction('Deposit', amount, 'Saving Account', self.acc_number)
        d = {'Account Number': self.acc_number,
        'Account Type': 'Saving',
        'Balance': self.balance,'\n'
        'Transaction': h.__dict__}

        with open(f'{username_}.txt', 'a+') as c:
            c.write(json.dumps(d)+'\n')

    def deposit(self, amount):
        self.balance += amount
        Transaction('Deposit', amount, 'Checking Account', self.acc_number)  # Composition
        # Write transaction details to the file
        tr = f'Deposit: {amount} | Balance: {self.balance}'
        with open(f'{Customer().username}.txt', 'a+') as f1:
            f1.write(tr + '\n')

        Transaction('Deposit', amount, 'Saving', self.acc_number)     # Composition

    def setInterest(self, interest_rate):
        self.interest_rate = interest_rate

    def getInterest(self):
        return 'Interest rate:', self.interest_rate

    def calc_monthly_interest(self, n):
        interest = (1 + self.interest_rate)**n         #n represents number of months
        self.balance *= interest

    def get_balance(self, n):
        return f'Balance after {n} months: {round(self.balance,3)}$'

    def withdraw(self, amount):
        if self.balance + self.credit_limit >= amount:
            self.balance -= amount
            Transaction('Withdraw', amount, 'Checking', self.acc_number)
            # Write transaction details to the file
            tr = f'Withdraw: {amount} | Balance: {self.balance}'
            with open(f'{username_}.txt', 'a+') as f1:
                f1.write(tr + '\n')
        else:
            print('Insufficient balance')

    def balanceEnquiry(self):
        return f'Balance:{self. balance}'


class LoanAccount(Account):
    def __init__(self, acc_number, balance, principal_amount=0, interest_rate=0.0, loan_duration=0):
        super().__init__(acc_number, balance)
        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.interest = 0
        self.loan_duration = loan_duration
        self.loan_balance = balance
        self.acc_number = username_ + ''.join(random.choices(string.digits, k=5))

        h = Transaction('Deposit', amount, 'Loan Account', self.acc_number)
        d = {'Account Number': self.acc_number,
             'Account Type': 'Saving',
             'Balance': self.balance, '\n'
                                      'Transaction': h.__dict__}

    def withdraw(self, principal_amount):
        self.principal_amount = principal_amount
        Transaction('Loan Amount', principal_amount, 'Loan', self.acc_number)

    def calc_monthly_interest(self):
        monthly_interest = self.interest_rate * (self.loan_duration/12)
        self.interest = self.principal_amount * monthly_interest

    def total_loan(self):
        self.loan_balance = self.principal_amount + self.interest
        return str(self.loan_balance)+' $ is the total loan amount.'     #Operator Overloading- String concatenation

    def deposit(self, amount):
        if amount <= self.loan_balance:
            self.loan_balance -= amount
            print(f'{self.loan_balance} is remaining.')
            Transaction('Loan Deposited', amount, 'Loan', self.acc_number)
        else:                 # Exception handling can be done too
            print(f'Overpayment!, {amount-self.loan_balance}$ will be refunded')

    def balanceEnquiry(self):
        return f'Balance:{self.loan_balance}'


class Customer:
    def __init__(self):
        self.accounts = []


    def create_acc(self):
        username_ = input('Enter username: ')
        password_ = input('Enter password: ')
        f_name = input('Enter first name: ')
        l_name = input('Enter last name: ')
        address = input('Enter address: ')

        d = {'Username': username_, 'Password': password_, 'First Name': f_name,
             'Last Name': l_name, 'Address': address}

        with open(f'Users.txt', 'a+') as f1:
            f1.write(f'{username_} {password_}\n')
        with open(f'{username_}.txt', 'a+') as f:
            for key, value in d.items():
                f.write(f'{key}: {value}\n')
        self.acc()

    def login(self):
        while True:


            choice = input("Choose an operation:\n1 - Create Account\n2 - Balance\n"
                           "3 - Transaction History\n4 - Generate Report\n5 - Make Transactions\n6 - Logout:\n ")


            if choice == "1":
                self.acc()

            elif choice == "2":
                account_number = input("Enter account number: ")
                with open(f'{username_}.txt', 'r+') as n:
                    for line in n:
                        try:  # Exception Handling
                            data = ast.literal_eval(line)
                            if isinstance(data, dict) and account_number in data.values():
                                for key, value in data.items():
                                    if key == 'Balance':
                                        print(f'{key}:{value}')

                        except (SyntaxError, ValueError):
                            continue

            elif choice == "3":
                print(f"Transaction History Report for {username_}\n")
                with open(f'{username_}.txt', 'r+') as f:
                    for line in f:
                        try:
                            data = ast.literal_eval(line)
                            if isinstance(data, dict) in data.values():
                                print(data)
                        except (SyntaxError, ValueError):
                            continue

            elif choice == "4":
                print(f"Account Report for {username_}\n")
                with open(f'{username_}.txt', 'r+') as f:
                    for line_number, line in enumerate(f, start=1):
                        print(line.strip())
                        if line_number == 5:
                            continue

            elif choice == '5':
                account_number = input('Enter account number: ')
                temp_file_path = f'temp_{username_}.txt'
                with open(f'{username_}.txt', 'r') as file, open(temp_file_path, 'w') as temp_file:
                    for line in file:
                        try:
                            data = ast.literal_eval(line)
                            if isinstance(data, dict) and account_number in data.values():
                                d = input('Do you want to deposit or withdraw account?(D/W): ').upper()
                                if d == 'D':
                                    dep = int(input('Enter amount to be deposited: '))
                                    value = data['Balance']
                                    value += dep
                                    data['Balance'] = value
                                    temp_file.write(json.dumps(data) + '\n')
                                    print('Updated Balance:', value)
                                    break

                                elif d == 'W':
                                    wit = int(input('Enter amount to be withdrawn: '))
                                    if wit <= data['Balance']:
                                        value = data['Balance']
                                        value -= wit
                                        data['Balance'] = value
                                        temp_file.write(json.dumps(data) + '\n')
                                        print('Updated Balance:', value)
                                        break


                                else:
                                    print('Insufficient balance')
                            else:
                                print('Invalid input')

                            temp_file.write(json.dumps(data) + '\n')
                        except (SyntaxError, ValueError):
                            temp_file.write(line)
                os.remove(f'{username_}.txt')
                os.rename(temp_file_path, f'{username_}.txt')
            elif choice == "6":
                print("Logged out")
                break
            else:
                print("Invalid choice")



    def acc(self):
        try:
            acc_type = str(input('Enter account type: '))
            if acc_type == 'Checking':
                account = CheckingAccount(acc_number='', balance=2000)
                s = input('Do you want to make transactions?(Y/N): ').upper()
                if s == 'Y':
                    a = input('Do want to deposit or withdraw amount?(D/W): ').upper()
                    if a == 'D':
                        dep = int(input('Enter amount to be deposited:'))
                        account.deposit(dep)
                    elif a == 'W':
                        wit = int(input('Enter amount to be withdrawn: '))
                        account.withdraw(wit)
            elif acc_type == 'Savings':
                account = SavingAccount(acc_number='', interest_rate=0.06)
                s = input('Do you want to make transactions?(Y/N): ').upper()
                if s == 'Y':
                    a = input('Do want to deposit or withdraw amount?(D/W): ').upper()
                    if a == 'D':
                        dep = int(input('Enter amount to be deposited:'))
                        account.deposit(dep)
                    elif a == 'W':
                        wit = int(input('Enter amount to be withdrawn: '))
                        account.withdraw(wit)
            elif acc_type == 'Loan':
                account = LoanAccount(acc_number='', balance=0)
                s = input('Do you want to make transactions?(Y/N): ').upper()
                if s == 'Y':
                    a = input('Do want to take or pay loan(T/P): ').upper()
                    if a == 'T':
                        loan = int(input('Enter loan amount: '))
                        account.withdraw(loan)
                    elif a == 'P':
                        pay = int(input('Enter amount to be payed: '))
                        account.deposit(pay)

            else:
                raise ValueError('Invalid Account Type !')               # Create exception handling ( TYPE ERROR )

        except ValueError as e:
            print(str(e))

    def get_account(self, account_number):
        for account in self.accounts:
            if account == account_number:
                return account
        return None

ask = input("are you an admin or user? ").lower()
if ask == "user":
    while True:
        ask1 = input('Enter L for login and N for new account: ').upper()
        if ask1 == 'L':
            username_ = input("Enter your username: ")
            password_ = input("Enter your password: ")

            def check():
                with open('Users.txt', 'r') as f2:
                    s = f2.readlines()
                    for line in s:
                        if username_ and password_ in line:
                            cust = Customer()
                            cust.login()
                            break
                    else:
                        print('Incorrect Login info...Please try again')
            check()
        elif ask1 == 'N':
            cust1 = Customer()
            cust1.create_acc()
        else:
            print('Enter L or N only for Login and New Account respectively !')

elif ask == 'admin':
    class Admin:
        admin_user = 'bank.admin'
        admin_pw = '130903'

        @staticmethod
        def all_cust_details():
            with open('Users.txt', 'r') as g:
                for line in g:
                    words = line.split()
                    if words:
                        with open(f'{words[0]}.txt', 'r') as g1:
                            print(g1.read())

        @staticmethod
        def cust_details():
            user = input('Enter username of customer: ')
            with open('Users.txt', 'r') as f:
                for line in f:
                    if user in line:
                        with open(f'{user}.txt', 'r') as f1:
                            print(f1.read())
                            break
                else:
                    print('Invalid Username')


        @staticmethod
        def del_cust():
            user = input('Enter username of customer: ')
            with open('Users.txt', 'r') as f:
                for line in f:
                    if user in line:
                        os.remove(f'{user}.txt')
                        print('USER REMOVED SUCCESSFULLY')
                        break
                else:
                    print('Invalid Username')

        @staticmethod
        def admin_login():
            check_admin = input("Enter admin username: ")
            check_admin_pw = input("Enter admin password: ")
            if check_admin == Admin.admin_user and check_admin_pw == Admin.admin_pw:
                while True:
                    choice = input("Choose an operation:\n1 - View All Customer Details\n2 - Customer Details\n"
                                   "3 - Delete Customer\n4 - Logout:\n ")
                    if choice == '1':
                        Admin.all_cust_details()
                    elif choice == '2':
                        Admin.cust_details()
                    elif choice == '3':
                        Admin.del_cust()
                    elif choice == '4':
                        print('Logged Out')
                        break

            else:
                print("Invalid admin credentials")

    Admin.admin_login()

else:
    print('Invalid option')
