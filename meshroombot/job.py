import os
import configparser
import subprocess
import re

#api
# job.Execute(settings)
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

class job:
    def __init__( self, jobSettings : dict, projectFolder : str ):
        self.jobSettings = jobSettings
        self.projectFolder = projectFolder

    # parse path and other settings in commands
    def SetSettingData( self, meshroom : str ):
        self.meshroom = meshroom

    # execute job with settings
    def Execute( self ):
        self.SetState( "computeState" )
        error = False
        os.makedirs(self.projectFolder + "/Meshroom", exist_ok=True)

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

    def SetState( self, state : str ):
        status = re.findall( r"(?<=\[)(.*?)(?=\])", os.path.basename(self.projectFolder))
        
        if( status == None or len( status ) == 0 ):
            # rename and update project folder
            os.rename( self.projectFolder, self.projectFolder + self.jobSettings[state] )
            self.projectFolder = self.projectFolder + self.jobSettings[state]
            return

        # rename and update project folder
        newdir = self.projectFolder.replace( "[" + status[0] + "]", self.jobSettings[state] )
        os.rename( self.projectFolder, newdir )
        self.projectFolder = newdir

    # parse command arguments template
    def ParseCommandArguments( self, cmd: str ) -> str:
        modulePath = os.path.abspath(os.path.dirname(__file__))

        return cmd.replace( "{folder}", self.projectFolder) \
            .replace( "{override}", modulePath + "/data.json" ) \
            .replace( "{meshroom}", self.meshroom )
        