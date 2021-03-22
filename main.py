import Parser
import Algorithms
import Utilities
import Settings as UI

# Allowed characters are (order of precedence for operators is the order from up to bottom):
# [a-z][A-Z]  - atoms (lowercase will not be treated as the same atom as UPPERCASE)
# { ¬ ! - }   - not
# { ∧ & ^ * } - and
# { ∨ | v + } - or
# { ⇒ > → ⊃ } - implication (if.. then)
# { ⇔ ~ ↔ }   - equivalence (if and only if)

# Operators can be mixed or used interchangeably without affecting the formula
# The output formula will always contain the logical operators though

# *** Associativity is from right to left ( EX: A⇒B⇒C ~ (A⇒(B⇒C)) )***

# --- INPUT ---

# If formula = "" or it is not declared, then you will need to type it into the console and press ENTER
# Otherwise you can just type your formula here
formula = ""
try:
    if not formula:
        print("Introduceti o formula propozitionala:")
        formula = input()
except:
    print("Introduceti o formula propozitionala:")
    formula = input()

# --- END OF INPUT ---

if __name__ == "__main__":
    print() # first line will always be empty
    # Transforms operators into the logical ones
    # If invalid characters are found, will throw an error
    formula = Parser.Transorm_to_logical(formula)

    # Checks if the formula respects a minimal set of rules
    # Ex: Number of left parenthesis is equal to the number of right ones, etc.
    Parser.Minimal_check(formula)

    # Transforms formula from infix form to postfix form
    # Much easier for the computer to parse a postfix formula
    postfix_formula = Parser.Infix_to_postfix(formula)

    # strict syntax formula
    infix_formula = Parser.Postfix_to_infix(postfix_formula)
    if UI.Strict_syntax:
        print("Sintaxa stricta a formulei propozitionale este: ", end='')
        print(infix_formula, end = '\n\n')

    # Get Atoms
    Atoms = Utilities.Get_atoms(postfix_formula)
    Atoms.sort()
    if UI.Show_atoms:
        Utilities.Print_atoms(Atoms)

    # Without a table, extended option does not have an effect
    if UI.Truth_table == False:
        UI.Extended = False

    # Split infix formula into components, helpful for extended truth table
    list_of_components = Parser.Split_infix_formula(infix_formula[1:len(infix_formula) - 1], [])[1]
    # Transform components to postfix form (for processing)
    list_of_postfix_components = [Parser.Infix_to_postfix(F) for F in list_of_components]

    # This will create a CSV file where the Truth-Table can be found
    if UI.Truth_table:
        Truth_table = Algorithms.Calculate_truth_table(list_of_postfix_components, Atoms, UI.Extended)
        Utilities.Create_Truth_Table(Truth_table, Atoms, list_of_components, UI.Extended)

    # This will print the formula in FNC
    if UI.FNC:
        FNC = Algorithms.Get_FNC(Atoms, postfix_formula)
        print("FNC: ", end='')
        if FNC:
            print(FNC, end = '\n\n')
        else:
            print("TAUTOLOGIE!\n")

    # This will print the formula in FND
    if UI.FND:
        FND = Algorithms.Get_FND(Atoms, postfix_formula)
        print("FND: ", end='')
        if FND:
            print(FND, end = '\n\n')
        else:
            print("CONTRADICTIE!\n")

    # This will print if the formula is satisfiable
    if UI.Satisfiability:
        if UI.Truth_table == False:
            Truth_table = Algorithms.Calculate_truth_table(list_of_postfix_components, Atoms, UI.Extended)

        if Utilities.Check_satisfiability(Truth_table):
            print("Formula propozitionala introdusa este SATISFIABILA!\n")
        else:
            print("Formula propozitionala introdusa este NESATISFIABILA!\n")

    # This will print if the formula is valid
    if UI.Validity:
        if UI.Truth_table == False:
            Truth_table = Algorithms.Calculate_truth_table(list_of_postfix_components, Atoms, UI.Extended)

        if Utilities.Check_validity(Truth_table):
            print("Formula propozitionala introdusa este VALIDA!\n")
        else:
            print("Formula propozitionala introdusa este INVALIDA!\n")

    # SKIP_FNC will treat the formula as being already in FNC
    if UI.SKIP_FNC:
        FNC = formula
    # If FNC wasn't computed yet, we will compute it (we need FNC for resolution methods)
    elif UI.FNC == False:
        FNC = Algorithms.Get_FNC(Atoms, postfix_formula)

    # This will print the clauses of the FNC
    if UI.Show_clauses:
        Set_of_clauses = Algorithms.Get_set_of_clauses(FNC)
        print("Multimea de clauze a formulei in FNC este:")
        print(Set_of_clauses, end='\n\n')

    # This will print a step by step resolution method applied on our set of clauses
    if UI.Resolution:
        # if clauses has not been already done
        if UI.Show_clauses == False:
            Set_of_clauses = Algorithms.Get_set_of_clauses(FNC)

        if Algorithms.Propositional_resolution(Set_of_clauses):
            print("Rezolutie: Formula propozitionala este satisfiabila!")
        else:
            print("Rezolutie: Formula propozitionala este nesatisfiabila!")

    # This will print a step by step DP method applied on our set of clauses
    elif UI.DP:
        Set_of_clauses = Algorithms.Get_set_of_clauses(FNC,True)
        if Algorithms.DP(Set_of_clauses, Atoms):
            print("DP: Formula propozitionala este satisfiabila!")
        else:
            print("DP: Formula propozitionala este nesatisfiabila!")

    # This will print a step by step DPLL method applied on our set of clauses
    # elif UI.DPLL:
    #     Set_of_clauses = Algorithms.Get_set_of_clauses(FNC, True)
    #     if Algorithms.DPLL(Set_of_clauses, Atoms):
    #         print("DPLL: Formula propozitionala este satisfiabila!")
    #     else:
    #         print("DPLL: Formula propozitionala este nesatisfiabila!")
