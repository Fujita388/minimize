# single.lammpstrjからrandom.sampleで界面活性剤の2倍の数のA原子をA-B分子に置換
import random


random.seed(117)


class Atoms:
    def __init__(self, atoms_id, mol_id, atoms_type, x, y, z, vx, vy, vz):
        self.atoms_id = atoms_id
        self.mol_id = mol_id
        self.type = atoms_type
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz


def choice(num_surf, num_atoms):  # num_surf:界面活性剤の数 num_atoms:粒子数
    l = []
    for i in range(num_atoms):
        l.append(i)
    choiced_list = random.sample(l, num_surf*2)  # 選ばれたA原子のリスト
    return choiced_list


def read_dump(atoms, bonds_list, dump_file, num_surf):
    with open(dump_file, "r") as f:  
        dump_data = f.readlines()
    step = []  #ダンプファイルにおけるstepの始まりのインデックスの配列
    for i, line in enumerate(dump_data):
        if "ITEM: TIMESTEP" in line:
            step.append(i)
    l = dump_data[step[-1]+5]  
    L = float(l.split()[1])  #ボックスサイズ
    num_atoms = int(dump_data[3])  #粒子数
    mol_id = 0
    num_bonds = 0  #bond数
    choiced_list = choice(num_surf, num_atoms)
    for i in range(num_atoms):
        position = dump_data[step[-1]+9+i]  #最後のグループの座標dataの先頭
        atoms_id = int(position.split()[0])
        x = float(position.split()[2])
        y = float(position.split()[3])
        z = float(position.split()[4])
        vx = float(position.split()[5])
        vy = float(position.split()[6])
        vz = float(position.split()[7])
        if i in choiced_list:  #選ばれたリスト内に粒子iが存在するか
            if choiced_list.index(i) < len(choiced_list)/2:
                num_bonds += 1
                bonds_list.append(atoms_id)
                bonds_list.append(num_atoms + num_bonds)
                atoms.append(Atoms(atoms_id, mol_id, 2, x, y, z, vx, vy, vz))  #AをA-Bで置換
                atoms.append(Atoms(num_atoms + num_bonds, mol_id, 3, x+0.35, y+0.35, z+0.35, vx, vy, vz))  #少しずらす
            else:
                continue
        else:
            atoms.append(Atoms(atoms_id, mol_id, 1, x, y, z, vx, vy, vz))
        mol_id += 1
    return num_bonds, L


def save_file(atoms, num_bonds, L):
    print("Position Data\n")
    print("{} atoms".format(len(atoms)))
    print("{} bonds\n".format(num_bonds))
    print("3 atom types")
    print("1 bond types\n")
    print("0.00 {} xlo xhi".format(L))
    print("0.00 {} ylo yhi".format(L))
    print("0.00 {} zlo zhi\n".format(L))
    print("Atoms\n")
    for i, a in enumerate(atoms):
        print("{} {} {} {} {} {}".format(a.atoms_id, a.mol_id, a.type, a.x, a.y, a.z))
    print("\n")
    print("Velocities\n")
    for i, a in enumerate(atoms):
        print("{} {} {} {}".format(a.atoms_id, a.vx, a.vy, a.vz))
    print("\n")
    print("Bonds\n")
    j = 0
    for i in range(num_bonds):
        print(i+1, 1, bonds_list[j], bonds_list[j+1])  #bonds_id, bonds_type, atoms_id1, atoms_id2 
        j += 2


atoms = []
bonds_list = []  #atoms_idのペアのリスト
num_bonds, L = read_dump(atoms, bonds_list, "single.lammpstrj", 1289)
save_file(atoms, num_bonds, L)
