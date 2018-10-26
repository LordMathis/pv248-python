from sys import argv
import numpy
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

def to_matrix(equations, variables):
    matrix = []
    for equation in equations:
        matrix_row = []
        for var in variables:
            if equation[var]:
                matrix_row.append(equation[var])
            else:
                matrix_row.append(0)
        matrix_row.append(equation['result'])
        matrix.append(matrix_row)
    return numpy.array(matrix)

if __name__ == '__main__':

    input = argv[1]
    eq_system = []
    variables = []

    with open(input, 'r') as lines:
        for line in lines:
            equation, vars = parse_line(line)
            eq_system.append(equation)
            variables = list(set(vars + variables))

    matrix = to_matrix(eq_system, variables)
    print(matrix)
