import sys
import random
import matplotlib.pyplot as plt
import csv
import os
import math
import numpy as np
import json
import time

# kullanıcıdan parametre alma
funcName = sys.argv[1]
dim = int(sys.argv[2])
maxIter = int(sys.argv[3])
foodNumber = int(sys.argv[4])
limit = int(sys.argv[5])
customExpr = sys.argv[6] if funcName == 'custom' else None

# file isimleri
output_dir = os.path.join(os.path.dirname(__file__), "files")
os.makedirs(output_dir, exist_ok=True)
timestamp = int(time.time())
graph_file = f"abc_graph_{timestamp}.png"
csv_file = f"abc_results_{timestamp}.csv"
graph_path = os.path.join(output_dir, graph_file)
csv_path = os.path.join(output_dir, csv_file)

# functions
def sphere(x):
    return sum(i**2 for i in x)

def rosenbrock(x):
    return sum(100*(x[i+1]-x[i]**2)**2 + (x[i]-1)**2 for i in range(len(x)-1))

def rastrigin(x):
    n = len(x)
    return 10*n + sum([xi**2 - 10*math.cos(2*math.pi*xi) for xi in x])

def ackley(x):
    n = len(x)
    a = 20
    b = 0.2
    c = 2*math.pi
    sum_sq = sum([xi**2 for xi in x])
    sum_cos = sum([math.cos(c*xi) for xi in x])
    return -a*math.exp(-b*math.sqrt(sum_sq/n)) - math.exp(sum_cos/n) + a + math.e

def griewank(x):
    sum_sq = sum([xi**2 for xi in x])/4000
    prod_cos = np.prod([math.cos(xi/math.sqrt(i+1)) for i, xi in enumerate(x)])
    return sum_sq - prod_cos + 1

def beale(x):
    if len(x) != 2:
        raise ValueError("Beale fonksiyonu sadece 2 boyutlu çalışır")
    x1, x2 = x
    return (1.5 - x1 + x1*x2)**2 + (2.25 - x1 + x1*x2**2)**2 + (2.625 - x1 + x1*x2**3)**2

def booth(x):
    if len(x) != 2:
        raise ValueError("Booth fonksiyonu sadece 2 boyutlu çalışır")
    x1, x2 = x
    return (x1 + 2*x2 - 7)**2 + (2*x1 + x2 - 5)**2

def custom(x):
    return eval(customExpr, {"x":x, "math":math})

func_dict = {
    "sphere": sphere,
    "rosenbrock": rosenbrock,
    "custom": custom,
    "rastrigin": rastrigin,
    "ackley": ackley,
    "griewank": griewank,
    "beale": beale,
    "booth": booth
}

obj_func = func_dict[funcName]

# abc algoritması
lb, ub = -10, 10
foods = [[random.uniform(lb, ub) for _ in range(dim)] for _ in range(foodNumber)]
fitness = [obj_func(sol) for sol in foods]
trial = [0]*foodNumber
best_idx = min(range(foodNumber), key=lambda i: fitness[i])
best_sol = foods[best_idx][:]
best_fit = fitness[best_idx]
fitness_list = []

for it in range(maxIter):
    # employed bees
    for i in range(foodNumber):
        k = random.choice([j for j in range(foodNumber) if j != i])
        phi = random.uniform(-1,1)
        param = random.randint(0, dim-1)
        new_sol = foods[i][:]
        new_sol[param] = foods[i][param] + phi*(foods[i][param]-foods[k][param])
        # sınır kontrolü
        new_sol[param] = max(lb, min(ub, new_sol[param]))

        new_fit = obj_func(new_sol)
        if new_fit < fitness[i]:
            foods[i] = new_sol
            fitness[i] = new_fit
            trial[i] = 0
        else:
            trial[i] += 1

    # onlooker bees
    inv_fits = [1/(f+1e-9) for f in fitness]
    total = sum(inv_fits)
    probs = [f/total for f in inv_fits]

    for _ in range(foodNumber):
        i = random.choices(range(foodNumber), weights=probs, k=1)[0]
        k = random.choice([j for j in range(foodNumber) if j != i])
        phi = random.uniform(-1,1)
        param = random.randint(0, dim-1)
        new_sol = foods[i][:]
        new_sol[param] = foods[i][param] + phi*(foods[i][param]-foods[k][param])
        # sınır kontrolü
        new_sol[param] = max(lb, min(ub, new_sol[param]))

        new_fit = obj_func(new_sol)
        if new_fit < fitness[i]:
            foods[i] = new_sol
            fitness[i] = new_fit
            trial[i] = 0
        else:
            trial[i] += 1

    # scout bees
    for i in range(foodNumber):
        if trial[i] > limit:
            foods[i] = [random.uniform(lb, ub) for _ in range(dim)]
            fitness[i] = obj_func(foods[i])
            trial[i] = 0

    # en iyi çözüm
    min_idx = min(range(foodNumber), key=lambda i: fitness[i])
    if fitness[min_idx] < best_fit:
        best_fit = fitness[min_idx]
        best_sol = foods[min_idx][:]
    fitness_list.append(best_fit)


# fitness iteration grafik
plt.plot(fitness_list)
plt.xlabel("Iteration")
plt.ylabel("Fitness")
plt.title("ABC Algoritması Sonuçları")
plt.savefig(graph_path, format='png', bbox_inches='tight')
plt.close()

# csv kaydet
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Iteration","Fitness"])
    for i, val in enumerate(fitness_list):
        writer.writerow([i+1,val])

# 2d grafik
if dim == 2:
    x_min, x_max = -10, 10
    y_min, y_max = -10, 10
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    zz = np.zeros_like(xx)
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            zz[i,j] = obj_func([xx[i,j], yy[i,j]])
    
    plt.figure(figsize=(6,5))
    plt.contourf(xx, yy, zz, levels=50, cmap='viridis')
    plt.colorbar(label='Fitness')
    sol_x = [sol[0] for sol in foods]
    sol_y = [sol[1] for sol in foods]
    plt.scatter(sol_x, sol_y, color='red', label='ABC Çözümleri')
    plt.xlabel('x[0]')
    plt.ylabel('x[1]')
    plt.title(f"{funcName} Fonksiyonu")
    plt.legend()
    func_graph_file = f"abc_func_{funcName}.png"
    plt.savefig(os.path.join(output_dir, func_graph_file), bbox_inches='tight')
    plt.close()
else:
    func_graph_file = None

# json çıktı
result = {
    "best_sol": best_sol,
    "best_fit": best_fit,
    "graph_file": graph_file,
    "func_graph_file": func_graph_file,
    "csv_file": csv_file
}

print(json.dumps(result))
