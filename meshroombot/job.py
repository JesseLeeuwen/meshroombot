import os
import configparser
import subprocess
import re
import sys

#api
# job.Execute()

# commands can contain these variables:
# {folderName} the name of the projectFolder (Bollard_01)
# {folder} the directory of the scans which is being processed
# {meshroom} the directory of meshroom ( set in conf.ini )
# {override} the path of the override/ settings json


# "template_name" : {
#     "commands" : [
#         "cmd command to run for this job", 
#     ],
#     "accept" : lambda(path) which checks if the given pass has all the requirements for this job,
#     "computeState"  : "suffix to give the folder when computing default: [-]",
#     "doneState"     : "suffix to give when the job was finished succesfully",
#     "error"         : "suffix for when the job was finisched with an error [!]"
# },


class job:
    def __init__( self, jobSettings : dict, directory : str, projectFolder : str ):
        self.jobSettings = jobSettings
        self.projectFolder = directory + "/" +projectFolder
        self.projectFolderName = projectFolder
        self.projectFolderDir = directory

    # parse path and other settings in commands
    def SetSettingData( self, meshroom : str ):
        self.meshroom = meshroom

    # execute job with settings
    def Execute( self ):
        try:
            self.SetState( "computeState" )
            error = False

            for cmd in self.jobSettings["commands"]:
                cmd_compiled = self.ParseCommandArguments( cmd )
                print( "run: " + cmd_compiled )
                # check for error
                if subprocess.call( cmd_compiled ) > 0:
                    error = True
                    break

            if not error:
                self.SetState( "doneState" )            
            else:
                self.SetState( "error" )

            print( "job complete" )
        except Exception as e:
            print( "error while performing a job on: {0}".format(self.projectFolderName), str(e) )

    def SetState( self, state : str ):
        folderName = re.sub( r"(\[.*\])", "", self.projectFolderName )
        newDir = self.projectFolderDir + "/" + folderName + self.jobSettings[state]
        os.rename( self.projectFolder, newDir )
        self.projectFolder = newDir

    # parse command arguments template
    def ParseCommandArguments( self, cmd: str ) -> str:
        modulePath = os.path.abspath(os.path.dirname(__file__))

        return cmd.replace( "{folder}", self.projectFolder) \
            .replace( "{override}", modulePath + "/data.json" ) \
            .replace( "{meshroom}", self.meshroom ) \
            .replace( "{folderName}", re.sub( r"(\[.*\])", "", self.projectFolderName ) )
         