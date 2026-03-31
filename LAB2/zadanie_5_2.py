from RandomNumberGenerator import RandomNumberGenerator

rng = RandomNumberGenerator(1232423222)

n = 10
a = n*[0]
b = n*[0]
r = n*[0]

f = n*[n*[0]]

for i in range(n):
    a[i] = rng.nextFloat(10,70)
    b[i] = rng.nextFloat(10, 70)
    r[i] = rng.nextFloat(1, 8)

for i in range(n):
    for j in range(n):
        if i == j:
            f[i][j] = 0
        else:
            f[i][j] = rng.nextFloat(1,20)

lines = []
lines.append("n = "+str(n)+";\n")
lines.append("a = "+str(a)+";\n")

lines.append("b ="+str(b)+";\n")
lines.append("r ="+str(r)+";\n")
lines.append("f ="+ str(f)+";\n")

with open("C:/Politechnika/Semestr_1_MGR/Optymalizacja/Lab2_Ilog/5.2/5.2.dat", "w", encoding="utf-8") as file:
    file.writelines(lines)