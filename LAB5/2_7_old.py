import math
from RandomNumberGenerator import RandomNumberGenerator
import time
from collections import deque

rng = RandomNumberGenerator(12435535)
MAX_TABU = 20

def generate_data_2_7(n):

    p = []  # processing times
    d = []  # due dates
    w = []  # weights

    S = 0

    for i in range(n):
        w.append(rng.nextInt(1, 10))
        proc = rng.nextInt(1,100)

        p.append(proc)

        S += proc

    for i in range(n):

        d.append(rng.nextInt(math.floor(S/4), math.floor(S/2)))
    return p, d, w

def randomChoice(arr):
    return arr[rng.nextInt(0, len(arr)-1)]

def randomShuffle(s):
    v = []
    while len(s) > 0:
        c = randomChoice(s)
        s.remove(c)
        v.append(c)
    return v

def random_solution(n):
    return randomShuffle([i for i in range(n)])

def evaluate_solution(v, p, d, w):
    completion_time = 0
    T = 0
    for i in range(len(v)):
        completion_time += p[v[i]]
        delta = completion_time - d[v[i]]
        if delta > 0:
            T += delta * w[v[i]]

    return T

def find_neighbours(v):
    neigh = []
    ii = []
    jj = []
    n = len(v)
    for i in range(n):
        for j in range(i+1, n):
            lv = v.copy()
            lv[i], lv[j] = lv[j], lv[i]
            neigh.append(lv)
            ii.append(i)
            jj.append(j)
    return neigh, ii, jj

def TS(p, d, w, itr = 1000, v = None, ev = 0):
    if v == None:
        v = random_solution(len(p))
        ev = evaluate_solution(v, p, d, w)

    best_v = v
    best_ev = ev
    tabu = []
    memo = []

    for _ in range(itr):
        nvs, k, l = find_neighbours(v)
        best_move = None
        local_v = None
        local_ev = math.inf
        for nv, i, j in zip(nvs, k, l):
            ev = evaluate_solution(nv, p, d, w)
            if ev < local_ev and (i, j) not in tabu:
                local_v = nv
                local_ev = ev
                best_move = (i, j)

        tabu.append(best_move)
        if len(tabu) > MAX_TABU:
            tabu.pop(0)

        if local_v is not None:
            v = local_v
            memo.append(local_v)
        else:
            if len(memo) > 0:
                v = memo[-1]
                memo.pop()
            else:
                print("Error")

        if local_ev < best_ev:
            best_v = local_v
            best_ev = local_ev

    return best_v, best_ev, len(tabu)

# print("-- TS --")
# start = time.time()
# tsv, etsv, le = TS(p, d, w, 1000, rv, erv)
# end = time.time()
# print("tsv=",tsv)
# print("etsv=",etsv)
# print("tabu len=",le)
# print("time= ",round(end-start,3))