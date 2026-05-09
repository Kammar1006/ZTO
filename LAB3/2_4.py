from RandomNumberGenerator import RandomNumberGenerator
import matplotlib.pyplot as plt
from docplex.mp.model import Model
import cplex
import time

# generator liczb losowych
rng = RandomNumberGenerator(231232323)

def to_list(x):
    tab_values = [[x[i][j].solution_value for i in range(len(x))] for j in range(len(x[0]))]
    return tab_values

# Generacja instancji
def generate(n):
    w = [[0 for i in range(n)] for j in range(n)]
    d = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                w[i][j] = 0
            else:
                w[i][j] = rng.nextInt(1, 50)

    for l in range(n):
        for k in range(n):
            if l == k:
                d[l][k] = 0
            else:
                d[l][k] = rng.nextInt(1, 50)

    return w, d


def solver(n):

    #print(n)

    # Wygeneruj dane
    w, d = generate(n)

    start = time.time()

    model = Model(name="test")

    # Zmienne decyzyjne
    x = [[model.binary_var(name=f"x[{i}][{j}]") for i in range(n)] for j in range(n)]

    # Funkcja celu
    model.minimize(model.sum(w[i][j]*d[k][l]*x[i][k]*x[j][l] for i in range(n) for j in range(n) for k in range(n) for l in range(n)))

    # Ograniczenia
    for i in range(n):
        model.add_constraint(model.sum(x[i][j] for j in range(n)) == 1)
        model.add_constraint(model.sum(x[j][i] for j in range(n)) == 1)

    #print(w)
    #print(d)

    model.solve()
    #model.print_solution()
    end = time.time()

    x_val = to_list(x)
    #print(x_val)
    return end-start


# Główna część programu
times1 = []
times2 = []
times3 = []
times4 = []
times5 = []
n = []
for i in range(5, 10):
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
plt.yscale("log")
plt.scatter(n, times1, label="1")
plt.scatter(n, times2, label="2")
plt.scatter(n, times3, label="3")
plt.scatter(n, times4, label="4")
plt.scatter(n, times5, label="5")
plt.title("2.4 Kwadratowe zagadnienie przydziału")
plt.grid(True)
plt.xlabel("n")
plt.ylabel("time [s]")
plt.legend(title="Powtórzenia")

# Średnia z pięciu powtórzeń
times = []
for i in range(len(times1)):
    times.append((times1[i]+times2[i]+times3[i]+times4[i]+times5[i])/5)

plt.subplot(1,2,2)
plt.yscale("log")
plt.scatter(n, times)
plt.title("2.4 Kwadratowe zagadnienie przydziału (Średnia z 5)")
plt.grid(True)
plt.xlabel("n")
plt.ylabel("time [s]")


plt.tight_layout()
plt.savefig("Zadanie_2_4.png")
plt.show()