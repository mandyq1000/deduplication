from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def list_files(filename):
    # gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()  # client_secrets.json need to be in the same directory as the script
    # drive = GoogleDrive(gauth)
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    fileList = drive.ListFile({'q': "'1V9y5Rvq3vAF3qaM16-bDhpgbo_7woue3' in parents and trashed=false"}).GetList()
    for file in fileList:
        print('Title: %s, ID: %s' % (file['title'], file['id']))
        # Get the folder ID that you want
        if (file['title'] == "transcripts"):
            fileID = file['id']

    file1 = drive.CreateFile({"mimeType": "text/txt", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
    file1.SetContentFile(filename)
    file1.Upload()  # Upload the file.
    print('Created file %s with mimeType %s' % (file1['title'], file1['mimeType']))
