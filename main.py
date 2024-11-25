from ortools.linear_solver import pywraplp
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
    else:
        print("O problema não possui solução ótima.")

def BranchAndBound():
    pass

PLSolver(c, A, b)