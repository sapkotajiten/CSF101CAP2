#Jiten Sapkota
#First mechanical 
#02230263
#reference
#https://youtu.be/uOtAiKnDHP4?si=V_EXo4Po55TJQrWs
#https://youtu.be/ZQkA44lDtIk?si=NsoxddKsJGUFsFC-


import os
import random
import string

# Define the base class for Accounts
class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: Nu{amount}. New Balance: Nu{self.balance}")
        else:
            print("Invalid amount. Please enter a valid amount.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn: Nu{amount}. New Balance: Nu{self.balance}")
        else:
            print("Insufficient funds or invalid amount.")

    def save_to_file(self, file_name='accounts.txt'):
        with open(file_name, 'a') as f:
            f.write(f"{self.account_number},{self.password},{self.account_type},{self.balance}\n")


# Define the PersonalAccount class inheriting from Account
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, 'personal', balance)

# Define the BusinessAccount class inheriting from Account
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, 'business', balance)

# Function to generate a random account number
def generate_account_number():
    return ''.join(random.choices(string.digits, k=5))

# Function to generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))

# Function to load account information from file
def load_accounts(file_name='accounts.txt'):
    accounts = {}
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                account_number, password, account_type, balance = line.strip().split(',')
                balance = float(balance)
                if account_type == 'personal':
                    account = PersonalAccount(account_number, password, balance)
                elif account_type == 'business':
                    account = BusinessAccount(account_number, password, balance)
                accounts[account_number] = account
    return accounts

#Function to login to an account
def login(accounts):
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    
    account = accounts.get(account_number)
    if account and account.password == password:
        print("Login successful!")
        return account
    else:
        print("Invalid account number or password.")
        return None


#Function to transfer the fund
def fund_transfer(accounts, from_account):
    to_account_number = input("Enter the recipient's account number: ")
    amount = float(input("Enter the amount to send: "))
    if to_account_number in accounts:
        if from_account.balance >= amount:
            from_account.withdraw(amount)
            accounts[to_account_number].deposit(amount)
            print(f"Transferred Nu{amount} to {to_account_number}")
        else:
            print("Insufficient funds.")
    else:
        print("Recipient account not found.")

def main():
    accounts = load_accounts()

    while True:
        print("\n..Welcome to Bank of Bhutan..")
        print("1. Open an Account")
        print("2. Login to Account")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            print("Select Account Type:")
            print("1. Personal Account")
            print("2. Business Account")
            account_type = input("Enter your choice: ")
            if account_type in ['1', '2']:
                account_number = generate_account_number()
                password = generate_password()
                if account_type == '1':
                    account = PersonalAccount(account_number, password)
                else:
                    account = BusinessAccount(account_number, password)
                account.save_to_file()
                accounts[account_number] = account
                print(f"Account created successfully! Account Number: {account_number}, Password: {password}")
            else:
                print("Invalid account type selected.")

        elif choice == '2':
            account = login(accounts)
            if account:
                while True:
                    print("\n..Account Menu..")
                    print("1. Check Balance")
                    print("2. Deposit ")
                    print("3. Withdraw ")
                    print("4. Transfer funds")
                    print("5. Delete Account")
                    print("6. Logout")
                    account_choice = input("Enter your choice: ")

                    if account_choice == '1':
                        print(f"Your Balance: Nu{account.balance}")
                    elif account_choice == '2':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif account_choice == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif account_choice == '4':
                        fund_transfer(accounts, account)
                    elif account_choice == '5':
                        del accounts[account.account_number]
                        print("Account deleted successfully.")
                        break
                    elif account_choice == '6':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        
        elif choice == '3':
            print("..Thank you for using bank of Bhutan..")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
