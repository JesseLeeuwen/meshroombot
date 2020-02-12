# program Design
# get available meshroombot Job
    # search in scan directory for the first available folder
        # check with rename
        # folder name indicated status
        #     available
        # [-] busy
        # [#] done
    # search in [#] scans for Meshroom/mesh.obj
        # (texture phase)

# process Job
    # new scans
        # create meshroom room .mg file
        # run toNode MeshFiltering
    # Texturing
        # set mesh.obj as Texture inputMesh
