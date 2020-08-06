import sqlite3
import getpass
import pathlib

username = getpass.getuser()

database_path = pathlib.Path("/home/" + username + "/Documents/Command Line Journal/commandlinejournal.db")
con = sqlite3.connect(database_path)
cursor = con.cursor()

def tablo():
    cursor.execute("CREATE TABLE IF NOT EXISTS Auth (authorized BOOLEAN, access_token TEXT)")
    con.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS User (password TEXT)")
    con.commit()
    