from sys import argv
from numpy import linalg

def parse_line(line):
    equation = {}
    variables = []
    sign = 1
    result = False

    for char in line.split():

        if char == '+':
            sign = 1
        elif char == '-':
            sign = -1
        elif char == '=':
            result = True
        elif result:
            equation['result'] = int(char)
        else:
            koef = sign
            var_name = char[-1]
            variables.append(var_name)
            if len(char) > 1:
                koef = sign * int(char[:-1])
            equation[var_name] = koef

    return equation, variables

def to_array(equations, variables):
    pass

if __name__ == '__main__':

    input = argv[1]
    eq_system = []
    variables = []

    with open(input, 'r') as lines:
        for line in lines:
            equation, vars = parse_line(line)
            eq_system.append(equation)
            variables = list(set(vars + variables))


    print(eq_system, variables)
