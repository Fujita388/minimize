# 構造緩和した後の粒子を読み込んでリスケール

def rescale(atoms_file, dump_file, scale):
	#atomsのファイルを読み込み
	with open(atoms_file, "r") as f:
		atoms_data = f.readlines()
	#dumpファイルを読み込み
	with open(dump_file, "r") as f:
		dump_data = f.readlines()
	group = []  #ダンプファイルにおけるグループの始まりのインデックスの配列
	for i, line in enumerate(dump_data):
		if "ITEM: TIMESTEP" in line:
			group.append(i)
	num_atoms = int(dump_data[3])  #atomの数
	l = dump_data[group[-1]+5]  
	L = float(l.split()[1])  #シミュレーションボックスのサイズ
	mol_list = [0 for i in range(num_atoms)]  #mol_idのリスト(mol_idをatoms_idに紐づける)
	for i in range(num_atoms):
		atoms_id  = int(atoms_data[i+14].split()[0])
		mol_id  = atoms_data[i+14].split()[1]
		mol_list[atoms_id-1] = mol_id
	print("Position Data\n")
	print(str(num_atoms) + " atoms")
	print(atoms_data[3])
	print("3 atom types")
	print("1 bond types\n")
	print("0.00 " + str(scale*L) + " xlo xhi")
	print("0.00 " + str(scale*L) + " ylo yhi")
	print("0.00 " + str(scale*L) + " zlo zhi\n")
	print("Atoms\n")
	for i in range(num_atoms):
		position = dump_data[group[-1]+9+i]  #最後のグループの座標dataの先頭
		atoms_id = int(position.split()[0])
		atoms_type = int(position.split()[1])
		x = float(position.split()[2]) * scale
		y = float(position.split()[3]) * scale
		z = float(position.split()[4]) * scale
		print(atoms_id, mol_list[atoms_id-1], atoms_type, x, y, z)
	print("\n")
	print("Velocities\n")
	for i in range(num_atoms):
		position = dump_data[group[-1]+9+i]  #最後のグループの座標dataの先頭
		atoms_id = int(position.split()[0])
		vx = float(position.split()[5])
		vy = float(position.split()[6])
		vz = float(position.split()[7])
		print(atoms_id, vx, vy, vz)
	print('\n')
	for i, line in enumerate(atoms_data):
		if "Bonds" in line:
			print(atoms_data[i])
			while len(atoms_data) > i+2:
				bond = atoms_data[i+2].split()
				print(bond[0] + ' ' + bond[1] + ' ' + bond[2] + ' ' + bond[3])
				i += 1


rescale("minimize.atoms", "minimize.lammpstrj", 1.05)
