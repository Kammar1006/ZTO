import math
from queue import PriorityQueue
from RandomNumberGenerator import RandomNumberGenerator
import time

rng = RandomNumberGenerator(1243553533)

class Node:
    def __init__(self, cost, weight):
        self.cost = cost
        self.weight = weight
        self.UB = 0
        self.index = 0
        self.list = []

    def __lt__(self, other):
        return self.UB > other.UB

def calcUB(node, c, w, B):
    betterUB = True

    if betterUB:
        # return node.cost + (B - node.weight) * c[node.index]/w[node.index]
        UB = node.cost
        localW = B - node.weight
        for i in range(node.index, len(c)):
            if localW < w[i]:
                return UB + (w[i] - localW) * c[i]/w[i]

            UB += c[i]
            localW -= w[i]
        return UB

    UB = node.cost
    for i in range(node.index, len(c)):
        UB += c[i]
    return UB

def calcLB(list, c):
    sum = 0
    for item in list:
        sum = sum + c[item]
    return sum

def calcBnB(c, w, B, sb1: float = 1.0, sb2 = False):
    if True: #sb1 == 1 and not sb2:
        LB, best = calcStartLB(c, w, B)
    else:
        LB, best = 0, []

    if sb1 != 1 or sb2:
        LB *= 0.8*sb1
        best = []

    root = Node(0, 0)

    q = PriorityQueue()
    q.put(root)

    while not q.empty():
        node = q.get()
        index = node.index

        if index == len(c):
            localLB = calcLB(node.list, c)
            if localLB > LB:
                LB = localLB
                best = node.list
            continue
        # V

        if(node.weight + w[index] <= B):
            node1 = Node(
                node.cost + c[index],
                node.weight + w[index]
            )
            node1.list = node.list + [index]
            node1.index = index+1
            node1.UB = calcUB(node1, c, w, B)
            if node1.UB*sb1 >= LB:
                q.put(node1)

                if sb2:
                    continue
        # X
        node2 = Node(node.cost, node.weight)
        node2.list = node.list
        node2.index = index+1
        node2.UB = calcUB(node2, c, w, B)
        if node2.UB*sb1 >= LB:
            q.put(node2)


    return LB, best

def calcStartLB(c, w, B):
    cw = 0
    cc = 0
    chosen = []

    for i, (a, b) in enumerate(zip(c, w)):
        if cw + b <= B:
            cw += b
            cc += a
            chosen.append(i)

    return cc, chosen

def generate_data_2_5(n):
    c = []
    w = []

    S = 0
    for i in range(n):
        c.append(rng.nextInt(1, 10))
        w.append(rng.nextInt(1, 10))
        S = S + w[i]
    B = rng.nextInt(math.floor(S / 4), math.floor(S / 2))
    return c,w,B

def mySort(c, w):
    bw = []
    bc = []
    r = [a / b for a, b in zip(c, w)]
    i = [i for i in range(len(c))]
    i.sort(key=lambda i: r[i], reverse=True)

    for item in i:
        bc.append(c[item])
        bw.append(w[item])

    return bc, bw



n = 70
c,w,B = generate_data_2_5(n)

bc, bw = mySort(c, w)

print("c= ",bc)
print("w= ",bw)
print("B= ",B)

print(" ---------- BnB ------------")
s = time.time()
best_value, chosen_items = calcBnB(bc, bw, B)
e = time.time()

print("Najlepsza wartość:", best_value)
print("Wybrane przedmioty:", chosen_items)
print(f"Czas: {e-s}")

print(" ---------- SB-1 (0.6) ------------")
s = time.time()
best_value, chosen_items = calcBnB(bc, bw, B, 0.6)
e = time.time()
print("Najlepsza wartość:", best_value)
print("Wybrane przedmioty:", chosen_items)
print(f"Czas: {e-s}")

print(" ---------- SB-2 (k = 1) ------------")
s = time.time()
best_value, chosen_items = calcBnB(bc, bw, B, 1, True)
e = time.time()
print("Najlepsza wartość:", best_value)
print("Wybrane przedmioty:", chosen_items)
print(f"Czas: {e-s}")