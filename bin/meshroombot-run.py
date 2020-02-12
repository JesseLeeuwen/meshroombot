#!/usr/bin/env python

from meshroombot.core import GetJob
import tkinter
import time # sleep
import os
import argparse
import configparser

from pathlib import Path
from tkinter import filedialog, messagebox

# parse arguments
parser = argparse.ArgumentParser(description='meshroom bot run script')
parser.add_argument("-c", "--conf", help="set custom path for conf file")
parser.add_argument("-d", "--dir",  help="the directory to run the meshroombot in")
args = parser.parse_args()

def SetConfigValue(config : configparser, setting : str):
    d = filedialog.askdirectory( title="Select " + setting + " path")
    if( d == "" ):
        return

    config["settings"][setting] = d

# create TK windows
root = tkinter.Tk()
root.withdraw()

# load settings
settingsPath = str(Path.home()) + "/.config/meshroombot/conf.ini"
if args.conf:
    settingsPath = args.conf
    if os.path.isfile( settingsPath ) == False:
        exit(1)

# create settings if missing
Config = configparser.ConfigParser()

if os.path.isfile( settingsPath ) == False:
    Config["settings"] = { "location" : "C:/"}
    SetConfigValue( Config, "meshroom" )
    
    os.makedirs(os.path.dirname(settingsPath), exist_ok=True)
    with open(settingsPath, 'w') as configfile:
        Config.write(configfile)
        configfile.close( )
else:
    Config.read( settingsPath )


# get target directory
if args.dir == None:
    directory = filedialog.askdirectory(initialdir = Config["settings"]["location"])
else:
    directory = args.dir

if directory == None or directory == "":
    answer = messagebox.askyesno("Continue?","invalid directory, do you want to use the previously used path?")
    if answer == False :
        exit(0)

    directory = Config["settings"]["location"]

# update config file
Config["settings"]["location"] = directory
with open(settingsPath, 'w') as configfile:
    Config.write(configfile)
    configfile.close( )

# template lib
jobTemplates = {
    "new scan" : {
        "commands" : [
            "cmd /C \"cd /D \"{meshroom}\" && meshroom_photogrammetry.exe --save \"{folder}/Meshroom/run.mg\" --input \"{folder}/Photo's/\" --cache \"{folder}/Meshroom/\" --overrides \"{override}\" \"",
            "cmd /C \"cd /D \"{meshroom}\" && meshroom_compute.exe \"{folder}/Meshroom/run.mg\" --forceStatus --toNode MeshFiltering --cache \"{folder}/Meshroom/\" \""
        ],
        "accept" : lambda a: ( not os.path.basename( a ).endswith(']') and os.path.isdir(a + "/Photo's") ),
        "computeState"  : "[-]",
        "doneState"     : "[+]",
        "error"         : "[!]"
    },
    "texturing" : {
        "commands" : [
            "cmd /C \"cd /D \"{meshroom}\" && meshroom_compute.exe \"{folder}/Meshroom/run.mg\" --forceStatus --toNode Texturing --cache \"{folder}/Meshroom/\" \""
        ],
        "accept" : lambda a: ( os.path.isfile(a +'/Meshroom/Zmesh.obj') and os.path.basename(a).endswith('[+]') ),
        "computeState"  : "[-]",
        "doneState "    : "[#]",
        "error"         : "[!!]"
    }
}

# start polling jobs on interval
try:
    while( True ):
        # get Job
        job = GetJob( directory, jobTemplates )
        
        if job is not None:
            job.SetSettingData( Config["settings"]["meshroom"] )
            print( job.projectFolder )
            job.Execute()

        time.sleep(2)
except KeyboardInterrupt:
    exit(0)