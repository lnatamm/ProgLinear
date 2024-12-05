from ortools.linear_solver import pywraplp

Costs = [
#                                    |D|       |D|  
#                          |R|       |ó|       |ó|  
#                          |i|       |l|       |l|  
#                |R|       |n|       |a|       |a|                 |L|  
#      |I|       |ú|       |g|       |r|       |r|       |E|       |i|       |P|
#      |e|       |p|       |g|       | |       | |       |u|       |b|       |e|
#      |n|       |i|       |i|       |N|       |C|       |r|       |r|       |s|
#      |e|       |a|       |t|       |A|       |A|       |o|       |a|       |o|
    [ 0.0000,   0.0050,   0.0050,   0.0040,   0.0040,   0.0040,   0.0025,   0.0050 ], #Iene 0
    [ 0.0050,   0.0000,   0.0070,   0.0050,   0.0030,   0.0030,   0.0075,   0.0075 ], #Rúpia 1
    [ 0.0050,   0.0070,   0.0000,   0.0070,   0.0070,   0.0040,   0.0045,   0.0050 ], #Ringgit 2
    [ 0.0040,   0.0050,   0.0070,   0.0000,   0.0005,   0.0010,   0.0010,   0.0010 ], #Dólar Norte Americano 3
    [ 0.0040,   0.0030,   0.0070,   0.0005,   0.0000,   0.0020,   0.0010,   0.0010 ], #Dólar Canadense 4
    [ 0.0040,   0.0030,   0.0040,   0.0010,   0.0020,   0.0000,   0.0005,   0.0050 ], #Euro 5
    [ 0.0025,   0.0075,   0.0045,   0.0010,   0.0010,   0.0005,   0.0000,   0.0050 ], #Libra 6
    [ 0.0050,   0.0075,   0.0050,   0.0010,   0.0010,   0.0050,   0.0050,   0.0000 ]  #Peso 7
]

def Flux(Costs):
    #Cria um solver utilizando o "GLOP" para problemas de otimização reais
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    n = len(Costs)
    #Definição de Variáveis
    x = []
    for i in range(n):
        x.append([])
        for j in range(n):
            x[i].append(solver.NumVar(0, solver.infinity(), f"x{i}{j}"))
        
    #Função Objetivo de Minimização
    solver.Minimize(solver.Sum(Costs[i][j]*x[i][j] for i in range(n) for j in range(n)))
    #Condições:
    #Fontes
    solver.Add(x[0][3] + x[0][4] + x[0][5] + x[0][6] + x[0][7] - 9.6 == 0)  #Iene
    solver.Add(x[1][3] + x[1][4] + x[1][5] + x[1][6] + x[1][7] - 1.68 == 0) #Rupia
    solver.Add(x[2][3] + x[2][4] + x[2][5] + x[2][6] + x[2][7] - 5.6 == 0)  #Riggit
    #Sumidouro
    solver.Add(16.88 - x[0][3] - x[1][3] - x[2][3] - x[4][3] - x[5][3] - x[6][3] - x[7][3] == 0)
    #Intermediario
    solver.Add(x[4][3] + x[4][5] + x[4][6] + x[4][7] - x[0][4] - x[1][4] - x[2][4] - x[5][4] - x[6][4] - x[7][4] == 0)
    solver.Add(x[5][3] + x[5][4] + x[5][6] + x[5][7] - x[0][5] - x[1][5] - x[2][5] - x[4][5] - x[6][5] - x[7][5] == 0)
    solver.Add(x[6][3] + x[6][4] + x[6][5] + x[6][7] - x[0][6] - x[1][6] - x[2][6] - x[4][6] - x[5][6] - x[7][6] == 0)
    solver.Add(x[7][3] + x[7][4] + x[7][5] + x[7][6] - x[0][7] - x[1][7] - x[2][7] - x[4][7] - x[5][7] - x[6][7] == 0)

    #Resolvemos o problema
    viable = solver.Solve()
    if viable == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.4f} milhões de U$")
        print(f"Transações de Ienes (em Milhões de U$)")
        print(f"Iene para Rúpia: {(x[0][1].solution_value()):.2f}")
        print(f"Iene para Ringgit: {(x[0][2].solution_value()):.2f}")
        print(f"Iene para Dólar Canadense: {(x[0][4].solution_value()):.2f}")
        print(f"Iene para Euro: {(x[0][5].solution_value()):.2f}")
        print(f"Iene para Libra: {(x[0][6].solution_value()):.2f}")
        print(f"Iene para Peso: {(x[0][7].solution_value()):.2f}")
        print(f"Iene para Dólar Norte Americano: {(x[0][3].solution_value()):.2f}")
        print("--------------------------------------------------------------------------")
        print("Transações de Rúpia (em Milhões de U$)")
        print(f"Rúpia para Iene: {(x[1][0].solution_value()):.2f}")
        print(f"Rúpia para Ringgit: {(x[1][2].solution_value()):.2f}")
        print(f"Rúpia para Dólar Canadense: {(x[1][4].solution_value()):.2f}")
        print(f"Rúpia para Euro: {(x[1][5].solution_value()):.2f}")
        print(f"Rúpia para Libra: {(x[1][6].solution_value()):.2f}")
        print(f"Rúpia para Peso: {(x[1][7].solution_value()):.2f}")
        print(f"Rúpia para Dólar Norte Americano: {(x[1][3].solution_value()):.2f}")
        print("--------------------------------------------------------------------------")
        print("Transações de Ringgt (em Milhões de U$)")
        print(f"Ringgt para Iene: {(x[2][0].solution_value()):.2f}")
        print(f"Ringgt para Rúpia: {(x[2][1].solution_value()):.2f}")
        print(f"Ringgt para Dólar Canadense: {(x[2][4].solution_value()):.2f}")
        print(f"Ringgt para Euro: {(x[2][5].solution_value()):.2f}")
        print(f"Ringgt para Libra: {(x[2][6].solution_value()):.2f}")
        print(f"Ringgt para Peso: {(x[2][7].solution_value()):.2f}")
        print(f"Ringgt para Dólar Norte Americano: {(x[2][3].solution_value()):.2f}")
        print("--------------------------------------------------------------------------")
        print("Transações Intermediárias (em Milhões de U$)")
        print(f"Dólar Canadense para Dólar Americano {(x[4][3].solution_value()):.2f}")
        print(f"Euro para Dólar Norte Americano {(x[5][3].solution_value()):.2f}")
        print(f"Libra para Dólar Norte Americano {(x[6][3].solution_value()):.2f}")
        print(f"Peso para Dólar Norte Americano {(x[7][3].solution_value()):.2f}")
    else:
        print("Solução inviável")

Flux(Costs)