all: 

temp_press:
	python3 temp_press.py > temp_press.dat

clean: 
	$(RM) *.lammpstrj *.atoms *.out *.lammps
