import os
import argparse
import json
import re

parser = argparse.ArgumentParser( 
    description='script to override options within a meshroom project file without limitations')
parser.add_argument("project", type=str, help="Project file to fix")
parser.add_argument("json",  type=str, help="Settings to paste into project")
parser.add_argument("--meshroom", type=str, help="path to meshroom")
args = parser.parse_args()

project = json.load( open( args.project, "r" ) )
overrides = json.load( open( args.json, "r") )

for node in project["graph"]:

    if args.meshroom != None:                    
        for inputOption in project["graph"][node]["inputs"]:
                if re.match( r"([A-Z]:(\/|\\).*)", str(project["graph"][node]["inputs"][inputOption])):
                    project["graph"][node]["inputs"][inputOption] = re.sub(
                        r"([A-Z]:(\/|\\).*?)\/aliceVision\/", 
                        args.meshroom + "aliceVision/", project["graph"][node]["inputs"][inputOption])

    if node in overrides:
        for option in overrides[node]:
            if type( project["graph"][node]["inputs"][option] ) is str:
                project["graph"][node]["inputs"][option] = overrides[node][option].replace(
                    "{project}", os.path.dirname( args.project ))
            else:
                project["graph"][node]["inputs"][option] = overrides[node][option]

f = open(args.project, "w")
f.write(json.dumps(project, indent=4, sort_keys=False))
f.close()