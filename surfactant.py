# 構造緩和した後の粒子を読み込んでリスケール
class Atoms:
    def __init__(self, atoms_id, mol_id, atoms_type, x, y, z, vx, vy, vz):
       self.atoms_id = atoms_id
       self.mol_id = mol_id
       self.atoms_type = atoms_type
       self.x = x
       self.y = y
       self.z = z
       self.vx = vx
       self.vy = vy
       self.vz = vz


class Bonds:
    def __init__(self, bonds_id, bonds_type, atoms_id1, atoms_id2):
        self.bonds_id = bonds_id
        self.bonds_type = bonds_type
        self.atoms_id1 = atoms_id1
        self.atoms_id2 = atoms_id2


def rescale(atoms, bonds, atoms_file, dump_file, scale):
    with open(atoms_file, "r") as f:  #atomsのファイルを読み込み
        atoms_data = f.readlines()
    with open(dump_file, "r") as f:  #dumpファイルを読み込み
        dump_data = f.readlines()
    step = []  #ダンプファイルにおけるstepの始まりのインデックスの配列
    for i, line in enumerate(dump_data):
        if "ITEM: TIMESTEP" in line:
            step.append(i)
    dl = dump_data[step[-1]+5]  
    L = float(dl.split()[1])  #ボックスサイズ
    num_atoms = int(atoms_data[2].split()[0])  #atomの数
    num_bonds = int(atoms_data[3].split()[0])  #bondの数
    mol_list = [0 for i in range(num_atoms+num_bonds)]
    for i, line in enumerate(atoms_data):
        if "Atoms" in line:
            while i+2 < num_atoms+14:
                atoms_id = int(atoms_data[i+2].split()[0])
                mol_id = int(atoms_data[i+2].split()[1])
                mol_list[atoms_id-1] = mol_id  #mol_idをatoms_idにひもづける
                i += 1
        if "Bonds" in line:
            while len(atoms_data) > i+2:
                bl = atoms_data[i+2].split()
                bonds.append(Bonds(bl[0], bl[1], bl[2], bl[3]))
                i += 1
    for i in range(num_atoms):
        position = dump_data[step[-1]+9+i]  #最後のグループの座標dataの先頭
        atoms_id = int(position.split()[0])
        atoms_type = int(position.split()[1])
        x = float(position.split()[2]) * scale
        y = float(position.split()[3]) * scale
        z = float(position.split()[4]) * scale
        vx = float(position.split()[5])
        vy = float(position.split()[6])
        vz = float(position.split()[7])
        atoms.append(Atoms(atoms_id, mol_list[atoms_id-1], atoms_type, x, y, z, vx, vy, vz))
    return L


def save_file(atoms, bonds, L, scale):
    print("Position Data\n")
    print("{} atoms".format(len(atoms)))
    print("{} bonds\n".format(len(bonds)))
    print("3 atom types")
    print("1 bond types\n")
    print("0.00 {} xlo xhi".format(scale*L))
    print("0.00 {} ylo yhi".format(scale*L))
    print("0.00 {} zlo zhi\n".format(scale*L))
    print("Atoms\n")
    for i, a in enumerate(atoms):
        print("{} {} {} {} {} {}".format(a.atoms_id, a.mol_id, a.atoms_type, a.x, a.y, a.z))
    print("\n")
    print("Velocities\n")
    for i, a in enumerate(atoms):
        print("{} {} {} {}".format(a.atoms_id, a.vx, a.vy, a.vz))
    print("\n")
    print("Bonds\n")
    for i, a in enumerate(bonds):
        print("{} {} {} {}".format(a.bonds_id, a.bonds_type, a.atoms_id1, a.atoms_id2))


atoms = []  #dump_fileのAtomsを保存したリスト
bonds = []  #atoms_fileのBondsを保存したリスト
L = rescale(atoms, bonds, "minimize.atoms", "minimize.lammpstrj", 1.05)
save_file(atoms, bonds, L, 1.05)
