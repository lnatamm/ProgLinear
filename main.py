from ortools.linear_solver import pywraplp
import math
c = [1, 2]
A = [
    [1, 2],
    [3, 4]
]
b = [5, 6]
negInf = -999999

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
        for i in range(len(conditionsLeft)):
            solver.Add(conditionsLeft[i][0] >= conditionsLeft[i][1])
    if(conditionsRight):
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
        print("-----------------")
        return solver, vars
    else:
        print("O problema não possui solução ótima.")
        print("-----------------")
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

def GetBestSolution(integerSolutions):
    bestSolution = negInf
    for solution in integerSolutions:
        if(solution > bestSolution):
            bestSolution = solution
    return bestSolution

def Branch(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight, integerSolutions, Pn, LorR):
    conditionsL = conditionsLeft.copy()
    conditionsR = conditionsRight.copy()
    #Criamos um novo solver com as mesmas condicoes
    solver, vars = GetNewSolver(c, A, b, conditionsL, conditionsR)
    if(LorR == 0): #Branch da Esquerda
        #Calculamos o teto
        ceil = math.ceil(decimalVar.solution_value())
        #Adicionamos a condição
        print(f"Adicionando {decimalVar} >= {ceil} na condicao")
        solver.Add(decimalVar >= ceil)
        conditionsL.append([decimalVar, ceil])
    else: #Branch da Direita
        #Calculamos o piso
        floor = math.floor(decimalVar.solution_value())
        print(f"Adicionando {decimalVar} <= {floor} na condicao")
        #Adicionamos a condição
        solver.Add(decimalVar <= floor)
        conditionsR.append([decimalVar, floor])
    
    #Resolvemos o problema
    viable = solver.Solve()

    print(f"Subproblema: P{Pn}")
    if viable == pywraplp.Solver.OPTIMAL:
        objectiveValue = solver.Objective().Value()
        integrability = checkIntegrability(vars)
        optimality = (bestBranchSolution >= objectiveValue) and integerSolutions
        if(bestBranchSolution == negInf):
            bestBranchSolution = objectiveValue
        print(f"Função Objetivo = {objectiveValue:0.2f}")
        print(f"Solução:")
        for i, var in enumerate(vars):
            print(f"x{i} = {var.solution_value():0.2f}")
        if(integrability):
            print(f"Poda por integrabilidade")
            print("-----------------")
            integerSolutions.append(objectiveValue)
        elif(optimality):
            print("Poda por optimalidade")
            print("-----------------")
        else:
            print("-----------------")
            BranchAndBound(solver, vars, bestBranchSolution, c, A, b, conditionsL, conditionsR, integerSolutions, Pn)
    else:
        print("Poda por inviabilidade")
        print("-----------------")

#Função que vai chamar a esquerda e direita
def BranchAndBound(solver, vars, bestBranchSolution, c, A, b, conditionsLeft, conditionsRight, integerSolutions, Pn):
    decimalVar = getDecimalVar(vars)
    Branch(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight, integerSolutions, Pn+1, 0)
    Branch(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight, integerSolutions, Pn+2, 1)
    return GetBestSolution(integerSolutions)

solver, vars = PLSolver(c, A, b)
bestSolution = BranchAndBound(solver, vars, negInf, c, A, b, [], [], [],0)
print(f"Melhor solução inteira: {bestSolution}")