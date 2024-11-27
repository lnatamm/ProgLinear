from ortools.linear_solver import pywraplp
import math
c = [3, 5]
A = [
    [2, 4],
    [1, 0],
    [0, 2]
]
b = [25, 8, 10]
negInf = -999999

#Apenas printa uma linha
def bigPrint():
    print("----------------------------------------------------------------------")

#Função que cria o solver para garantir que as condições sejam exclusivas para cada branch
def GetNewSolver(c, A, b, conditionsLeft, conditionsRight):
    #Cria um solver utilizando o "GLOP" para problemas de otimização reais
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    m = len(A)
    # Definição de Variáveis
    vars = []
    for i in range(len(c)):
        vars.append(solver.NumVar(0, solver.infinity(), f"x{i}"))
    #Função Objetivo de Maximização
    solver.Maximize(solver.Sum(c[i]*vars[i] for i in range(len(c))))
    #Condições
    for i in range(m):
        solver.Add(solver.Sum(A[i][j]*vars[j] for j in range(len(A[i]))) <= b[i])
    #Parte exclusiva do Branch and Bound para salvar as condições que foram feitas em cada branch
    #já que para cada execução do Branch and Bound nós criamos um solver novo
    if(conditionsLeft):
        for i in range(len(conditionsLeft)):
            solver.Add(conditionsLeft[i][0] >= conditionsLeft[i][1])
    if(conditionsRight):
        for i in range(len(conditionsRight)):
            solver.Add(conditionsRight[i][0] <= conditionsRight[i][1])

    return solver, vars

#Função que resolve o problema e posteriormente vai chamar o Branch and Bound
def PLSolver(c, A, b):
    #Inicialização do Solver
    solver, vars = GetNewSolver(c, A, b, 0, 0)
    if not solver:
        return
    #Resolvemos o problema
    viable = solver.Solve()
    if viable == pywraplp.Solver.OPTIMAL:
        bigPrint()
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.2f}")
        for i, var in enumerate(vars):
            print(f"x{i} = {var.solution_value():0.2f}")
        print("Iniciando o Branch and Bound")
        bigPrint()
        #Chamamos o Branch and Bound para procurar uma solução inteira
        return BranchAndBound(solver, vars, [[negInf]], c, A, b, [], [], [0])
    else:
        print("O problema não possui solução ótima.")
        bigPrint()
        return None

#Função que faz a verificação de se todas as variáveis são inteiras
def checkIntegrability(vars):
    for i in range(len(vars)):
        if(not round(vars[i].solution_value(), 3).is_integer()):
            return False
    return True

#Função que retorna a variável decimal a ser trabalhada
def getDecimalVar(vars):
    for i in range(len(vars)):
        if(not vars[i].solution_value().is_integer()):
            return vars[i]
    return None

#Rotina de execução do Branch and Bound. LorR é uma flag que indica se a execução é da esquerda ou direita
def Branch(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight, Pn, LorR):
    #Atualizamos o valor de Pn (Está armazenado em um array para que seu valor seja passado por referência em vez de valor)
    Pn[0] += 1
    #Fazemos uma cópia de cada condição para pegar apenas o valor e não a referência do array
    conditionsL = conditionsLeft.copy()
    conditionsR = conditionsRight.copy()
    #Criamos um novo solver com as mesmas condições
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
    print(f"Maior F.O Atual: {"Ainda não foi encontrada uma solução inteira" if bestBranchSolution[0][0] == negInf else bestBranchSolution[0][0]}")
    print(f"Subproblema: P{Pn[0]}")
    if viable == pywraplp.Solver.OPTIMAL:
        objectiveValue = round(solver.Objective().Value(), 3)
        #Verificamos se a solução é inteira
        integrability = checkIntegrability(vars)
        #Verificamos se o valor da função objetiva é melhor que o último valor encontrado em uma solução inteira
        optimality = (bestBranchSolution[0][0] >= objectiveValue)
        #Array que irá salvar os nomes e valores das variáveis caso seja uma solução inteira
        varsValues = []
        print(f"Função Objetivo = {objectiveValue:0.2f}")
        print(f"Solução:")
        for i, var in enumerate(vars):
            print(f"x{i} = {var.solution_value():0.2f}")
            varsValues.append([f"x{i}", round(var.solution_value(), 3)])
        if(optimality):
            print("Poda por Optimalidade")
            bigPrint()
        elif(integrability):
            print(f"Poda por Integrabilidade")
            #Atualizamos a melhor solução inteira
            bestBranchSolution[0] = [objectiveValue, varsValues]
            print(f"Nova solução inteira encontrada! Valor da F.O: {bestBranchSolution[0][0]}")
            bigPrint()
        else:
            bigPrint()
            #Caso ainda não tenhamos encontrado uma solução inteira, executamos o Branch and Bound novamente
            BranchAndBound(solver, vars, bestBranchSolution, c, A, b, conditionsL, conditionsR, Pn)
    else:
        print("Poda por Inviabilidade")
        bigPrint()

#Função que vai chamar as rotinas da esquerda e direita do Branch and Bound
def BranchAndBound(solver, vars, bestBranchSolution, c, A, b, conditionsLeft, conditionsRight, Pn):
    decimalVar = getDecimalVar(vars)
    Branch(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight, Pn, 0)
    Branch(bestBranchSolution, decimalVar, c, A, b, conditionsLeft, conditionsRight, Pn, 1)
    return bestBranchSolution[0]

#Chamada do método principal
bestSolution = PLSolver(c, A, b)
if(bestSolution):
    print(f"Solução ótima")
    print(f"Função Objetivo: {bestSolution[0]}")
    print(f"Solução:")
    for i in range(len(bestSolution[1])):
        print(f"{bestSolution[1][i][0]} = {bestSolution[1][i][1]}")
    bigPrint()