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

def evaluate_partial(v, p, d, w, start=0, completion_time=None, T = None):

    n = len(v)

    if completion_time is None or T is None:
        completion_time = [0] * n
        T = [0] * n
        start = 0


    if start == 0:
        completion_time[0] = p[v[0]]
        delta = completion_time[0] - d[v[0]]

        if delta > 0:
            T[0] += delta * w[v[0]]

        start = 1

    for i in range(start, n):

        completion_time[i] = completion_time[i-1] + p[v[i]]

        delta = completion_time[i] - d[v[i]]

        if delta > 0:
            T[i] = T[i-1] + delta * w[v[i]]

    return T[-1], completion_time, T

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

def VD(p, d, w, itr = 1000, v = None, ev = 0):
    if v == None:
        v = random_solution(len(p))
        ev, _, _ = evaluate_partial(v, p, d, w)

    best_v = v
    best_ev = ev

    for _ in range(itr):
        nvs, _, _ = find_neighbours(v)
        local_v = []
        local_ev = math.inf
        for nv in nvs:
            ev, _, _ = evaluate_partial(nv, p, d, w)
            if ev < local_ev:
                local_v = nv
                local_ev = ev

        if local_ev < best_ev:
            best_v = local_v
            best_ev = local_ev
            v = local_v.copy()
        else:
            break

    return best_v, best_ev

def inlineTS(p, d, w, itr = 1000, v = None, ev = 0):
    if v == None:
        v = random_solution(len(p))
        ev, _, _ = evaluate_partial(v, p, d, w)

    best_v = v
    best_ev = ev
    tabu_dq = deque()
    tabu_set = set()
    pct = None
    T = None

    for _ in range(itr):
        n = len(v)
        local_v = None
        local_ev = math.inf
        best_move = None
        for i in range(n):
            for j in range(i+1, n):
                lv = v.copy()
                lv[i], lv[j] = lv[j], lv[i]

                ev, _, _ = evaluate_partial(lv, p, d, w)
                move = (i, j)
                if ev < local_ev and move not in tabu_set:
                    local_v = lv
                    local_ev = ev
                    best_move = move

        tabu_set.add(best_move)
        tabu_dq.append(best_move)
        if len(tabu_dq) > MAX_TABU:
            old = tabu_dq.popleft()
            tabu_set.remove(old)

        if local_v is None:
            print("BREAK!!!!")
            break
        
        v = local_v
        _, pct, T = evaluate_partial(v, p, d, w, best_move[0], pct, T)

        if local_ev < best_ev:
            best_v = local_v
            best_ev = local_ev


    return best_v, best_ev, len(tabu_set)

# Main
n = 20
p, d, w = generate_data_2_7(n)

print("p=",p)
print("d=",d)
print("w=",w)

print("losowe rozwiązanie")
rv = random_solution(n)
erv, _, _ = evaluate_partial(rv, p, d, w)
print("rv=",rv)
print("erv=",erv)

print("-- VD --")
start = time.time()
vdv, evdv = VD(p, d, w, 1000, rv, erv)
end = time.time()
print("vdv=",vdv)
print("evdv=",evdv)
print("time= ",round(end-start,3))



print("-- inline TS --")
start = time.time()
tsv, etsv, le = inlineTS(p, d, w, 1000, rv, erv)
end = time.time()
print("tsv=",tsv)
print("etsv=",etsv)
print("tabu len=",le)
print("time= ",round(end-start,3))

###########################3

vd_results = []
ts_results = []
its_results = []

for i in range(30):

    print(f" --- loop {i+1}/30 --- ")

    rv = random_solution(n)
    erv, _, _ = evaluate_partial(rv, p, d, w)

    _, ev1 = VD(p, d, w, 1000, rv, erv)
    _, ev3, _ = inlineTS(p, d, w, 1000, rv, erv)

    vd_results.append(ev1)
    its_results.append(ev3)

print(sum(vd_results)/30)
print(sum(its_results)/30)