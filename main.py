from ortools.linear_solver import pywraplp
import math
c = [1, 2]
A = [
    [1, 2],
    [3, 4]
]
b = [5, 6]
def PLSolver(c, A, b):
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    m = len(A)

    #Variáveis
    x = solver.NumVar(0, solver.infinity(), "x")
    y = solver.NumVar(0, solver.infinity(), "y")
    vars = [x, y]

    #Função Objetivo 
    solver.Maximize(solver.Sum(c[i]*vars[i] for i in range(len(c))))

    #Condições
    for i in range(m):
        solver.Add(solver.Sum(A[i][j]*vars[j] for j in range(len(A[i]))) <= b[i])

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.2f}")
        print(f"x = {x.solution_value():0.2f}")
        print(f"y = {y.solution_value():0.2f}")
        r = []
        for i in range(len(vars)):
            r.append(vars[i].solution_value())
        return r
    else:
        print("O problema não possui solução ótima.")

def checkIntegrability(solutions):
    for i in range(len(solutions)):
        if(not int(solutions[i])):
            return False
    return True

def getDecimalVar(solutions):
    for i in range(len(solutions)):
        if(not int(solutions[i])):
            return solutions[i]
    return None


def BranchAndBound(solver, solutions, bestBranchSolution, b):
    #solver.Add()
    bestBranchSolution = solver.Objective().Value()
    decimal = getDecimalVar(solutions)
    ceil = math.ceil(decimal)
    floor = math.floor(decimal)
    BranchAndBound(solver, solutions, bestBranchSolution, ceil)
    BranchAndBound(solver, solutions, bestBranchSolution, floor)
    if(checkIntegrability(solutions)):
        print("Poda por Integrabilidade")
    

PLSolver(c, A, b)