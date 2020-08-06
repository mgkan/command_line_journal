import pathlib
import getpass
username = getpass.getuser()
mkdir_path = pathlib.Path("/home/" + username + "/Documents/Command Line Journal")
import os
try:
    os.mkdir(mkdir_path)
except FileExistsError:
    pass
import auth
import data
import sqlite3
import datetime
from datetime import datetime
import text_store
import dropbox
import login
import time

date = datetime.strftime(datetime.now(), "%D")
database_path = pathlib.Path("/home/" + username + "/Documents/Command Line Journal/commandlinejournal.db")

data.tablo()
con = sqlite3.connect(database_path)
cursor = con.cursor()

text_store.text_table()

cursor.execute("Select authorized from Auth")
liste = cursor.fetchall()
if liste != [(1,)]:
    try:
        auth.oauth()
    except:
        print("### -PLEASE TRY AGAIN- ###\n")
        quit()
elif liste == [(1,)]:
    print("Dropbox login successful\n")

token = []
cursor.execute("Select access_token from Auth")
token_list = cursor.fetchall()
for token_tuple in token_list:
    token.append(token_tuple[0])
dbx = dropbox.Dropbox(token[0])

try:
    dbx_metadata = dbx.files_get_metadata("/commandlinejournal.db")
except:
    with open(database_path, "rb") as f:
        dbx.files_upload(f.read(), "/commandlinejournal.db", mode=dropbox.files.WriteMode("overwrite"))

utcdate = datetime.utcnow()
cdate = datetime.strftime(utcdate, "%Y-%m-%d %H:%M")

cursor.execute("CREATE TABLE IF NOT EXISTS ctime (created_time TEXT)")
cursor.execute("INSERT INTO ctime Values(?)", (cdate,))
con.commit()

dbx_metadata = dbx.files_get_metadata("/commandlinejournal.db")
dbx_date = dbx_metadata.client_modified
dbx_time = datetime.strftime(dbx_date, '%Y-%m-%d %H:%M')

modTimesinceEpoc = os.path.getmtime(database_path)
utc_local_time = datetime.utcfromtimestamp(modTimesinceEpoc).strftime('%Y-%m-%d %H:%M')

cursor.execute("Select created_time from ctime")
timee = cursor.fetchall()
timestr = []
for i in timee:
    timestr.append(i[0])
cutctime = datetime.strptime(timestr[0],'%Y-%m-%d %H:%M')
cutctime_f = cutctime.strftime('%Y-%m-%d %H:%M')
print("Dropbox last sync date (UTC): ", dbx_time)

sync_check = dbx_time > utc_local_time
first_time_check = cutctime_f == utc_local_time
#print("there is a newer database in your dropbox: ", sync_check, "\n")
if cutctime_f == utc_local_time == dbx_time:
    pass
elif first_time_check == True:
    try:
        dbx.files_download_to_file(database_path, "/commandlinejournal.db")
        print("-Synced from dropbox- (your password is also being synced from dropbox)\n")
    except:
        pass
elif sync_check == True:
    dbx.files_download_to_file(database_path, "/commandlinejournal.db", )
    print("-Synced from dropbox- (your password is also being synced from dropbox)\n")

login.login()

def view_todays_entry():
    
    cursor.execute("SELECT * from text_store where date = ?", (date,))
    today = cursor.fetchall()
    for i in today:
        print("################ ", i[1]," - ",i[0], " ################", "\n")
    for i in today:
        print(i[2])
    if today == []:
        print("title for today's entry: ")
        title = input()
        text_store.text_data(date, title, '')
        print("today's entry is created\n")
        print("################ ", title," - ",date, " ################", "\n")
cursor.execute("SELECT text from text_store where date = ?", (date,))
today = cursor.fetchall()
old_text = []

view_todays_entry()
text_input = input()
if today != []:
    for i in today:
        old_text.append(i[0])
    final_text = (old_text[0] + " " + text_input)
else:
    final_text = (text_input)
text_store.text_update(final_text, date,)
try:
    with open(database_path, "rb") as f:
            dbx.files_upload(f.read(), "/commandlinejournal.db", mode=dropbox.files.WriteMode("overwrite"))
            print("\n-Synced to dropbox, You can exit now-")
except:
    print("Couldn't sync with dropbox. Please check your internet connection and restart the app.")
