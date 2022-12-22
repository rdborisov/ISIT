import numpy as np
from numpy import genfromtxt

dataset = genfromtxt('data.csv', delimiter=',', dtype=None)


def __normalize__(dataset, n_dataset, n, m):
    for j in range(m):
        sq = np.sqrt(sum(dataset[:, j] ** 2))
        n_dataset[:, j] = [dataset[i, j] / sq for i in range(n)]
    return n_dataset


def __get_worst_best__(signs, dataset, m):
    worst = []
    best = []
    for i in range(m):
        fir, sec = (max(dataset[:, i]), min(dataset[:, i])) if signs[i] == 1 else (
            min(dataset[:, i]), max(dataset[:, i]))
        worst.append(sec)
        best.append(fir)
    return worst, best


def __get_worst_best_distanse__(dataset, worst, best, n):
    worst_dist = (dataset - worst) ** 2
    best_dist = (dataset - best) ** 2
    worst_dist = np.array([sum(worst_dist[i, :]) ** 0.5 for i in range(n)])
    best_dist = np.array([sum(best_dist[i, :]) ** 0.5 for i in range(n)])
    return worst_dist, best_dist


def __topsis__(dataset, weights, signs):
    dataset = np.array(dataset, dtype=float)
    n, m = len(dataset), len(dataset[0])
    n_dataset = np.empty((n, m), np.float64)
    n_dataset = __normalize__(dataset, n_dataset, n, m) * weights
    (worst, best) = __get_worst_best__(signs, n_dataset, m)
    (worst_dist, best_dist) = __get_worst_best_distanse__(n_dataset, worst, best, n)
    return worst_dist / (best_dist + worst_dist)


def prepare_info(res_dataset):
    max_ind = np.argmax(res_dataset)
    min_ind = np.argmin(res_dataset)
    max_info = f'{max_ind + 1} is the best. It has score = {res_dataset[max_ind]:.4f}'
    min_info = f'{min_ind + 1} is the worst. It has score = {res_dataset[min_ind]:.4f}'
    res = [f'№{i + 1} = {x:.4f}' for i, x in enumerate(res_dataset)]
    res.append(max_info)
    res.append(min_info)
    res = '\n'.join(res)
    print(max_info)
    print(min_info)


def topsis(dataset, weights, signs):
    res_dataset = __topsis__(dataset, weights, signs)
    prepare_info(res_dataset)
    return res_dataset


def dominate(dataset):
    def weigh(a, b):
        if (a[0] >= b[0]) and (a[1] >= b[1]) and (a[2] >= b[2]) and (a[3] >= b[3]) and (a[4] >= b[4]):
            if (a[0] > b[0]) or (a[1] > b[1]) or (a[2] > b[2]) or (a[3] > b[3]) or (a[4] > b[4]):
                return 1
            else:
                return 0
        elif (a[0] <= b[0]) and (a[1] <= b[1]) and (a[2] <= b[2]) and (a[3] <= b[3]) and (a[4] <= b[4]):
            if (a[0] < b[0]) or (a[1] < b[1]) or (a[2] < b[2]) or (a[3] < b[3]) or (a[4] < b[4]):
                return 2
            else:
                return 0
        else:
            return 0

    pareto = []
    for i in range(len(dataset)):
        pareto.append(-1)
    for i in range(len(dataset)):
        for j in range(i + 1, len(dataset)):
            comp = weigh(dataset[i], dataset[j])
            if comp == 0:
                if pareto[i] == -1:
                    pareto[i] = 1
                if pareto[j] == -1:
                    pareto[j] = 1
            if comp == 1:
                if pareto[i] == -1:
                    pareto[i] = 1
                pareto[j] = 0
            if comp == 2:
                pareto[i] = 0
                if pareto[j] == -1:
                    pareto[j] = 1
    count_dom = 0
    wai = [1, 1, 1, 1, 1] #веса критериев
    signs = [1, 1, 1, 1, 1] #знаки критериев
    rating = topsis(dataset, wai, signs)
    for i in range(len(dataset)):
        count_dom += pareto[i]
        print(str(i + 1), dataset[i], pareto[i], "score:", round(rating[i], 3))
    print("count_dom:", count_dom)


dominate(dataset)
