import json
import random
import string
from pathlib import Path

class Bank:
    database = 'database.json'
    data = []

    if Path(database).exists():
        with open(database) as fs:
            data = json.loads(fs.read())

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=8)
        num = random.choices(string.digits, k=4)
        acno = alpha + num
        random.shuffle(acno)
        return "".join(acno)

    def create_user(self):
        info = {
            "name": input("Enter your name: "),
            "age": int(input("Enter your age: ")),
            "email": input("Enter your email: "),
            "Accountno": Bank.__accountgenerate(),
            "pin": int(input("Enter a 4-digit PIN: ")),
            "balance": 0
        }

        if info["age"] < 12 or len(str(info["pin"])) != 4:
            print("Sorry, we cannot create this account. Age must be 12+ and PIN must be 4 digits.")
        else:
            Bank.data.append(info)
            Bank.__update()
            print(f"Account created successfully! Your Account No: {info['Accountno']}")

    def deposite_money(self):
        acno = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))
        userdata = [i for i in Bank.data if i["Accountno"] == acno and i["pin"] == pin]

        if not userdata:
            print("Sorry, no such user exists.")
        else:
            amount = int(input("Enter amount to deposit: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print(f"₹{amount} deposited successfully. New balance: ₹{userdata[0]['balance']}")

    def withdraw_money(self):
        acno = input("Enter your account number: ")
        pin = int(input("Enter your PIN: "))
        userdata = [i for i in Bank.data if i["Accountno"] == acno and i["pin"] == pin]

        if not userdata:
            print("Sorry, no such user exists.")
        else:
            amount = int(input("Enter amount to withdraw: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
            elif amount > userdata[0]['balance']:
                print("Insufficient balance.")
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print(f"₹{amount} withdrawn successfully. New balance: ₹{userdata[0]['balance']}")

    def detail_user(self):
        acno = input("Enter your account number: ")      # account no is a string, not int
        pin = int(input("Enter your PIN: "))
        userdata = [i for i in Bank.data if i["Accountno"] == acno and i["pin"] == pin]

        if not userdata:
            print("No data found.")
        else:
            print("\n--- User Details ---")
            for key in userdata[0]:
                print(f"{key} : {userdata[0][key]}")
            print("--------------------\n")

    def update_detail(self):
        acno = input("Enter your account number: ")      # account no is a string, not int
        pin = int(input("Enter your PIN: "))
        userdata = [i for i in Bank.data if i["Accountno"] == acno and i["pin"] == pin]

        if not userdata:
            print("No user found.")
        else:
            print("Note: You cannot change balance and account number.")

            newdata = {
                "name": input("Enter new name (or press Enter to skip): "),
                "email": input("Enter new email (or press Enter to skip): "),
                "pin": input("Enter new PIN (or press Enter to skip): ")
            }

            if newdata['name'] == "":
                newdata['name'] = userdata[0]['name']
            if newdata['email'] == "":
                newdata['email'] = userdata[0]['email']
            if newdata['pin'] == "":
                newdata['pin'] = str(userdata[0]['pin'])
            elif len(newdata['pin']) != 4 or not newdata['pin'].isdigit():
                print("Invalid PIN. Must be 4 digits. PIN not updated.")
                newdata['pin'] = str(userdata[0]['pin'])

            for key in userdata[0]:
                if key in newdata and key != 'pin':
                    userdata[0][key] = newdata[key]
                elif key == 'pin':
                    userdata[0][key] = int(newdata[key])

            Bank.__update()
            print("Details updated successfully.")

    def delete_ac(self):
        acno = input("Enter your account number: ")      # account no is a string, not int
        pin = int(input("Enter your PIN: "))
        userdata = [i for i in Bank.data if i["Accountno"] == acno and i["pin"] == pin]

        if not userdata:
            print("No such user found.")
        else:
            print("Are you sure you want to delete your account?")
            check = input("Press y (yes) or n (no): ")
            if check.lower() == 'y':
                index = Bank.data.index(userdata[0])   # find index and remove
                Bank.data.pop(index)
                Bank.__update()
                print("Account deleted successfully.")
            else:
                print("Deletion cancelled.")


bank = Bank()
while True:
 
 print("\n===== BANK MENU =====")
 print("Press 1 for creating account")
 print("Press 2 for depositing money")
 print("Press 3 for withdrawing money")
 print("Press 4 for user details")
 print("Press 5 for updating user details")
 print("Press 6 for deleting account")
 print("Press 0 to exit")
 res=int(input("tell your respone"))
    

 if res == 1:
    bank.create_user()
 elif res == 2:
    bank.deposite_money()
 elif res == 3:
    bank.withdraw_money()
 elif res == 4:
        bank.detail_user()
 elif res == 5:
        bank.update_detail()
 elif res == 6:
        bank.delete_ac()
 elif res == 0:
        print("Thank you for using our bank. Goodbye!")
        break
 else:
        print("Invalid input, try again.")