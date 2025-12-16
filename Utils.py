import pandas as pd
from tabulate import tabulate
import arabic_reshaper
from bidi.algorithm import get_display

import sys
sys.stdout.reconfigure(encoding='utf-8')

brands = [
    "ایسوس",
    "لنوو",
    "اپل",
    "اچ پی",
    "مایکروسافت",
    "ایسر",
    "هواوی",
    "دل",
    "ام اس آی",
    "سامسونگ",
    "شیائومی",
    "ریزر",
    "سونی",
    "فوجیتسو",
    "آنر",
    "ال جی",
    "آی لایف",
    "گیگابایت",
    "گوگل",
    "توشیبا",
    "اینتل",
    "ایکس ویژن",
    "ایکس پی جی"
]

# Function to reshape and apply bidi transformation
def process_rtl_text(text):
    if isinstance(text, str):  # Only process strings
        reshaped_text = arabic_reshaper.reshape(text)  # Reshape text
        return get_display(reshaped_text)  # Apply bidi transformation
    return text 


def load_products():
    products = pd.read_csv("data/products.csv")
    df_processed = products.applymap(process_rtl_text)
    print(tabulate(df_processed, 
               headers="keys", tablefmt="heavy_grid"))
    
    return products



def load_user_pass():
    userPass = pd.read_csv("data/userPass.csv")
    savedUsers = userPass["user"].values.tolist()
    savedPass = userPass["pass"].values.tolist()
    dict_user = {}
    for i in range(len(savedUsers)):
        dict_user[proc_user([savedUsers[i]])[0]] = savedPass[i]
    return dict_user, savedUsers, savedPass


def save_user_pass(dict_user):
    users = [], passwords = []

    for user in dict_user:
        users.append(user)
        passwords.append(dict_user[user]
                         )
    newUsers = {'user': users, 'pass': passwords}
    #create DataFrame
    df = pd.DataFrame(newUsers)
    df.to_csv('data/userPass.csv')




def proc_user(users):
    users = [i.lower() for i in users]
    return users
    
def contains_a_to_z(input_string):
    for char in input_string:
        if 'a' <= char <= 'z':
            return True
    return False



def get_user_pass():
    user = input("\nPlease Enter Username: \n")
    password = input("\nPlease Enter Password: \n")
    return user, password




def create_accunt():
    dict_user, savedUsers, savedPass = load_user_pass()
    procSavedUsers = proc_user(savedUsers)

    user, password = get_user_pass()

    procUser = proc_user([user])[0]
    counter = 0
    if procUser in procSavedUsers or not contains_a_to_z(password):
        while counter < 3:
            if procUser in procSavedUsers and counter == 0:
                print("\n=====================================================\n\nError------> This user exists, Please Use another username....\n\n")

            if not contains_a_to_z(password) and counter == 0:
                print("\n=====================================================\n\nError------>The password should contains at least one character from a to z...")
            
            user, password = get_user_pass()
            procUser = proc_user([user])[0]

            counter = counter + 1

            if procUser in procSavedUsers:
                continue
            else:
                if contains_a_to_z(password):
                    dict_user[user] = password 
                    save_user_pass(dict_user)
                    break
                else:
                    print("\n=====================================================\n\nError------>The password should contains at least one character from a to z...")
                    continue

    else:
        dict_user[user] = password
        save_user_pass(dict_user)



    if counter < 3:
        print("\nYour accunt created....\n\n please Sign in to continue\n\n")
        sign_in_menu()
    else:
        print("\nYou are blocked, please try later....")
        exit(1)




def sign_in(user, password):
    dict_user, savedUsers, savedPass = load_user_pass()
    procSavedUsers = proc_user(savedUsers)


    procUser = proc_user([user])[0]
    counter = 0


    if procUser in procSavedUsers and password == dict_user[procUser]:
        print("\n\n***   You entered   ***\n\n")
        products = load_products()
    
    else:
        while counter < 3:

            print("\n===================================================== \n\nError------> The username or password is wrong, Please try again....\n\n")
            user, password = get_user_pass()
            procUser = proc_user([user])[0]

            counter = counter + 1

            if procUser in procSavedUsers and password == dict_user[procUser]:
                print("\n\n***   You entered   ***\n\n")
                load_products()
                break
            elif counter >= 3:
                print("\nYou are blocked, please try later....")
                exit(1)
            else:
                continue





def sign_in_menu():
    user_input = input(" =====================================================\n                          Main Menu\n =====================================================\n 1.Sign in \n 2.Exit \n =====================================================\n")
    #user_input =2

    user_input = int(user_input)

    if user_input==1:
        user, password = get_user_pass()
        sign_in(user, password)
    else:
        exit(1)




def display_menu():
    user_input = input(" =====================================================\n                          Main Menu\n =====================================================\n 1.Sign in \n 2.Sign up \n 3.Exit \n =====================================================\n")
    #user_input =2

    user_input = int(user_input)

    if user_input==1:
        user, password = get_user_pass()
        sign_in(user, password)
    elif user_input==2:
        create_accunt()
    else:
        exit(1)




