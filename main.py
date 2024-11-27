from ortools.linear_solver import pywraplp
import math
c = [1, 2]
A = [
    [1, 2],
    [3, 4]
]
b = [5, 6]

#Função que cria o solver
def GetNewSolver(c, A, b, conditionsLeft, conditionsRight):
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    m = len(A)

    # Definir variáveis
    vars = []
    for i in range(len(c)):
        vars.append(solver.NumVar(0, solver.infinity(), f"x{i}"))

    #Função Objetivo 
    solver.Maximize(solver.Sum(c[i]*vars[i] for i in range(len(c))))

    #Condições
    for i in range(m):
        solver.Add(solver.Sum(A[i][j]*vars[j] for j in range(len(A[i]))) <= b[i])
    if(conditionsLeft):
        print("Hm")
        for i in range(len(conditionsLeft)):
            solver.Add(conditionsLeft[i][0] >= conditionsLeft[i][1])
    if(conditionsRight):
        print("Hm")
        for i in range(len(conditionsRight)):
            solver.Add(conditionsRight[i][0] <= conditionsRight[i][1])

    return solver, vars

#Função que resolve o problema e posteriormente vai chamar o Branch and Bound
def PLSolver(c, A, b):
    solver, vars = GetNewSolver(c, A, b, 0, 0)

    if not solver:
        return

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.2f}")
        for i, var in enumerate(vars):
            print(f"x{i} = {var.solution_value():0.2f}")
        return solver, vars
    else:
        print("O problema não possui solução ótima.")
        return None, None

def checkIntegrability(vars):
    for i in range(len(vars)):
        if(not vars[i].solution_value().is_integer()):
            return False
    return True

def getDecimalVar(vars):
    for i in range(len(vars)):
        if(not vars[i].solution_value().is_integer()):
            return vars[i]
    return None

#Diz respeito a parte esquerda do branch and bound
def BranchLeft(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight):
    conditionsL = conditionsLeft.copy()
    conditionsR = conditionsRight.copy()
    #Criamos um novo solver com as mesmas condicoes
    solver, vars = GetNewSolver(c, A, b, conditionsL, conditionsR)
    #Calculamos o teto
    ceil = math.ceil(decimalVar.solution_value())
    #Adicionamos a condição
    print(f"Adicionando {ceil} na condicao")
    solver.Add(decimalVar >= ceil)
    conditionsL.append([decimalVar, ceil])
    #Resolvemos o problema
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.2f}")
        for i, var in enumerate(vars):
            print(f"x{i} = {var.solution_value():0.2f}")
        #BranchAndBound(solver, vars, bestBranchSolution, c, A, b)
    else:
        print("O problema não possui solução ótima.")
        return None, None

#Diz respeito a parte direita do branch and bound
def BranchRight(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight):
    conditionsL = conditionsLeft.copy()
    conditionsR = conditionsRight.copy()
    #Criamos um novo solver com as mesmas condicoes
    solver, vars = GetNewSolver(c, A, b, conditionsL, conditionsR)
    #Calculamos o piso
    floor = math.floor(decimalVar.solution_value())
    print(f"Adicionando {floor} na condicao")
    #Adicionamos a condição
    solver.Add(decimalVar <= floor)
    conditionsR.append([decimalVar, floor])
    #Resolvemos o problema
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.2f}")
        for i, var in enumerate(vars):
            print(f"x{i} = {var.solution_value():0.2f}")
        #BranchAndBound(solver, vars, bestBranchSolution, c, A, b)
    else:
        print("O problema não possui solução ótima.")
        return None, None

#Função que vai chamar a esquerda e direita
def BranchAndBound(solver, vars, bestBranchSolution, c, A, b, conditionsLeft, conditionsRight):
    bestBranchSolution = solver.Objective().Value()
    decimalVar = getDecimalVar(vars)
    BranchLeft(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight)
    BranchRight(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight)
    if(checkIntegrability(vars)):
        print("Poda por Integrabilidade")
    

solver, vars = PLSolver(c, A, b)
BranchAndBound(solver, vars, 0, c, A, b, [], [])
for i in range(len(vars)):
    print(vars[i].solution_value())