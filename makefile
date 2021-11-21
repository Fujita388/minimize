all: 

single:
	python3 generate.py
	/home/Fujita388/github/lammps/src/lmp_serial < single.input

minimize: 
	python3 minimize.py > minimize.atoms
	/home/Fujita388/github/lammps/src/lmp_serial < minimize.input

surfactant:
	python3 surfactant.py > surfactant.atoms
	/home/Fujita388/github/lammps/src/lmp_serial < surfactant.input

volume:
	g++ -c -std=c++11 main.cpp split.cpp
	g++ -std=c++11 main.o split.o

temp_press:
	python3 temp_press.py > temp_press.dat

clean: 
	rm *.lammpstrj *.atoms *.png *.o a.out
