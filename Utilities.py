import csv

def Get_atoms(formula):
    Atoms_set = set()
    for x in formula:
        if x.isalpha():
            Atoms_set.add(x)

    return list(Atoms_set)


def Print_atoms(Atoms):
    print("Atomii formulei propozitionale sunt: {", end='')
    first = True
    for atom in Atoms:
        if not first:
            print(end=',')
        first = False
        print(atom, end='')
    print('}\n')


def Check_satisfiability(Truth_table):
    for row in Truth_table:
        if row[-1] == True:
            return True
    return False


def Check_validity(Truth_table):
    for row in Truth_table:
        if row[-1] == False:
            return False
    return True


def Create_Truth_Table(values, Atoms, components, Extended = False):
    with open('Truth-Table.csv', 'w', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        header = Atoms[:]
        if Extended:
            header.extend(components)
        else:
            header.append(components[-1])
        writer.writerow(header)

        for row in values:
            writer.writerow(row)