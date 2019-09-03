# -*- coding: utf-8 -*-

import math
import os
from subprocess import Popen

''' We can write a file too with the desired results '''


SALOME_ROOT='/INSTALLABLES/salome_meca-2017/appli_V2017.0.2/salome' #root folder for salome
ASTER_ROOT='/INSTALLABLES/aster' #root folder for asterstudy
WORKING_DIR='/home/u1449908/Salome_files/AUTO_FIBER' #Working directory
ASTER_VERSION='2017.0.2' #I dont think if its needed
#MESH_NAME='hex_mesh.med' #Mesh file name
#COMM_FILE='hex_new.comm' #.comm file - this file has all the details to 

salome_run = Popen(SALOME_ROOT + ' -t ' + WORKING_DIR + '/salome_geometry.py', shell='TRUE') # This will run the python sript from salome_meca
salome_run.wait() 

'''The input/output files are defined as follow: the first letter “F” means we are dealing with a file
(it is possible to define a directory as “D”), then the type of file (comm or mmed …), then the file name (or directory name),
then the letter “D” means data (or “R” means result), and finally the number at the end of a line correspond to the Fortran unit.

P means parameters of execution'''

###CREATING THE .export file
##exportfile = os.path.join(WORKING_DIR,'hex_new.export') 
##e = open(exportfile,'w')
##e.write('P actions make_etude\n') #it means to make aster run study actions
##e.write('P memjob 4096\n') #memory used in job in MB
##e.write('P memory_limit 4096.0\n')  # Memory for Aster computation in MB
##e.write('P mode interactif\n') # mode interactive
##e.write('P mpi_nbcpu 1\n') # number of processors for parallelism
##e.write('P mpi_nbnoeud 1\n') # number of nodes for parallelism
##e.write('P ncpus 1\n') 
##e.write('P platform LINUX64\n') # platform that we are going to use
##e.write('P proxy_dir /tmp\n') # Directory to store temporary files
##e.write('P rep_trav /tmp/case1\n') #Name of the repository of work
##e.write('P origine AsterStudy ' + ASTER_VERSION + '\n') # Name of the application having generated the file .export 
##e.write('P version stable\n') #version of aster
##e.write('A args\n')
##e.write('A memjeveux 512.0\n') # Size of the memory taken by the execution (in MB). memjeveux = Total memory / 8
##e.write('A tpmax 900\n') # Limit of the time of the execution (in seconds)
##e.write('F mmed '+ WORKING_DIR + '/' + MESH_NAME + ' D 20\n') #DATA - input mesh
##e.write('F comm '+ WORKING_DIR + '/' + COMM_FILE + ' D  1\n') #DATA - command file
##e.write('F rmed '+ WORKING_DIR + '/hex.rmed R  80\n') #Result - rmed file
##e.write('F mess '+ WORKING_DIR + '/hex.mess R  6\n') #Result - output message
##e.close()
##
##aster_run = Popen(ASTER_ROOT + '/bin/as_run ' + WORKING_DIR + '/hex_new.export', shell='TRUE') # aster should run the analysis
##aster_run.wait()
