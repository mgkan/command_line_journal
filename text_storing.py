import pathlib
import getpass
from datetime import datetime
import sqlite3

username = getpass.getuser()
database_path = pathlib.Path("/home/" + username + "/Documents/Command Line Journal/commandlinejournal.db" )
con = sqlite3.connect(database_path)
cursor = con.cursor()

def text_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS text_store (date TEXT, text_title TEXT, text TEXT)")
    con.commit()


def text_data(date, title, text):
    cursor.execute("CREATE TABLE IF NOT EXISTS text_store (date TEXT, text_title TEXT, text TEXT)")
    con.commit()
    cursor.execute("INSERT INTO text_store Values(?, ?, ?)", (date, title, text))
    con.commit()

def text_update(text, date):
    cursor.execute("Update text_store set text = ? where date = ?", (text, date))
    con.commit()