from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Authentication

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


# Methods for various API Calls

glob_file_path = "root"
current_folder_id = "null"

# queries ENTIRE Drive (shared and personal) for filename, downloads into specified filepath
# potential conflict if multiple files have same filename 
def downloadFile(file_name):
  file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(current_folder_id)}).GetList()
  download_path = input("Enter the file path for the download location: ")
  for file1 in file_list:
    if file1['title'] == file_name:
      file2 = drive.CreateFile({'id': file1['id']})
      print('Downloading file %s from Google Drive' % file2['title']) 
      full_path = download_path + "/" + file_name
      file2.GetContentFile(full_path)  # Save Drive file as a local file


# searches folder by name and returns folder ID
def getFolderID(folder_name):
  file_list = drive.ListFile({'q': 'trashed=false'}).GetList()
  for files in file_list:
    if files['title'] == folder_name:
      return files['id']


# returns contents inside a given folder, query uses folderID
def getFolderContents(folder):
  folder_id = getFolderID(folder)
  file_list = drive.ListFile({'q': "'{}' in parents".format(folder_id)}).GetList()
  return file_list

# helper function for file navigation
def navHelper(parent, child):
  for i in parent:
    if i['title'] == child:
      return True
  return False

# prints the content of a given file path
def filePathNav(file_path):
  folder_list = file_path.split("/")
  if(len(folder_list) == 1): # if only only folder is queried 
    res = getFolderContents(folder_list[0])
    for files in res:
      print('title: %s, id: %s' % (files['title'], files['id']))
    return
  i = 0     
  while(i < len(folder_list) - 1):
    parent = getFolderContents(folder_list[i])
    isChild = navHelper(parent, folder_list[i+1])
    if(isChild == True):
      i+=1
    else: # folder does not exist in parent
      print("folder not found")
      return
  if(isChild == True):
    res = getFolderContents(folder_list[i])
    global current_folder_id
    global glob_file_path
    glob_file_path = file_path
    current_folder_id = getFolderID(folder_list[i])
    for files in res:
      print(file_path + '/%s, id: %s' % (files['title'], files['id']))


