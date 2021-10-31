import random
import math
import sqlite3
conn = sqlite3.connect('card.s3db')
exe = conn.cursor()
exe.execute("""DROP TABLE card;""")
conn.commit()
exe.execute("""CREATE TABLE card (
    id INTEGER, 
    number TEXT, 
    pin TEXT, 
    balance INTEGER DEFAULT 0
);""")
conn.commit()

numbers = "0123456789"


def check_luth(number):
    lst = list(map(lambda x: int(x), number))
    summa = 0
    i = 1
    for num in lst:
        if i % 2 == 1:
            num *= 2
        if num > 9:
            num -= 9
        summa += int(num)
        i += 1
    return summa % 10 == 0


def get_luth(number):
    lst = list(map(lambda x: int(x), number))
    summa = 0
    i = 1
    for num in lst:
        if i % 2 == 1:
            num *= 2
        if num > 9:
            num -= 9
        summa += int(num)
        i += 1
    return math.ceil(summa / 10) * 10 - summa


def generate_num(n):
    i = 0
    if n == 4:
        result = ""
        while i < n:
            result = result + random.choice(numbers)
            i += 1
    else:
        result = "400000"
        while i < n - 1:
            result = result + random.choice(numbers)
            i += 1
        result = result + str(get_luth(result))

    return result


def get_number(num):
    exe.execute("SELECT number FROM card")
    rows = exe.fetchall()
    conn.commit()
    list_2 = []
    if num == "list":
        for elem in rows:
            list_2.append(elem[0])
        return list_2
    else:
        return rows[num][0]


def get_pin(num):
    exe.execute("SELECT pin FROM card")
    rows = exe.fetchall()
    conn.commit()
    list_1 = []
    if num == "list":
        for elem in rows:
            list_1.append(elem[0])
        return list_1
    else:
        return rows[num][0]


def get_balance(num):
    exe.execute(f"SELECT balance FROM card WHERE number={num}")
    rows = exe.fetchall()
    conn.commit()
    return rows[0][0]


log = True
x = 0
while log:
    choice = int(input("""\n1. Create an account
2. Log into account
0. Exit\n"""))
    if choice == 1:
        exe.execute("INSERT INTO card (id, number, pin) VALUES (?, ?, ?)", (x+1, generate_num(10), generate_num(4)))
        conn.commit()
        print("""Your card has been created
Your card number:""")
        print(get_number(x))
        print("Your card PIN:")
        print(get_pin(x))
        x += 1
    elif choice == 2:
        user_number = input("\nEnter your card number:")
        user_pin = input("Enter your PIN:")
        list_of_numbers = get_number("list")
        list_of_pin = get_pin("list")
        if (user_number not in list_of_numbers) or (user_pin not in list_of_pin):
            print("\nWrong card number or PIN!")
            continue
        elif (user_number in list_of_numbers) and (user_pin != list_of_pin[list_of_numbers.index(user_number)]):
            print("\nWrong card number or PIN!")
            continue
        else:
            print("\nYou have successfully logged in!")
            while log:
                choice_2 = input("""\n1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit\n""")
                if choice_2 == "1":
                    print("\nBalance: " + str(get_balance(user_number)))
                elif choice_2 == "2":
                    money = int(input("\nEnter income:"))
                    exe.execute(f"UPDATE card SET balance=balance+{money} WHERE number={user_number}")
                    conn.commit()
                    print("\nIncome was added!")
                elif choice_2 == "3":
                    transfer_card = input("\nTransfer\nEnter card number:")
                    if not check_luth(transfer_card):
                        print("Probably you made a mistake in the card number. Please try again!")
                        continue
                    elif transfer_card not in get_number("list"):
                        print("Such a card does not exist.")
                        continue
                    elif transfer_card == user_number:
                        print("You can't transfer money to the same account!")
                        continue
                    else:
                        transfer_money = int(input("\nEnter how much money you want to transfer:"))
                        if transfer_money > get_balance(user_number):
                            print("Not enough money!")
                            continue
                        else:
                            exe.execute(f"UPDATE card SET balance=balance-{transfer_money} WHERE number={user_number}")
                            conn.commit()
                            exe.execute(f"UPDATE card SET balance=balance+{transfer_money} WHERE number={transfer_card}")
                            conn.commit()
                            print("Success!")
                            continue
                elif choice_2 == "4":
                    exe.execute(f"DELETE FROM card WHERE number={user_number}")
                    conn.commit()
                    print("\nThe account has been closed!")
                    break
                elif choice_2 == "5":
                    print("\nYou have successfully logged out!")
                    break
                else:
                    print("\nBye!")
                    log = False
                    break
    else:
        print("\nBye!")
        break