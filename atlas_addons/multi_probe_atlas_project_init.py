import shutil
import sys
import os

#===============
#
# File: multi_probe_atlas_project_init.py
# Version: 1.0, 08-22-22
# Usage (cmd): python  multi_probe_atlas_project_init.py
# Description: Creates a project folder and populates it with the pdbs in pdb_input along with designated templates with which to run atlas
#
# Authors: Caleb Weber, Oleksandr Savytskyi, Ph.D, Thomas Caulfield, Ph.D
# CAULFIELD LABORATORY, PROPERTY OF MAYO CLINIC
# https://www.mayo.edu/research/labs/drug-discovery-design-optimization-novel-therapeutics-therapeutics
#
#===============

# The name of the project as a whole
main_project_folder_name = '1ubq'
# Which probe versions you would like to utilize
probe_versions = ['V1', 'V2']
# From the templates folder, which run templates would you like to use for each probe?
v1_template = 'run_template_atlas_probes_V1.py'
v2_template = 'run_template_atlas_probes_V2.py'
templates = [v1_template, v2_template]

#Choose from the following options:
# - sequential: runs each atlas simulation in order
# - pairwise: runs v1/v2 simulations in parallel, with the variable pdbs in sequence
# - parallel: runs all simulations at once
run_style = 'pairwise'

# Prior to running, place all PDBs you wish to be analyzed in the pdb_input folder.
# These will be copied and placed in folders created within your project folder so that they may be examined.

if __name__ == "__main__":
    print("Creating atlas- project folder for "+main_project_folder_name+"...")
    main_path = '../atlas_projects/'
    project_folder = main_path+main_project_folder_name+"/"
    paths = [main_path, project_folder]
    pdbs = os.listdir('pdb_input/')
    pdbs = [x for x in pdbs if '.pdb' in x]
    subfolder_names = [x.split('.')[0] for x in pdbs]
    for subfolder_name in subfolder_names:
        subfolder = project_folder+subfolder_name+"/"
        paths.append(subfolder)
        for probe_version in probe_versions:
            subfolder_vx_output = subfolder+subfolder_name+"_"+probe_version+"_output/"
            paths.append(subfolder_vx_output)

    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
    subfolder_run_files = []
    for pdb in pdbs:
        subfolder_name = pdb.split('.')[0]
        subfolder_path = project_folder+subfolder_name+"/"
        shutil.copy('pdb_input/'+pdb, subfolder_path+pdb)
        pair = []
        for template_name in templates:
            template = 'templates/'+template_name
            run_template = open(template, "r")
            run_template_txt = run_template.read()
            run_txt = run_template_txt.replace('RECEPTOR.pdb', pdb)
            run_txt = run_txt.replace('ATLAS_PATH', '../../atlas_package/bin')

            subfolder_template_name = template_name.replace('template', subfolder_name)
            subfolder_run_file = subfolder_path+subfolder_template_name
            subproject_run = open(subfolder_run_file, "w")
            subproject_run.write(run_txt)
            subfolder_file_path = subfolder_run_file.split('/')[-2]+'/'+subfolder_run_file.split('/')[-1]
            pair.append(subfolder_file_path)

            run_template.close()
            subproject_run.close()

        if run_style == 'pairwise':
            subfolder_run_files.append(pair)
        else:
            for file in pair:
                subfolder_run_files.append(file)

    run_all_template_name = 'templates/run_all_template_'+run_style+'.py'
    run_all_template = open(run_all_template_name, "r")
    run_all_template_txt = run_all_template.read()
    run_all_txt = run_all_template_txt.replace('SUBPROCESS_LIST', str(subfolder_run_files))
    project_run = open(project_folder+'run_all_'+main_project_folder_name+"_"+run_style+'.py', "w")
    project_run.write(run_all_txt)
    project_run.close()

    print(main_project_folder_name+" creation complete!")


