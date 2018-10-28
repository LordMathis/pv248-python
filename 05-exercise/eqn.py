from sys import argv
import numpy as np
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
    vec = []
    for equation in equations:
        matrix_row = []
        for var in variables:
            if var in equation:
                matrix_row.append(equation[var])
            else:
                matrix_row.append(0)
        vec.append(equation['result'])
        matrix.append(matrix_row)

    return np.array(matrix), np.array(vec)

def frobein(matrix, vector):

    n = vector.shape[0]
    vector = np.reshape(vector, (n,1))

    augmented = np.append(matrix, vector, 1)

    rank_a = linalg.matrix_rank(augmented)
    rank_b = linalg.matrix_rank(matrix)

    if rank_a != rank_b:
        return -1

    if rank_b == matrix.shape[1]:
        return 0

    return matrix.shape[1] - rank_b

def solve(matrix, vector, variables):
    res = linalg.solve(matrix, vector)
    solution = {}
    for i in range(0, len(variables)):
        solution[variables[i]] = res[i]

    return solution


if __name__ == '__main__':

    input = argv[1]
    eq_system = []
    variables = []

    with open(input, 'r') as lines:
        for line in lines:
            equation, vars = parse_line(line)
            eq_system.append(equation)
            variables = list(set(vars + variables))

    matrix, vector = to_matrix(eq_system, variables)
    num_sol = frobein(matrix, vector)

    if num_sol == -1:
        print('no solution')

    elif num_sol == 0:

        solution = solve(matrix, vector, variables)
        solution_string = "solution:"

        for key, value in sorted(solution.items(), key=lambda x: x[0]):
            solution_string += " " + str(key) + " = " + str(value) + ","
        print(solution_string[:-1])

    else:
        print('solution space dimension:', num_sol)
