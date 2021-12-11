#!/bin/sh
#PBS -M naofuji.1220@gmail.com
#PBS -m be
#PBS -l nodes=1:ppn=20

cd $PBS_O_WORKDIR

source /opt/intel/bin/compilervars.sh -arch intel64 -platform linux
PATH=/opt/openmpi/bin:$PATH
PATH=/opt/intel/compilers_and_libraries/linux/bin/intel64:$PATH
LD_LIBRARY_PATH=/opt/openmpi/lib:$LD_LIBRARY_PATH
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/compilers_and_libraries/linux/lib/intel64
MANPATH=/opt/openmpi/share/man:$MANPATH
export PATH LD_LIBRARY_PATH MANPATH

# 20プロセス並列
python3 generate.py
mpirun -np 20 /home/Fujita388/github/lammps/src/lmp_mpi < single.input
python3 minimize.py > minimize.atoms
mpirun -np 20 /home/Fujita388/github/lammps/src/lmp_mpi < minimize.input
python3 surfactant.py > surfactant.atoms
mpirun -np 20 /home/Fujita388/github/lammps/src/lmp_mpi < surfactant.input
