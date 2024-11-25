from ortools.linear_solver import pywraplp
def BranchAndBound():
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    #Variáveis
    x = solver.NumVar(0, solver.infinity(), "x")
    y = solver.NumVar(0, solver.infinity(), "y")

    #Função Objetivo 
    solver.Maximize(x + y)

    #Condições
    solver.Add(x + y < 0)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.2f}")
        print(f"x = {x.solution_value():0.2f}")
        print(f"y = {y.solution_value():0.2f}")
    else:
        print("O problema não possui solução ótima.")

BranchAndBound()