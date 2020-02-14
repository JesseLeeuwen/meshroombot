import os

def GetAllSubdirectories( path : str ):
    # loop through all sub directories
    # combine path and sub directory name to check wether the path is a valid directory
    return [name for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))]

def CheckFolderStatus( folderName: str, path: str ) -> str:    
    try:
        # check if folder is locked
        os.rename(path, path+ "2")
        os.rename(path+"2", path)
        return "available"
    except:
        return "error" 