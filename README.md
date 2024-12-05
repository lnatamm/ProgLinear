# ProgLinear
Exercícios de programação linear resolvidos utilizando a biblioteca ortools

## Running

### Branch and Bound:

Abra a pasta "Branch and Bound", altere o conteúdo do arquivo LP.txt da seguinte maneira:
<pre>
𝑛 𝑚, o número de variáveis e o número de condições, respectivamente
𝑐1 𝑐2… 𝑐𝑛, o vetor dos coeficientes do problema
𝑎11 𝑎12… 𝑎1𝑛 𝑎1𝑛+1𝑏1
𝑎21 𝑎22… 𝑎2𝑛 𝑎2𝑛+1𝑏2
.                                     Os coeficientes e os termos independentes das condições
.                                     Ex: 𝑎11 + 𝑎12… + 𝑎1𝑛 = 𝑎1𝑛+1𝑏1
.
𝑎𝑚1 𝑎𝑚2… 𝑎𝑚𝑛 𝑎𝑚𝑛+1𝑏𝑚
</pre>

No exemplo padrão do LP.txt temos:
<pre>
2 3
3 5
2 4 25
1 0 8
0 2 10

2 variáveis, 3 condições  
Função objetivo: 3𝑥1 + 5𝑥2
Condições:
2𝑥1 + 4𝑥2 = 25
1𝑥1 + 0𝑥2 = 8
0𝑥1 + 2𝑥2 = 10
</pre>

!! O solver utiliza como padrão problemas de maximização e condições 𝐴𝑥 = 𝑏.  
Para problemas de minimização, altere a linha 45 para:

    solver.Maximize(solver.Sum(c[i]*vars[i] for i in range(len(c))))
Para condições de ≤ ou ≥, altere a linha 48 para:

    solver.Add(solver.Sum(A[i][j]*vars[j] for j in range(len(A[i]))) <= b[i])
ou

    solver.Add(solver.Sum(A[i][j]*vars[j] for j in range(len(A[i]))) >= b[i])

Por fim, execute o comando:


    py main.py

### Problema de Jake Nguienes

Abra a pasta "Problema de Jake Nguienes".

Para o item B execute o comando:

    py jakeB.py

Para o item C execute o comando:

    py jakeC.py

Para o item D execute o comando:

    py jakeD.py