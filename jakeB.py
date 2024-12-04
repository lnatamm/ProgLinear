from ortools.linear_solver import pywraplp

INF = 999999

Taxas = [
#                                            |D|         |D|
#                                |R|         |ó|         |ó|
#                                |i|         |l|         |l|
#                    |R|         |n|         |a|         |a|                     |L|  
#        |I|         |ú|         |g|         |r|         |r|         |E|         |i|         |P|
#        |e|         |p|         |g|         | |         | |         |u|         |b|         |e|
#        |n|         |i|         |i|         |N|         |C|         |r|         |r|         |s|
#        |e|         |a|         |t|         |A|         |A|         |o|         |a|         |o|
    [ 1.000000,   50.00000,   0.040000,   0.008000,   0.010000,   0.006400,   0.004800,   0.076800 ], #Iene 0
    [ 50.00000,   1.000000,   0.000800,   0.000160,   0.000200,   0.000128,   0.000096,   0.001536 ], #Rúpia 1
    [ 0.040000,   0.000800,   1.000000,   0.200000,   0.250000,   0.160000,   0.120000,   1.920000 ], #Ringgit 2
    [ 0.008000,   0.000160,   0.200000,   1.000000,   1.250000,   0.800000,   0.600000,   9.600000 ], #Dólar Norte Americano 3
    [ 0.010000,   0.000200,   0.250000,   1.250000,   1.000000,   0.640000,   0.480000,   7.680000 ], #Dólar Canadense 4
    [ 0.006400,   0.000128,   0.160000,   0.800000,   0.640000,   1.000000,   0.750000,   12.00000 ], #Euro 5
    [ 0.004800,   0.000096,   0.120000,   0.600000,   0.480000,   0.750000,   1.000000,   16.00000 ], #Libra 6
    [ 0.076800,   0.001536,   1.920000,   9.600000,   7.680000,   12.00000,   16.00000,   1.000000 ]  #Peso 7
]

Custos = [
#                                          |D|       |D|  
#                                |R|       |ó|       |ó|  
#                                |i|       |l|       |l|  
#    |D|               |R|       |n|       |a|       |a|                 |L|  
#    |u|     |I|       |ú|       |g|       |r|       |r|       |E|       |i|       |P|
#    |m|     |e|       |p|       |g|       | |       | |       |u|       |b|       |e|
#    |m|     |n|       |i|       |i|       |N|       |C|       |r|       |r|       |s|
#    |y|     |e|       |a|       |t|       |A|       |A|       |o|       |a|       |o|
    [ 0,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000 ], #Dummy
    [ 0,   0.0000,   0.0050,   0.0050,   0.0040,   0.0040,   0.0040,   0.0025,   0.0050 ], #Iene 1
    [ 0,   0.0050,   0.0000,   0.0070,   0.0050,   0.0030,   0.0030,   0.0075,   0.0075 ], #Rúpia 2
    [ 0,   0.0050,   0.0070,   0.0000,   0.0070,   0.0070,   0.0040,   0.0045,   0.0050 ], #Ringgit 3
    [ 0,   0.0040,   0.0050,   0.0070,   0.0000,   0.0005,   0.0010,   0.0010,   0.0010 ], #Dólar Norte Americano 4
    [ 0,   0.0040,   0.0030,   0.0070,   0.0005,   0.0000,   0.0020,   0.0010,   0.0010 ], #Dólar Canadense 5
    [ 0,   0.0040,   0.0030,   0.0040,   0.0010,   0.0020,   0.0000,   0.0005,   0.0050 ], #Euro 6
    [ 0,   0.0025,   0.0075,   0.0045,   0.0010,   0.0010,   0.0005,   0.0000,   0.0050 ], #Libra 7
    [ 0,   0.0050,   0.0075,   0.0050,   0.0010,   0.0010,   0.0050,   0.0050,   0.0000 ]  #Peso 8
]

Capacidade = [
#                                   |D|     |D|
#                           |R|     |ó|     |ó|
#                           |i|     |l|     |l|
#    |D|            |R|     |n|     |a|     |a|             |L|
#    |u|    |I|     |ú|     |g|     |r|     |r|     |E|     |i|     |P|
#    |m|    |e|     |p|     |g|     | |     | |     |u|     |b|     |e|
#    |m|    |n|     |i|     |i|     |N|     |C|     |r|     |r|     |s|
#    |y|    |e|     |a|     |t|     |A|     |A|     |o|     |a|     |o|
    [ INF,  9.6,    1.68,   5.6,     0,      0,      0,      0,      0 ], #Dummy
    [ 0,    INF,    5,      5,       2,      2,      2,      2,      4 ], #Iene
    [ 0,    5,      INF,    2,      0.2,     200,    1,      0.5,    0.2  ], #Rúpia
    [ 0,    3,      4.5,    INF,    1.5,     1.5,   2.5,     1,      1 ]  #Ringgit
]

def Flux(Custos, Capacidade):
    #Cria um solver utilizando o "GLOP" para problemas de otimização reais
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return None
    n = len(Custos)
    # Definição de Variáveis
    vars = []
    for i in range(n):
        vars.append([])
        for j in range(n):
            vars[i].append(solver.NumVar(0, solver.infinity(), f"x{i}{j}"))
        
    #Função Objetivo de Minimização
    solver.Minimize(solver.Sum(Custos[i][j]*vars[i][j] for i in range(n) for j in range(n)))
    #print(solver.Sum(Custos[i][j]*vars[i][j] for i in range(n) for j in range(n)))
    #Condições:
    #Capacidade das arestas
    for i in range(4):
        for j in range(n):
            print(f"{vars[i][j]} <= {Capacidade[i][j]}")
            solver.Add(vars[i][j] <= Capacidade[i][j])

    # solver.Add(vars[5][4] <= INF)
    # solver.Add(vars[6][4] <= INF)
    # solver.Add(vars[7][4] <= INF)
    # solver.Add(vars[8][4] <= INF)
    # #Balanço de fluxo
    # #Fontes
    # solver.Add(vars[0][1] + vars[0][2] + vars[0][3] - 16.88 == 0)
    # #Sumidouro
    # solver.Add(16.88 - vars[1][4] - vars[2][4] - vars[3][4] - vars[5][4] - vars[6][4] - vars[7][4] - vars[8][4] == 0)
    # #"Fontes"
    # solver.Add(vars[1][2] + vars[1][3] + vars[1][4] + vars[1][5] + vars[1][6] + vars[1][7] + vars[1][8] - vars[0][1] - vars[2][1] - vars[3][1] == 0)
    # solver.Add(vars[2][1] + vars[2][3] + vars[2][4] + vars[2][5] + vars[2][6] + vars[2][7] + vars[2][8] - vars[0][2] - vars[1][2] - vars[3][2] == 0)
    # solver.Add(vars[3][1] + vars[3][2] + vars[3][4] + vars[3][5] + vars[3][6] + vars[3][7] + vars[3][8] - vars[0][3] - vars[1][3] - vars[2][3] == 0)
    # #Intermediarios
    # solver.Add(vars[5][4] + vars[5][6] + vars[5][7] + vars[5][8] - vars[1][5] - vars[2][5] - vars[3][5] - vars[6][5] - vars[7][5] - vars[8][5] == 0)
    # solver.Add(vars[6][4] + vars[6][5] + vars[6][7] + vars[6][8] - vars[1][6] - vars[2][6] - vars[3][6] - vars[5][6] - vars[7][6] - vars[8][6] == 0)
    # solver.Add(vars[7][4] + vars[7][5] + vars[7][6] + vars[7][8] - vars[1][7] - vars[2][7] - vars[3][7] - vars[5][7] - vars[6][7] - vars[8][7] == 0)
    # solver.Add(vars[8][4] + vars[8][5] + vars[8][6] + vars[8][7] - vars[1][8] - vars[2][8] - vars[3][8] - vars[5][8] - vars[6][8] - vars[7][8] == 0)
    #Balancoooo
    #Resolvemos o problema
    viable = solver.Solve()
    if viable == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.5f}")
        # print("Conversões de Iene:")
        # for i in range(1, n):
        #     print(f"{vars[1][i]} = {vars[1][i].solution_value():0.2f}")
        # print("Conversões de Rúpia")
        # for i in range(1, n):
        #     print(f"{vars[2][i]} = {vars[2][i].solution_value():0.2f}")
        # print("Conversões de Ringgit")
        # for i in range(1, n):
        #     print(f"{vars[2][i]} = {vars[2][i].solution_value():0.2f}")
        # print("Conversões Intermédio")
        # for i in range(1, n):
        #     print(f"{vars[i][4]} = {vars[i][4].solution_value():0.2f}")
        # for i in range(n):
        #     for j in range(n):
        #         print(f"{vars[i][j]} = {vars[i][j].solution_value():0.2f}")
    else:
        print("Solução inviável")

Flux(Custos, Capacidade)