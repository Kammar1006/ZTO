import numpy as np
from RandomNumberGenerator import RandomNumberGenerator
import subprocess
import re
import matplotlib.pyplot as plt

rng = RandomNumberGenerator(1232423222)

def run(n, path):
    runNumbers(n)
    return runCplex(path)

def runNumbers(n):
    a = n * [0]
    b = n * [0]
    r = n * [0]

    f = n * [n * [0]]

    for i in range(n):
        a[i] = rng.nextFloat(10, 70)
        b[i] = rng.nextFloat(10, 70)
        r[i] = rng.nextFloat(1, 8)

    for i in range(n):
        for j in range(n):
            if i == j:
                f[i][j] = 0
            else:
                f[i][j] = rng.nextFloat(1, 20)

    lines = []
    lines.append("n = " + str(n) + ";\n")
    lines.append("a = " + str(a) + ";\n")

    lines.append("b =" + str(b) + ";\n")
    lines.append("r =" + str(r) + ";\n")
    lines.append("f =" + str(f) + ";\n")

    with open("C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/5.2/5.2.dat", "w", encoding="utf-8") as file:
        file.writelines(lines)

def runCplex(dp):

    result = subprocess.run(
        ["oplrun", "C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/5.2/5.2.mod", dp],
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

def generate_nm(n_max, step):
    n_vals = np.arange(step, n_max + 1, step)

    N = np.meshgrid(n_vals)

    return N.flatten()

def runMain():
    #n = [10,10,10,10,10,10,10,10,10,10, 20,20,20,20,20,30,30,30,40,40,50,50]
    #m = [10,20,30,40,50,60,70,80,90,100,10,20,30,40,50,10,20,30,10,20,10,20]
    #n = np.linspace(1, 100, 100)
    #m = np.linspace(1, 100, 100)
    n = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    t = []

    for i in range(len(n)):
        ni = int(n[i])
        if ni > 40:
            wynik = 0
        else:
            wynik = run(
                ni,
                "C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/5.2/5.2.dat"
            )
            print(ni, wynik)
        t.append(wynik)

    print(n)
    print(t)

    plt.scatter(n, t)
    plt.grid()
    plt.xlabel("n")
    plt.ylabel("t*100")
    plt.savefig('zadanie_5_2.png')
    plt.show()

runMain()

#run(20, "C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/5.2/5.2.dat")

