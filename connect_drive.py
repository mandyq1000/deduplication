from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def upload_transcript(filename):
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
    # fileList = drive.ListFile({'q': "'1V9y5Rvq3vAF3qaM16-bDhpgbo_7woue3' in parents and trashed=false"}).GetList()
    # for file in fileList:
    #     print('Title: %s, ID: %s' % (file['title'], file['id']))
    #     # Get the folder ID that you want
    #     if (file['title'] == "transcripts"):
    #         fileID = file['id']

    file1 = drive.CreateFile({"mimeType": "text/txt", "parents": [{"kind": "drive#fileLink", "id": "1B99EQSA1IMgdxuCIbHPh6Uz9O0cB36nE"}]})
    file1.SetContentFile(filename)
    file1.Upload()  # Upload the file.
    print('Created file %s with mimeType %s' % (file1['title'], file1['mimeType']))


def upload_summary(filename):
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
    # fileList2 = drive.ListFile({'q': "'1-vtjs8c0AVQexDPgoOaazleO6poP84xi' in parents and trashed=false"}).GetList()
    # for file in fileList2:
    #     print('Title: %s, ID: %s' % (file['title'], file['id']))
    #     # Get the folder ID that you want
    #     if (file['title'] == "summary"):
    #         fileID2 = file['id']

    file2 = drive.CreateFile({"mimeType": "text/txt", "parents": [{"kind": "drive#fileLink", "id": "1-vtjs8c0AVQexDPgoOaazleO6poP84xi"}]})
    file2.SetContentFile(filename)
    file2.Upload()  # Upload the file.
    print('Created file %s with mimeType %s' % (file2['title'], file2['mimeType']))


def upload_video(filename):
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
    # fileList3 = drive.ListFile({'q': "'1ip2ICs3-r_bZHOBEDIUtV0jbgMNnGjqy' in parents and trashed=false"}).GetList()
    # for file in fileList3:
    #     print('Title: %s, ID: %s' % (file['title'], file['id']))
    #     # Get the folder ID that you want
    #     if (file['title'] == "videos"):
    #         fileID3 = file['id']

    file3 = drive.CreateFile(
        {"mimeType": "video/mp4", "parents": [{"kind": "drive#fileLink", "id": "1ip2ICs3-r_bZHOBEDIUtV0jbgMNnGjqy"}]})
    file3.SetContentFile(filename)
    file3.Upload()  # Upload the file.
    print('Created file %s with mimeType %s' % (file3['title'], file3['mimeType']))
