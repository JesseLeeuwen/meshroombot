from .job import job
from .util import GetAllSubdirectories, CheckFolderStatus

# create way to poll a job

def GetJob(directory, jobTemplates : dict) -> job:

    folders = GetAllSubdirectories( directory )
    for folder in folders:
        status = CheckFolderStatus( folder, directory + "/" + folder )
        if status != "available":
            continue

        for key in jobTemplates:
            if jobTemplates[key]["accept"](directory + "/" + folder) == True:
                return job( jobTemplates[key], directory, folder )

    return None