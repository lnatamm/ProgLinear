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

Capacidade = [
#                            |D|     |D|
#                    |R|     |ó|     |ó|
#                    |i|     |l|     |l|
#            |R|     |n|     |a|     |a|             |L|
#    |I|     |ú|     |g|     |r|     |r|     |E|     |i|     |P|
#    |e|     |p|     |g|     | |     | |     |u|     |b|     |e|
#    |n|     |i|     |i|     |N|     |C|     |r|     |r|     |s|
#    |e|     |a|     |t|     |A|     |A|     |o|     |a|     |o|
    [INF,     5,      5,      2,      2,      2,      2,      4    ], #Iene
    [5,       INF,    2,     0.2,    0.2,     1,     0.5,    0.2  ], #Rúpia
    [3,       4.5,   INF,    1.5,    1.5,     2.5,    1,      1    ]  #Ringgit
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
    for i in range(3):
        for j in range(n):
            print(f"{vars[i][j]} <= {Capacidade[i][j]}")
            solver.Add(vars[i][j] <= Capacidade[i][j])
    #Fontes
    solver.Add(vars[0][3] + vars[0][4] + vars[0][5] + vars[0][6] + vars[0][7] - 9.6 == 0) #Iene
    solver.Add(vars[1][3] + vars[1][4] + vars[1][5] + vars[1][6] + vars[1][7] - 1.68 == 0)#Rupia
    solver.Add(vars[2][3] + vars[2][4] + vars[2][5] + vars[2][6] + vars[2][7] - 5.6 == 0) #Riggit
    #Sumidouro
    solver.Add(16.88 - vars[0][3] - vars[1][3] - vars[2][3] - vars[4][3] - vars[5][3] - vars[6][3] - vars[7][3] == 0)
    #Intermediario
    solver.Add(vars[4][3] + vars[4][5] + vars[4][6] + vars[4][7] - vars[0][4] - vars[1][4] - vars[2][4] - vars[5][4] - vars[6][4] - vars[7][4] == 0)
    solver.Add(vars[5][3] + vars[5][4] + vars[5][6] + vars[5][7] - vars[0][5] - vars[1][5] - vars[2][5] - vars[4][5] - vars[6][5] - vars[7][5] == 0)
    solver.Add(vars[6][3] + vars[6][4] + vars[6][5] + vars[6][7] - vars[0][6] - vars[1][6] - vars[2][6] - vars[4][6] - vars[5][6] - vars[7][6] == 0)
    solver.Add(vars[7][3] + vars[7][4] + vars[7][5] + vars[7][6] - vars[0][7] - vars[1][7] - vars[2][7] - vars[4][7] - vars[5][7] - vars[6][7] == 0)

    #Resolvemos o problema
    viable = solver.Solve()
    if viable == pywraplp.Solver.OPTIMAL:
        print("Solução:")
        print(f"Função Objetivo = {solver.Objective().Value():0.4f}")
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
        print(f"Iene para Rupiah: x[0][1] - {vars[0][1].solution_value()} <= {Capacidade[0][1]} Cost: {Custos[0][1]}")
        print(f"Iene para Ringgit: x[0][2] - {vars[0][2].solution_value()} <= {Capacidade[0][2]} Cost: {Custos[0][2]}")
        print(f"Iene para Canadian: x[0][4] - {vars[0][4].solution_value()} <= {Capacidade[0][4]} Cost: {Custos[0][4]}")
        print(f"Iene para Euro: x[0][5] - {vars[0][5].solution_value()} <= {Capacidade[0][5]} Cost: {Custos[0][5]}")
        print(f"Iene para Libra: x[0][6] - {vars[0][6].solution_value()} <= {Capacidade[0][6]} Cost: {Custos[0][6]}")
        print(f"Iene para Peso: x[0][7] - {vars[0][7].solution_value()} <= {Capacidade[0][7]} Cost: {Custos[0][7]}")
        print(f"Iene para Dólar: x[0][3] - {vars[0][3].solution_value()} <= {Capacidade[0][3]} Cost: {Custos[0][3]}")
        print("--------------------------------------------------------------------------")
        print(f"Rupiah para Iene: x[0][1] - {vars[1][0].solution_value()} <= {Capacidade[1][0]} Cost: {Custos[1][0]}")
        print(f"Rupiah para Ringgit: x[0][2] - {vars[1][2].solution_value()} <= {Capacidade[1][2]} Cost: {Custos[1][2]}")
        print(f"Rupiah para Canadian: x[0][4] - {vars[1][4].solution_value()} <= {Capacidade[1][4]} Cost: {Custos[1][4]}")
        print(f"Rupiah para Euro: x[0][5] - {vars[1][5].solution_value()} <= {Capacidade[1][5]} Cost: {Custos[1][5]}")
        print(f"Rupiah para Libra: x[0][6] - {vars[1][6].solution_value()} <= {Capacidade[1][6]} Cost: {Custos[1][6]}")
        print(f"Rupiah para Peso: x[0][7] - {vars[1][7].solution_value()} <= {Capacidade[1][7]} Cost: {Custos[1][7]}")
        print(f"Rupiah para Dólar: x[0][3] - {vars[1][3].solution_value()} <= {Capacidade[1][3]} Cost: {Custos[1][3]}")
        print("--------------------------------------------------------------------------")
        print(f"Ringgt para Iene: x[0][1] - {vars[2][0].solution_value()} <= {Capacidade[2][0]} Cost: {Custos[2][0]}")
        print(f"Ringgt para Rupiah: x[0][2] - {vars[2][1].solution_value()} <= {Capacidade[2][1]} Cost: {Custos[2][1]}")
        print(f"Ringgt para Canadian: x[0][4] - {vars[2][4].solution_value()} <= {Capacidade[2][4]} Cost: {Custos[2][4]}")
        print(f"Ringgt para Euro: x[0][5] - {vars[2][5].solution_value()} <= {Capacidade[2][5]} Cost: {Custos[2][5]}")
        print(f"Ringgt para Libra: x[0][6] - {vars[2][6].solution_value()} <= {Capacidade[2][6]} Cost: {Custos[2][6]}")
        print(f"Ringgt para Peso: x[0][7] - {vars[2][7].solution_value()} <= {Capacidade[2][7]} Cost: {Custos[2][7]}")
        print(f"Ringgt para Dólar: x[0][3] - {vars[2][3].solution_value()} <= {Capacidade[2][3]} Cost: {Custos[2][3]}")
        print("--------------------------------------------------------------------------")
        print(f"Canadian para Dólar x[4][3] - {vars[4][3].solution_value()}")
        print(f"Euro para Dólar x[5][3] - {vars[5][3].solution_value()}")
        print(f"Libra para Dólar x[6][3] - {vars[6][3].solution_value()}")
        print(f"Peso para Dólar x[7][3] - {vars[7][3].solution_value()}")
    else:
        print("Solução inviável")

Flux(Custos, Capacidade)