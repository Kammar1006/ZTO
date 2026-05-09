from RandomNumberGenerator import RandomNumberGenerator
import matplotlib.pyplot as plt
from docplex.mp.model import Model
import cplex
import time

# generator liczb losowych
rng = RandomNumberGenerator(231232323)

def generate(n):
    a = []
    b = []
    r = []
    for i in range(n):
        a.append(rng.nextFloat(10,70))
        b.append(rng.nextFloat(10,70))
        r.append(rng.nextFloat(1,8))
    x0 = rng.nextFloat(10,70)
    y0 = rng.nextFloat(10,70)
    return a,b,r,x0,y0

def solve(n,a,b,r,x0,y0):

    m = Model("zad_5_1")

    x = [m.continuous_var(lb=0, name=f"x[{i}]") for i in range(n)]
    y = [m.continuous_var(lb=0, name=f"y[{i}]") for i in range(n)]

    m.minimize(
        m.abs(x[0] - x0) + m.abs(y[0] - y0)+
        m.sum(m.abs(x[i]-x[i-1])+m.abs(y[i]-y[i-1]) for i in range(1, n))+
        m.abs(x[n-1] - x0) + m.abs(y[n-1] - y0)
    )

    for i in range(n):
        m.add_constraint(m.abs(x[i]-a[i])+m.abs(y[i]-b[i]) <= r[i])

    start = time.time()
    m.solve()
    end = time.time()
    m.print_solution()

    return round(end-start,4)

def solver(n):
    a, b, r, x0, y0 = generate(n)
    return solve(n,a,b,r,x0,y0)

# główny program
times1 = []
times2 = []
times3 = []
times4 = []
times5 = []
n = []
for i in range(3, 50):
    print("n =",i)
    times1.append(solver(i))
    times2.append(solver(i))
    times3.append(solver(i))
    times4.append(solver(i))
    times5.append(solver(i))
    n.append(i)
    print(f"times1: {times1[-1]:.3f}")
    print(f"times2: {times2[-1]:.3f}")
    print(f"times3: {times3[-1]:.3f}")
    print(f"times4: {times4[-1]:.3f}")
    print(f"times5: {times5[-1]:.3f}")
#print(times)

plt.subplot(1,2,1)
#plt.yscale("log")
plt.scatter(n, times1, label="1")
plt.scatter(n, times2, label="2")
plt.scatter(n, times3, label="3")
plt.scatter(n, times4, label="4")
plt.scatter(n, times5, label="5")
plt.title("5.1 Problem inspekcji")
plt.grid(True)
plt.xlabel("n")
plt.ylabel("time [s]")
plt.legend(title="Powtórzenia")

# Średnia z pięciu powtórzeń
times = []
for i in range(len(times1)):
    times.append((times1[i]+times2[i]+times3[i]+times4[i]+times5[i])/5)

plt.subplot(1,2,2)
#plt.yscale("log")
plt.scatter(n, times)
plt.title("5.1 Problem inspekcji (Średnia z 5)")
plt.grid(True)
plt.xlabel("n")
plt.ylabel("time [s]")


plt.tight_layout()
plt.savefig("Zadanie_5_1.png")
plt.show()