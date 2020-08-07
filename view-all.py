import getpass
import sqlite3
import pathlib
import login

login.login()

username = getpass.getuser()
database_path = pathlib.Path("/home/" + username + "/Documents/Command Line Journal/commandlinejournal.db")
con = sqlite3.connect(database_path)
cursor = con.cursor()

def view_all():
    try:
        cursor.execute("SELECT * from text_store")
        all_entries = cursor.fetchall()
        for i in all_entries:
            print("############", i[1], "-", i[0], "############\n","\n", i[2], "\n")
    except:
        print("Sorry can't find any entries now, please try again later")
view_all()
