import math
from RandomNumberGenerator import RandomNumberGenerator
import time
from collections import deque

rng = RandomNumberGenerator(12435535)
#MAX_TABU = 20

def stats(arr):
    #print(arr)
    return {
        "MIN": min(arr),
        "MAX": max(arr),
        "AVG": round(sum(arr) / len(arr), 2)
    }

def print_table(title, rs_results, vd_results, ts_results):

    rs = stats(rs_results)
    vd = stats(vd_results)
    ts = stats(ts_results)

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"{'Algorithm':<20} {'MIN':>10} {'MAX':>10} {'AVG':>10}")
    print("-" * 60)

    print(f"{'Random Solution':<20} {rs['MIN']:>10} {rs['MAX']:>10} {rs['AVG']:>10}")
    print(f"{'DS':<20} {vd['MIN']:>10} {vd['MAX']:>10} {vd['AVG']:>10}")
    print(f"{'Tabu Search':<20} {ts['MIN']:>10} {ts['MAX']:>10} {ts['AVG']:>10}")

    print("=" * 60)

def generate_data_2_7(n):

    p = []  # processing times
    d = []  # due dates
    w = []  # weights

    S = 0

    for _ in range(n):
        w.append(rng.nextInt(1, 10))
        proc = rng.nextInt(1,100)

        p.append(proc)

        S += proc

    for _ in range(n):
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

def find_neighbours(v, nb_type: str = "n2"):
    neigh = []
    ii = []
    jj = []
    n = len(v)
    if nb_type == "n2":
        for i in range(n):
            for j in range(i+1, n):
                lv = v.copy()
                lv[i], lv[j] = lv[j], lv[i]
                neigh.append(lv)
                ii.append(i)
                jj.append(j)
    elif nb_type == "n":
        for i in range(n):
            j = (i+1)%n
            lv = v.copy()
            lv[i], lv[j] = lv[j], lv[i]
            neigh.append(lv)
            ii.append(i)
            jj.append(j)
    return neigh, ii, jj

def DS(p, d, w, itr = 1000, v = None, ev = 0, nb_type: str = "n2"):
    if v == None:
        v = random_solution(len(p))
        ev, _, _ = evaluate_partial(v, p, d, w)

    best_v = v
    best_ev = ev

    for _ in range(itr):
        nvs, _, _ = find_neighbours(v, nb_type)
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

def inlineTS(p, d, w, itr = 1000, v = None, ev = 0, nb_type: str = "n2", tabu_type: str = None, max_tabu = 20):
    return TS(p, d, w, itr, v, ev, nb_type, tabu_type, max_tabu)
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

def TS(p, d, w, itr = 1000, v = None, ev = 0,  nb_type: str = "n2", tabu_type = None, max_tabu = 20):
    if v == None:
        v = random_solution(len(p))
        ev, _, _ = evaluate_partial(v, p, d, w)

    if tabu_type == None:
        tabu_type = "numbers" if nb_type == "n" else "indexes"

    best_v = v
    best_ev = ev
    tabu_dq = deque()
    tabu_set = set()
    pct = None
    T = None

    for _ in range(itr):
        local_v = None
        local_ev = math.inf
        best_move = None
        nbs, ii, jj = find_neighbours(v, nb_type)
        for nb, i, j in zip(nbs, ii, jj):
            ev, _, _ = evaluate_partial(nb, p, d, w)
            if tabu_type == "indexes":
                move = (i, j)
            else:
                move = (nb[i], nb[j])
            if ev < local_ev and move not in tabu_set:
                local_v = nb
                local_ev = ev
                best_move = move

        tabu_set.add(best_move)
        tabu_dq.append(best_move)
        if len(tabu_dq) > max_tabu:
            old = tabu_dq.popleft()
            tabu_set.remove(old)

        if local_v is None:
            print("BREAK")
            break
        
        v = local_v
        _, pct, T = evaluate_partial(v, p, d, w, best_move[0], pct, T)

        if local_ev < best_ev:
            best_v = local_v
            best_ev = local_ev


    return best_v, best_ev, len(tabu_set)

# Main
def single_exp():
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

    print("-- DS --")
    start = time.time()
    vdv, evdv = DS(p, d, w, 1000, rv, erv)
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

###########################
def avg_exp():
    n = 25
    p, d, w = generate_data_2_7(n)
    max_tabu = 20

    print_list = []
    repeats = 10
    rs_results = []
    ers_results = []

    for _ in range(repeats):
        rv = random_solution(n)
        erv, _, _ = evaluate_partial(rv, p, d, w)
        rs_results.append(rv)
        ers_results.append(erv)

    #for nb_type, tabu_type in zip(["n2", "n2", "n"], ["indexes", "numbers", "numbers"]):
    for nb_type in ["n2", "n"]:
        for tabu_type in ["indexes", "numbers"]:
            if n < max_tabu + 5 and nb_type == "n" and tabu_type == "indexes":
                continue
            vd_results = []
            its_results = []

            print(p)
            print(d)
            print(w)

            for i in range(repeats):

                print(f" --- loop {i+1}/{repeats} --- ")
                print(f"Nbs type: {nb_type} | Tabu type: {tabu_type}")

                rv = rs_results[i]
                erv = ers_results[i]

                _, ev1 = DS(p, d, w, 1000, rv, erv, nb_type = nb_type)
                _, ev3, _ = inlineTS(p, d, w, 1000, rv, erv, nb_type = nb_type, tabu_type = tabu_type)

                print(erv, ev1, ev3)

                rs_results.append(erv)
                vd_results.append(ev1)
                its_results.append(ev3)

            print_list.append([
                f"Nbs type: {nb_type} | Tabu type: {tabu_type}",
                ers_results,
                vd_results,
                its_results
            ])

    for pl in print_list:
        print_table(pl[0], pl[1], pl[2], pl[3])

def iter_exp():
    n = 25
    p, d, w = generate_data_2_7(n)
    print_list = []

    repeats = 10
    rs_results = []
    ers_results = []

    for _ in range(repeats):
        rv = random_solution(n)
        erv, _, _ = evaluate_partial(rv, p, d, w)
        rs_results.append(rv)
        ers_results.append(erv)

    # for nb_type, tabu_type in zip(["n2", "n2", "n"], ["indexes", "numbers", "numbers"]):
    for iter in [5, 20, 100, 300, 1000]:
        vd_results = []
        its_results = []


        print(p)
        print(d)
        print(w)

        for i in range(repeats):
            print(f" --- loop {i + 1}/{repeats} --- ")
            print(f"Iter: {iter}")

            rv = rs_results[i]
            erv = ers_results[i]

            _, ev1 = DS(p, d, w, iter, rv, erv)
            _, ev3, _ = inlineTS(p, d, w, iter, rv, erv)

            print(erv, ev1, ev3)

            vd_results.append(ev1)
            its_results.append(ev3)

        print_list.append([
            f"Iter {iter}",
            ers_results,
            vd_results,
            its_results
        ])

    for pl in print_list:
        print_table(pl[0], pl[1], pl[2], pl[3])

def tabu_exp():
    n = 25
    p, d, w = generate_data_2_7(n)
    print_list = []

    repeats = 10
    rs_results = []
    ers_results = []

    for _ in range(repeats):
        rv = random_solution(n)
        erv, _, _ = evaluate_partial(rv, p, d, w)
        rs_results.append(rv)
        ers_results.append(erv)

    # for nb_type, tabu_type in zip(["n2", "n2", "n"], ["indexes", "numbers", "numbers"]):
    for max_tabu in [5, 10, 20, 30]:
        vd_results = []
        its_results = []


        print(p)
        print(d)
        print(w)

        for i in range(repeats):
            print(f" --- loop {i + 1}/{repeats} --- ")
            print(f"Max Tabu: {max_tabu}")

            rv = rs_results[i]
            erv = ers_results[i]

            _, ev1 = DS(p, d, w, 1000, rv, erv)
            _, ev3, _ = inlineTS(p, d, w, 1000, rv, erv, "n2", "indexes", max_tabu)

            print(erv, ev1, ev3)

            vd_results.append(ev1)
            its_results.append(ev3)

        print_list.append([
            f"Max tabu: {max_tabu}",
            ers_results,
            vd_results,
            its_results
        ])

    for pl in print_list:
        print_table(pl[0], pl[1], pl[2], pl[3])


if __name__ == "__main__":
    #single_exp()
    avg_exp()
    #iter_exp()
    #tabu_exp()