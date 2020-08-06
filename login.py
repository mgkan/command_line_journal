import sqlite3
import pathlib
import getpass

username = getpass.getuser()
database_path = pathlib.Path("/home/" + username + "/Documents/Command Line Journal/commandlinejournal.db")

con = sqlite3.connect(database_path)
cursor = con.cursor()

def login():
    
    cursor.execute("Select password from User")
    password_list = cursor.fetchall()
    password = []
    for i in password_list:
        password.append(i[0])
        
    if password == []:
        set_password = input("Set password: ")
        cursor.execute("INSERT INTO User Values(?)", (set_password,))
        con.commit()
        print("Password set")
        cursor.execute("Select password from User")
        password_list = cursor.fetchall()
        password = []
        for i in password_list:
            password.append(i[0])
    
    password_input = input("Password(to reset type 'reset'): ")
    
    
    if password_input == 'reset':
        old_pass = input("Old password: ")
        if old_pass == password[0]:
            new_pass = input("New password: ")
            cursor.execute("Update User set password = ? where password = ?", (new_pass, old_pass))
            con.commit()
            print("Password set\n")
        elif old_pass != password[0]:
            print("Wrong password")
            quit()
    elif password[0] == password_input:
        print("Login successful\n")

    elif password_input != password[0]:
        print("Wrong password")
        quit()


