#!/bin/sh

#SBATCH -p i8cpu
#SBATCH -N 1
#SBATCH -n 100
#SBATCH -c 1
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=naofuji.1220@gmail.com

source /home/issp/materiapps/intel/lammps/lammpsvars.sh

python3 generate.py
srun lammps < single.input
python3 minimize.py > minimize.atoms
srun lammps < minimize.input
python3 surfactant.py > surfactant.atoms
srun lammps < surfactant.input
