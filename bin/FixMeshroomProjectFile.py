import os
import argparse
import json

parser = argparse.ArgumentParser(description='script to override options within a meshroom project file without limitations')
parser.add_argument("project", type=str, help="Project file to fix")
parser.add_argument("json",  type=str, help="Settings to paste into project")
args = parser.parse_args()

project = json.load( open( args.project, "r" ) )
overrides = json.load( open( args.json, "r") )

for node in project["graph"]:
   if node in overrides:
       for option in overrides[node]:
           project["graph"][node]["inputs"][option] = overrides[node][option]

f = open(args.project, "w")
f.write(json.dumps(project, indent=4, sort_keys=False))
f.close()