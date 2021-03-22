from collections import deque

class Clause:
    def __init__(self, C_neg, C_poz):
        # C_neg and C_poz should be a frozenset for simple Resolution method
        # And a normal set otherwise
        self.set_neg = C_neg
        self.set_poz = C_poz

    def __repr__(self):
        clause = []
        for atom in self.set_poz:
            clause.append(atom)
        for atom in self.set_neg:
            clause.append('¬' + atom)
        clause.sort()
        return str(clause)


def Generate_interpretation(Atoms, lvl, curr_interpretation = {}):

    if lvl == len(Atoms):
        yield curr_interpretation
    else:
        curr_interpretation[ Atoms[lvl] ] = False
        yield from Generate_interpretation(Atoms, lvl + 1, curr_interpretation)

        curr_interpretation[ Atoms[lvl] ] = True
        yield from Generate_interpretation(Atoms, lvl + 1, curr_interpretation)


def Calculate_truth_table(components, Atoms, Extended = False):
    Table_rows = []

    for interpretation in Generate_interpretation(Atoms, 0):
        row = list(interpretation.values())

        if Extended:
            for formula in components:
                row.append(Calculate_interpretation(formula, interpretation))
        else:
            row.append(Calculate_interpretation(components[-1], interpretation))

        Table_rows.append(row)
        #print(interpretation, end = ' = ')
        #print(Calculate_interpretation(components[-1], interpretation))

    return Table_rows


# Only for postfix formula
def Calculate_interpretation(formula, interpretation):

    stack = deque()
    for x in formula:
        if x.isalpha():
            stack.append( interpretation[x] )
        else:
            if x == '¬':
                stack[-1] = not stack[-1]
            else:
                b = stack[-1]
                stack.pop()
                a = stack[-1]
                stack.pop()
                if x == '∧':
                    stack.append(a and b)
                elif x == '∨':
                    stack.append(a or b)
                elif x == '⇒':
                    stack.append((not a) or b)
                elif x == '⇔':
                    stack.append((a and b) or ((not a) and (not b)))

    return stack[-1]


def Get_FNC(Atoms, formula):

    FNC_str = ""
    for interpretation in Generate_interpretation(Atoms, 0):

        value = Calculate_interpretation(formula, interpretation)

        if value == False:
            FNC_str += '('
            not_first_chr = False

            for atom in interpretation:
                if not_first_chr:
                    FNC_str += '∨'
                not_first_chr = True

                if interpretation[atom] == True:
                    FNC_str += '¬'
                FNC_str += atom

            FNC_str += ")∧"

    # last element is always ^
    return FNC_str[:-1]


def Get_FND(Atoms, formula):

    FND_str = ""
    for interpretation in Generate_interpretation(Atoms, 0):

        value = Calculate_interpretation(formula, interpretation)

        if value == True:
            FND_str += '('

            not_first_chr = False

            for atom in interpretation:
                if not_first_chr:
                    FND_str += '∧'
                not_first_chr = True

                if interpretation[atom] == False:
                    FND_str += '¬'
                FND_str += atom

            FND_str += ')∨'

    # last element is always ∨
    return FND_str[:-1]

def Get_set_of_clauses(FNC_formula, DP = False):
    open_clause = False
    NOT = False
    Set = []
    for chr in FNC_formula:
        if chr == ' ':
            continue

        if chr == '(':
            open_clause = True
            C_list_neg = []
            C_list_poz = []
        elif chr == ')':
            if DP:
                Set.append(Clause(set(C_list_neg),set(C_list_poz)))
            else:
                Set.append(Clause(frozenset(C_list_neg),frozenset(C_list_poz)))
            open_clause = False
        else:
            if open_clause == True:
                if chr == '¬':
                    NOT = True
                elif chr.isalpha():
                    if NOT:
                        C_list_neg.append(chr)
                    else:
                        C_list_poz.append(chr)
                    NOT = False
                else:
                    assert chr == '∨', "Nu s-a putut extrage multimea de clauze, formula nu este in FNC!"
            else:
                assert chr == '∧', "Nu s-a putut extrage multimea de clauze, formula nu este in FNC!"

    return Set


def Check_for_trivial_clause(C):
    if len(C.set_neg) < len(C.set_poz):
        for atom in C.set_neg:
            if atom in C.set_poz:
                return True
    else:
        for atom in C.set_poz:
            if atom in C.set_neg:
                if atom in C.set_neg:
                    return True

    return False

def Resolvent(Clause1, Clause2, atom):
    # creeam o clauza noua care este reuniunea lui C1 si C2

    new_Clause_poz = Clause1.set_poz.difference(atom).union(Clause2.set_poz.difference(atom))
    new_Clause_neg = Clause1.set_neg.difference(atom).union(Clause2.set_neg.difference(atom))

    new_Clause = Clause(new_Clause_neg,new_Clause_poz)

    return new_Clause


def Search_for_resolvent(List_clauses, Set_clauses, C1, Not_checked_range, Trivial_clause, i, j):
    if Trivial_clause[j]:
        return

    # Vom compara toti atomii negative dintr-o clauza cu toti atomii pozitivi din cealalta clauza
    # Si invers

    C2 = List_clauses[j]
    for atom in C1.set_poz:
        if atom in C2.set_neg:
            # Creeam o clauza noua care este reuniunea lui C1 si C2
            New_C = Resolvent(C1, C2, atom)

            # Verificam daca clauza noua exista deja
            if (New_C.set_neg,New_C.set_poz) in Set_clauses:
                return

            print("Din clauza ({}) si ({}) prin eliminarea lui {} s-a format clauza ({}):".format(i + 1, j + 1, atom, len(List_clauses) + 1))
            print(New_C, end='\n\n')

            if len(New_C.set_poz) == 0 and len(New_C.set_neg) == 0:
                print("Am obitnut o clauza vida => Nesatisfiabila!\n")
                return False
            else:
                # Daca nu, adaugam clauza noua

                # Verificam daca este o clauza triv
                Trivial_clause.append(Check_for_trivial_clause(New_C))
                if Trivial_clause[len(List_clauses)]:
                    print("S-a eliminat clauza triviala {}".format(len(List_clauses) + 1), end='\n\n')

                List_clauses.append(New_C)
                Set_clauses.add((New_C.set_neg,New_C.set_poz))

                # cu Not_checked_range vom parcurge pana la indicele i mai incolo
                # pentru a ne asigura ca se vor face toate combinatiile posibile inclusiv cu clauzele noi
                Not_checked_range.append(i)

            return

    for atom in C1.set_neg:
        if atom in C2.set_poz:
            # creeam o clauza noua care este reuniunea lui C1 si C2
            New_C = Resolvent(C1, C2, atom)

            # Verificam daca clauza noua exista deja
            if (New_C.set_neg,New_C.set_poz) in Set_clauses:
                return

            print("Din clauza ({}) si ({}) prin eliminarea lui {} s-a format clauza ({}):".format(i + 1, j + 1, atom, len(List_clauses) + 1))
            print(New_C, end='\n\n')

            # Verificam daca am obtinut o clauza vida
            if len(New_C.set_poz) == 0 and len(New_C.set_neg) == 0:
                print("Am obitnut o clauza vida => Nesatisfiabila!\n")
                return False
            else:
                # Daca nu, adaugam clauza noua

                # Verificam daca este o clauza triviala
                Trivial_clause.append(Check_for_trivial_clause(New_C))
                if Trivial_clause[len(List_clauses)]:
                    print("S-a eliminat clauza triviala {}".format(len(List_clauses) + 1), end='\n\n')

                List_clauses.append(New_C)
                Set_clauses.add((New_C.set_neg,New_C.set_poz))

                # cu Not_checked_range vom parcurge pana la indicele i mai incolo
                # pentru a ne asigura ca se vor face toate combinatiile posibile inclusiv cu clauzele noi
                Not_checked_range.append(i)

            return

def Print_clauses_list(List_clauses, Trivial_clause):
    print("Multimea ramasa de clauze este:")
    for i in range(len(List_clauses)):
        str = "({}) {}".format(i + 1, List_clauses[i])
        if Trivial_clause[i]:
            # Clauzele trivala au fost taiate, deci vom afisa o linie peste acestea
            str = '\u0336'.join(str) + '\u0336'
        print(str)
    print()


def Propositional_resolution(List_clauses):
    # Functia va returna True daca am obtinut satisfiabilitatea
    # si False daca am obtinut nesatisfiabilitatea

    Trivial_clause = [] # sir ce contine numai False si True
    Not_checked_range = [0] * len(List_clauses) # un sir de indici
    Set_clauses = set() # multimea de clauze


    for i in range(len(List_clauses)):
        # Adaug in vectorul Trivial_clause daca clauza i este sau nu este clauza triviala
        Trivial_clause.append(Check_for_trivial_clause(List_clauses[i]))

        # Adaug Clauza in multimea de clauze (NU PERMITE DUBLURI)
        Set_clauses.add((List_clauses[i].set_neg,List_clauses[i].set_poz))

        if Trivial_clause[i] == True:
            print("S-a eliminat clauza triviala ({}): {}".format(i, List_clauses[i]), end='\n\n')

    # Parcurg toata lista de clauze
    # *** Nu parcurg set-ul de clauze pentru ca am nevoie de o ordine garantata si de un index, ceea ce set-ul nu ofera ***
    i = 0
    while i + 1 < len(List_clauses): # Parcurg absolut toate clauzele
        if Trivial_clause[i] == True:
            i += 1
            continue

        # Creez aceasta variabila pentru ca mai incolo o sa am nevoie de ea la for (ca sa nu parcurg clauzele noi create in acest ciclu)
        # Pentru a nu combina o clauza C si o clauza derivata din C, pentru ca nu va avea niciun rezultat
        Numer_of_clauses = len(List_clauses)

        # extragem o clauza
        C1 = List_clauses[i]

        # acest for este pentru clauzele noi create care nu au fost inca comparate cu clauzele de dinainte de i
        # practic acest for asigura ca vom face toate combinatiile posibile care pot avea un rezultat
        for j in range(Not_checked_range[i]):
            if Search_for_resolvent(List_clauses, Set_clauses, C1, Not_checked_range, Trivial_clause, i, j) == False:
                return False

        # acest for porneste de la i + 1 pentru a nu facem aceleasi comparatii de 2 ori
        for j in range(i + 1, Numer_of_clauses):
            if Search_for_resolvent(List_clauses, Set_clauses, C1, Not_checked_range, Trivial_clause, i, j) == False:
                return False

        i += 1

    Print_clauses_list(List_clauses, Trivial_clause)

    return True


def Check_if_clause_exists(List_clauses, C):
    for clause in List_clauses:
        if clause.set_poz == C.set_poz and clause.set_neg == C.set_neg:
            return True

    return False


def DP(List_clauses, List_atoms):
    Trivial_clause = []  # sir ce contine numai False si True
    Not_checked_range = [0] * len(List_clauses)  # un sir de indici
    Set_clauses = set()  # multimea de clauze

    Atoms_dict = {}
    for i in range(len(List_atoms)):
        Atoms_dict[List_atoms[i]] = i

    #print(List_clauses)

    ok = True
    while ok:
        ok = False

        # -- RULE 1 ---
        for i in range(len(List_clauses)):
            C = List_clauses[i]
            if len(C.set_neg) + len(C.set_poz) == 1:
                NEG = False
                if C.set_neg:
                    NEG = True
                    atom = next(iter(C.set_neg))
                    print("1. Regula clauzei cu un literal: (¬{})".format(atom))
                else:
                    atom = next(iter(C.set_poz))
                    print("1. Regula clauzei cu un literal: ({})".format(atom))

                new_list = []
                for j in List_clauses:
                    if atom in j.set_poz:
                        if NEG:
                            print("Se sterge ({}) din clauza: {}".format(atom,j))
                            j.set_poz.remove(atom)

                            if not j.set_poz:
                                print("S-a gasit o clauza vida!")
                                return False

                            new_list.append(j)
                        else:
                            print("Se sterge clauza: {}".format(j))

                    elif atom in j.set_neg:
                        if NEG == False:
                            print("Se sterge (¬{}) din clauza: {}".format(atom,j))
                            j.set_neg.remove(atom)

                            if not j.set_neg:
                                print("S-a gasit o clauza vida!")
                                return False

                            new_list.append(j)
                        else:
                            print("Se sterge clauza: {}".format(j))

                List_clauses = new_list
                print()
                ok = True
                break

        if ok:
            continue

        # --- RULE 2 ---
        count_neg = [0] * len(List_atoms)
        count_poz = [0] * len(List_atoms)

        for i in range(len(List_clauses)):
            C = List_clauses[i]

            for atom in C.set_neg:
                count_neg[Atoms_dict[atom]] += 1

            for atom in C.set_poz:
                count_poz[Atoms_dict[atom]] += 1

        for i in range(len(List_atoms)):
            if (count_neg[i] == 0 and count_poz[i] > 0) or (count_neg[i] > 0 and count_poz[i] == 0):
                atom = List_atoms[i]
                if count_neg[i] > 0:
                    print("2. Regula literalului pur: (¬{})".format(atom))
                else:
                    print("2. Regula literalului pur: ({})".format(atom))

                new_list = []
                for j in List_clauses:
                    if atom in j.set_poz or atom in j.set_neg:
                        print("S-a sters clauza: {}".format(j))
                    else:
                        new_list.append(j)

                List_clauses = new_list
                print()
                ok = True
                break

        if ok:
            continue

        # --- Rule 3 ---
        for i in range(1, len(List_clauses)):
            C1 = List_clauses[i]

            for j in range(i):
                C2 = List_clauses[j]

                for atom in C1.set_neg:
                    if atom in C2.set_poz:
                        C = Resolvent(C1, C2, atom)

                        if Check_if_clause_exists(List_clauses, C):
                            break

                        if Check_for_trivial_clause(C):
                            break

                        print("3. Se aplica rezolutia si se combina: {} si {}".format(C1, C2))

                        if len(C.set_poz) == 0 and len(C.set_neg) == 0:
                            print("S-a gasit o clauza vida!")
                            return False

                        List_clauses.append(C)
                        ok = True
                        break

                if ok == True:
                    break

                for atom in C1.set_poz:
                    if atom in C2.set_neg:
                        C = Resolvent(C1, C2, atom)

                        if Check_if_clause_exists(List_clauses, C):
                            break

                        if Check_for_trivial_clause(C):
                            break

                        print("3. Se aplica rezolutia si se combina: {} si {}".format(C1, C2))

                        if len(C.set_poz) == 0 and len(C.set_neg) == 0:
                            print("S-a gasit o clauza vida!")
                            return False

                        List_clauses.append(C)
                        ok = True
                        break
                if ok:
                    break
            if ok:
                break

    return True

# def DPLL(List_clauses, List_atoms):
#     pass