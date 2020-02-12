import os
import re

statusLookup = { 
    "-": "processing", 
    "+": "available", # check content "/Meshroom/Zmesh.obj" before passing to Texturing
    "#": "texture done",
    "!": "error"
}

def GetAllSubdirectories( path : str ):
    # loop through all sub directories
    # combine path and sub directory name to check wether the path is a valid directory
    return [name for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))]

def CheckFolderStatus( folderName: str, path: str ) -> str:    
    status = re.findall( r"(?<=\[)(.*?)(?=\])", folderName)
    
    try:
        # check if folder is locked
        os.rename( path, path )

        if( status == None or len( status ) == 0 ):
            return "available"
    except:
        return "error"
    
    return statusLookup[ status[0] ]