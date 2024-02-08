import os
import shutil
import zipfile

def create_directories(directory):  # check if  dir already exists
    dirs=["psd", "image", "pdf" , "ai" , "txt" , "unsorted"]
    for d in dirs :
        dir_path = os.path.join( directory , d )
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"created {d} directory")


def extract_zip_files(directory, extractedlist):  # extract zip files in found before organizing
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_file_path = os.path.join(directory, filename)
            extractedlist.append(zip_file_path)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
            print(f"Extracted {filename} in {directory}")


def delete_zip(extractedlist): # delete extracted zip files
    i = 0
    for zip in extractedlist:
        try:
            os.remove(zip)
            i += 1
        except:
            print("error while deleting", zip)
    print(i, " zip files Deleted out of ", len(extractedlist))


def organize_files(directory):  # organize files in main and all directories and manage existing files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            targeted_dir = ""
            sourcefile = ""
            if filename.endswith(".psd"):
                targeted_dir = os.path.join(directory,"psd")
            elif filename.endswith((".jpg", ".jpeg", ".png")):
                targeted_dir = os.path.join(directory,"image")
            elif filename.endswith(".pdf"):
                targeted_dir = os.path.join(directory,"pdf")
            elif filename.endswith(".ai") or filename.endswith(".eps") :
                targeted_dir = os.path.join(directory,"ai")
            elif filename.endswith(".txt") :
                targeted_dir = os.path.join(directory,"txt")
            else:
                targeted_dir= os.path.join(directory,"unsorted")
                #print(f"Ignored {filename}.")
            if targeted_dir:
                sourcefile = os.path.join(root, filename)
                try:
                    shutil.move(sourcefile, targeted_dir)
                except:
                    print(f"{filename} moved to {targeted_dir}")
def delete_url_files (directory) :
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".url"):
                filepath = os.path.join(root,file)
                os.remove(filepath)
                print(f"deleted {file}")



def delete_empty_folders(directory):  # delete remaining empty folders
    for root, dirs, files in os.walk(directory, topdown=False):  # topdown = false : visiting subdir before root
        for dir_name in dirs:
            if dir_name not in ["psd", "pdf", "image" , "ai" , "txt" , "unsorted"]: # making sure this won't delete our directories
                dir_path = os.path.join(root,dir_name)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                try :
                    if os.listdir(dir_path) :
                        print(f"the folder {dir_name} is not empty do u Want to delete it ? y/n")
                        resp = str(input())
                        response= resp.lower()
                        if response == "y" :
                            shutil.rmtree(dir_path,ignore_errors=True)
                except :
                    pass
                print(f"Deleted folder: {dir_name}")
#directory = "folderexample"
directory = str(input("enter Directory path"))
list = []
create_directories(directory)
extract_zip_files(directory, list)
delete_zip(list)
organize_files(directory)
delete_empty_folders(directory)
delete_url_files(directory)
