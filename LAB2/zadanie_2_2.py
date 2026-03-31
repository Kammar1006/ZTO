import numpy as np
from RandomNumberGenerator import RandomNumberGenerator
import subprocess
import re

rng = RandomNumberGenerator(1232423222)

def run(n, m, path):
    runNumbers(n, m)
    return runCplex(path)

def runNumbers(n, m):
    # n * m <= 1000
    # n <= m

    S = []
    D = []
    s = 0
    d = 0

    for i in range(n):
        val = rng.nextInt(1,20)
        S.append(val)
        s = s+val

    for j in range(m):
        val = rng.nextInt(1,20)
        D.append(val)
        d = d+val

    while s < d:
        i = rng.nextInt(0,n-1)
        S[i] = S[i]+1
        s=s+1
    while d < s:
        i = rng.nextInt(0,m-1)
        D[i] = D[i]+1
        d=d+1

    k = n*[m*[1]]
    for i in range(n):
        for j in range(m):
            k[i][j] = rng.nextInt(1, 10)
    print(k)
    print(s,d)

    lines = []
    lines.append("n = "+str(n)+";\n")
    lines.append("m = "+str(m)+";\n")

    lines.append("S ="+str(S)+";\n")
    lines.append("D ="+str(D)+";\n")
    lines.append("k ="+ str(k)+";\n")

    with open("C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/2.2/2.2.dat", "w", encoding="utf-8") as file:
        file.writelines(lines)

def runCplex(dp):

    result = subprocess.run(
        ["oplrun", "C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/2.2/2.2.mod", dp],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)

    out = result.stdout + result.stderr

    match = re.search(r"Total .* \(([\d,]+) ticks\)", out)

    if not match:
        raise Exception("Nie znaleziono TOTAL ticks!")

    print(match.group(1))
    ticks = int(float(match.group(1).replace(",", ".")) * 100)

    print(ticks)
    return ticks

def generate_nm(n_max, m_max, step):
    n_vals = np.arange(step, n_max + 1, step)
    m_vals = np.arange(step, m_max + 1, step)

    N, M = np.meshgrid(n_vals, m_vals)

    return N.flatten(), M.flatten()

def runMain():
    #n = [10,10,10,10,10,10,10,10,10,10, 20,20,20,20,20,30,30,30,40,40,50,50]
    #m = [10,20,30,40,50,60,70,80,90,100,10,20,30,40,50,10,20,30,10,20,10,20]
    #n = np.linspace(1, 100, 100)
    #m = np.linspace(1, 100, 100)
    n, m = generate_nm(100, 100, 2)
    t = []

    for i in range(len(n)):
        ni = int(n[i])
        mi = int(m[i])
        if ni*mi > 1000:
            wynik = 0
        else:
            wynik = run(
                ni,
                mi,
                "C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/2.2/2.2.dat"
            )
            print(wynik)
        t.append(wynik)

    print(n.tolist())
    print(m.tolist())
    print(t)

runMain()

#run(20, 50, "C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/2.2/2.2.dat")