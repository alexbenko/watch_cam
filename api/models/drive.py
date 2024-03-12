from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFileList
import googleapiclient.errors
import os
#if you want to use this class, you need to set up some credentials. Follow these 2 links
# https://stackoverflow.com/questions/28184419/pydrive-invalid-client-secrets-file
# https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process/24542604#24542604
# and remember, both credential files need to be where this model is ran, not where the model file is
class G_Drive():
  def __init__(self, drive=None):
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # will open browser for you to sign into
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    self.drive = GoogleDrive(gauth)

  def create_folder(self, parent_folder_id, folder_name, ):
    folder_metadata = {
      'title': folder_name,
      'mimeType': 'application/vnd.google-apps.folder',
	  	'parents': [{"kind": "drive#fileLink", "id": parent_folder_id}]
    }

    folder = self.drive.CreateFile(folder_metadata)
    folder.Upload()

    return folder['id']
  def get_folder_id(self, parent_folder_id, folder_name):
    # Auto-iterate through all files in the parent folder.
    file_list = GoogleDriveFileList()
    try:
        file_list = self.drive.ListFile({'q': "'{0}' in parents and trashed=false".format(parent_folder_id)}).GetList()
    except googleapiclient.errors.HttpError as err:
      return None #Folder not found

    for file1 in file_list:
        if file1['title'] == folder_name:
            return file1['id']

  def back_up_recordings(self, folder_id, folder_location):
    #folder location should be the Path object from pathlib
    files = [str(folder_location)  + f'/{f}' for f in os.listdir(str(folder_location)) if f.endswith(".png")]

    for f in files:
      gfile = self.drive.CreateFile({'parents': [{'id': folder_id}]})
      gfile.SetContentFile(f)
      gfile.Upload()
    print("!!!!!!!DONE BACKING UP FOLDER: ", folder_location)