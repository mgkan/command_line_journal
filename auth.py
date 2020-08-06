import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import sqlite3
import getpass
import pathlib

username = getpass.getuser()
database_path = pathlib.Path("/home/" + username + "/Documents/Command Line Journal/commandlinejournal.db")
app_key = "YOUR KEY"
app_secret = "YOUR SECRET"
auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
auth_url = auth_flow.start()
def oauth():
    print("Copy and paste the authorization code: ", auth_url)
    auth_code = input(": ").strip()

    oauth_result = auth_flow.finish(auth_code)

    dbx = dropbox.Dropbox(oauth2_access_token= oauth_result.access_token)
    token = dbx._oauth2_access_token
    dbx.users_get_current_account
    print("Dropbox login successful")
    con = sqlite3.connect(database_path)
    cursor = con.cursor()
    cursor.execute("INSERT INTO Auth values(?, ?)", (1, token))
    con.commit()

