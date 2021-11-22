#!/bin/sh
#PBS -l nodes=1:ppn=20

cd $PBS_O_WORKDIR

# 20プロセス並列
python3 generate.py
mpirun -np 20 /home/Fujita388/github/lammps/src/lmp_mpi < single.input
python3 minimize.py > minimize.atoms
mpirun -np 20 /home/Fujita388/github/lammps/src/lmp_mpi < minimize.input
python3 surfactant.py > surfactant.atoms
mpirun -np 20 /home/Fujita388/github/lammps/src/lmp_mpi < surfactant.input
