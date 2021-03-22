from collections import deque

def Minimal_check(formula):
    operators = "∧∨⇒⇔" # not is excluded
    left = 0
    right = 0
    prev = ''

    if formula[0] in operators:
        raise Exception("ERROR: Invalid formula!")

    for x in formula:

        if (x in operators and prev in operators) or (x.isalpha() and prev.isalpha()):
            raise Exception("ERROR: Invalid formula!")
        elif x == '(':
            left += 1
        elif x == ')':
            right += 1

        prev = x

    if x in operators or x == '¬':
        raise Exception("ERROR: Invalid formula!")

    if left != right:
        raise Exception("ERROR: Invalid formula!")


set_not = "¬!-"
set_and = "∧&^*"
set_or  = "∨|v+"
set_imp = "⇒>→⊃"
set_eqv = "⇔~↔"
def Logical_chr(chr):
    if chr == ' ':
        return ''

    if chr.isalpha() or chr == '(' or chr == ')':
        return chr

    for x in set_not:
        if chr == x:
            return '¬'

    for x in set_and:
        if chr == x:
            return '∧'

    for x in set_or:
        if chr == x:
            return '∨'

    for x in set_imp:
        if chr == x:
            return '⇒'

    for x in set_eqv:
        if chr == x:
            return '⇔'

    raise Exception("ERROR: Invalid character inside formula!")


def Transorm_to_logical(formula):
    logical_form = ""
    for x in formula:
        logical_form += Logical_chr(x)

    return logical_form


def Precedence(operator):

    if operator == '¬':
        return 1
    elif operator == '∧':
        return 2
    elif operator == '∨':
        return 3
    elif operator == '⇒':
        return 4
    elif operator == '⇔':
        return 5
    else:
        return 6


def Infix_to_postfix(in_str):

    stack = deque()
    post_str = ''
    for c in in_str:

        if c.isalpha():
            post_str += c

        elif c == '(':
            stack.append('(')

        elif c == ')':
            while stack and stack[-1] != '(':
                post_str += stack[-1]
                stack.pop()
            stack.pop() #removing '('

        else:
            # Asociativitate la dreapta: >
            # Asociativitate la stanga: >=
            while stack and Precedence(c) > Precedence(stack[-1]):
                post_str += stack[-1]
                stack.pop()
            stack.append(c)

    while stack:
        post_str += stack[-1]
        stack.pop()

    return post_str


def Postfix_to_infix(post_str):

    stack = deque()
    for c in post_str:
        if c.isalpha():
            stack.append(c)
        else:
            if c== '¬':
                str = '(' + c + stack[-1] + ')'
                stack.pop()
            else:
                str = '(' + stack[-2] + c + stack[-1] + ')'
                stack.pop()
                stack.pop()

            stack.append(str)

    return stack[-1]


def Split_infix_formula(formula, list):
    i = 0
    while i < len(formula):

        if formula[i] == '(':
            tup = Split_infix_formula(formula[i + 1:], list)
            i += tup[0]
            list = tup[1]

        elif formula[i] == ')':
            list.append(formula[:i])
            return i + 1, list

        i += 1

    list.append(formula)
    return None, list
