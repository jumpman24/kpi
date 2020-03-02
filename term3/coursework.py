from collections import defaultdict
from pulp import *

print("===============================================================================================")
print("Вихідна задача з чіткими умовами")
print("===============================================================================================")
print("+-------------+------------------------------------+-------+\n"
      "|             | Завод 1  Завод 2  Завод 3  Завод 4 | Попит |\n"
      "+-------------+------------------------------------+-------+\n"
      "| Витрати     |    9        3        6       10    |       |\n"
      "+-------------+------------------------------------+-------+\n"
      "| Споживач 1  |    5        3        6        2    |  400  |\n"
      "| Споживач 2  |    3        4        5        6    |  800  |\n"
      "| Споживач 3  |    7        5        6        4    |  200  |\n"
      "| Споживач 4  |    4        8        5        3    |  800  |\n"
      "+-------------+------------------------------------+-------+\n"
      "| Потужність  |   500      700      600      ---   |       |\n"
      "| Дод.витрати |    3        2        5       ---   |       |\n"
      "+-------------+------------------------------------+-------+\n")


def solve_phase_one(consumers: int, producers: int,
                    transition_coeffs: list,
                    needs: list, powers: list):
    errors = []

    if len(transition_coeffs) != consumers * producers:
        errors.append("Транспортні витрати вказані невірно")

    if len(needs) != consumers:
        errors.append("Попит споживачів вказан невірно")

    if len(powers) != producers:
        errors.append("Потужність заводів вказана невірно")

    if sum(needs) > sum(powers):
        errors.append("Попиту споживачів перевищує потужність заводів")

    if errors:
        return errors

    X = []
    for i in range(consumers):
        for j in range(producers):
            X.append(pulp.LpVariable(f"X{i+1}{j+1}", lowBound=0, cat=pulp.LpInteger))

    transition_cost = sum([c_ij*x_ij for c_ij, x_ij in zip(transition_coeffs, X)])

    problem = pulp.LpProblem("0", LpMinimize)
    problem += transition_cost, "Цільова функція"

    print("Цільова функція:", transition_cost)

    print("Обмеження за попитом:")
    # Обмеження за попитом
    for idx, need in enumerate(needs):
        # print(sum(X[producers*idx:producers*(idx+1)]) == need)
        problem += sum(X[producers*idx:producers*(idx+1)]) == need, f"споживач {idx + 1}"

    print("Обмеження за потужністю:")
    for idx, power in enumerate(powers):
        print(sum(X[idx::consumers]) <= power)
        problem += sum(X[idx::consumers]) <= power, f"завод {idx + 1}"

    problem.solve()

    print("План поставки:")
    for variable in problem.variables():
        if variable.varValue > 0:
            var_name = variable.name
            print(f"Завод {var_name[2]} -> Споживач {var_name[1]}: {int(variable.varValue)}")

    print(f"Витрати на транспортування: {int(value(transition_cost))}")

    return problem


transition_coeffs = [5, 3, 6, 2, 3, 4, 5, 6, 7, 5, 6, 4, 4, 8, 5, 3]
needs = [400, 800, 200, 800]

print("===============================================================================================")
print("Варіант №1. Розширюємо потужність першого заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs1 = [12, 3, 6, 0]
powers1 = [900, 700, 600, 0]
production_cost1 = sum([c * n for c, n in zip(production_coeffs1, powers1)])
vars1 = solve_phase_one(4, 4, transition_coeffs, needs, powers1)
print(f"Витрати на виробництво:     {int(value(production_cost1))}")
print(f"Загальні витрати:           {int(value(vars1.objective) + int(value(production_cost1)))}")

print("===============================================================================================")
print("Варіант №2. Розширюємо потужність другого заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs2 = [9, 5, 6, 0]
powers2 = [500, 1100, 600, 0]
production_cost2 = sum([c * n for c, n in zip(production_coeffs2, powers2)])
vars2 = solve_phase_one(4, 4, transition_coeffs, needs, powers2)
print(f"Витрати на виробництво:     {int(value(production_cost2))}")
print(f"Загальні витрати:           {int(value(vars2.objective) + int(value(production_cost2)))}")

print("===============================================================================================")
print("Варіант №3. Розширюємо потужність третього заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs3 = [9, 3, 11, 0]
powers3 = [500, 700, 1000, 0]
production_cost3 = sum([c * n for c, n in zip(production_coeffs3, powers3)])
vars3 = solve_phase_one(4, 4, transition_coeffs, needs, powers3)
print(f"Витрати на виробництво:     {int(value(production_cost3))}")
print(f"Загальні витрати:           {int(value(vars3.objective) + int(value(production_cost3)))}")

print("===============================================================================================")
print("Варіант №4. Будуємо четвертий завод без додаткових витрат на одиницю продукції")
print("===============================================================================================")

production_coeffs4 = [9, 3, 6, 10]
powers4 = [500, 700, 600, 400]
production_cost4 = sum([c * n for c, n in zip(production_coeffs4, powers4)])
vars4 = solve_phase_one(4, 4, transition_coeffs, needs, powers4)
print(f"Витрати на виробництво:     {int(value(production_cost4))}")
print(f"Загальні витрати:           {int(value(vars4.objective) + int(value(production_cost4)))}")

print()
print("==================================================================================================")
print("Вихідна задача з нечіткими обмеженнями")
print("==================================================================================================")
print("+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "|             | Завод 1  Завод 2  Завод 3  Завод 4 |  Попит,min | Попит,max | Дефіцит | Надлишок |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "| Витрати     |    9        3        6       10    |                                             |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "| Споживач 1  |    5        3        6        2    |     300    |    500    |    5    |     8    |\n"
      "| Споживач 2  |    3        4        5        6    |     700    |   1100    |    6    |    10    |\n"
      "| Споживач 3  |    7        5        6        4    |     200    |    400    |    6    |    19    |\n"
      "| Споживач 4  |    4        8        5        3    |     600    |   1000    |    3    |     6    |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "| Потужність  |   500      700      600      ---   |                                             |\n"
      "| Дод.витрати |    3        2        5       ---   |                                             |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+")


def calc_cost(X, C, W, B_min, B_max, S, R):
    res = 0

    for c, x in zip(C, X):
        res += value(c * x)
    print(res)
    for j in range(4):
        res += R[j] * ((B_max[j] + B_min[j]) / 2 - W[j])
        res += ((S[j] + R[j]) / (2 * (B_max[j] - B_min[j]))) * ((W[j] - B_min[j]) ** 2)

    return res


def gradients(m, n, C, W, A, B_min, B_max, S, R):
    grads = []

    for i in range(m):
        for j in range(n):
            grad = C[i*n+j] - R[j] + (S[j] + R[j]) / (B_max[j] - B_min[j]) * (W[j] - B_min[j])
            grads.append(grad)

    return grads


C = [5, 3, 6, 2, 3, 4, 5, 6, 7, 5, 6, 4, 4, 8, 5, 3]
X = vars2.variables()
A = [500, 1100, 600, 0]
W = [400, 800, 200, 800]
B_min = [300, 700, 200, 600]
B_max = [500, 1100, 400, 1000]
B = [(b_max+b_min)/2 for b_max, b_min in zip(B_max, B_min)]
R = [5, 6, 6, 3]
S = [8, 10, 19, 6]

X_grads = gradients(4, 4, C, W, A, B_min, B_max, S, R)
Y = []
for i in range(4):
    for j in range(4):
        Y.append(pulp.LpVariable(f"Y{i + 1}{j + 1}", lowBound=0, cat=pulp.LpInteger))
print(X_grads)
cost = sum([x0*y for x0, y in zip(X_grads, Y)])
print(cost)
prob_y = LpProblem('grad1', LpMinimize)
prob_y += cost, 'grad_cost'

print("Обмеження за попитом:")
# Обмеження за попитом
for idx, need in enumerate(B):
    print(sum(Y[4*idx:4*(idx+1)]) == need)
    prob_y += sum(Y[4 * idx:4 * (idx + 1)]) == need, f"споживач {idx + 1}"

print("Обмеження за потужністю:")
for idx, power in enumerate(A):
    print(sum(Y[idx::4]) <= power)
    prob_y += sum(Y[idx::4]) <= power, f"завод {idx + 1}"

prob_y.solve()

print("План поставки:")
for variable in prob_y.variables():
    if variable.varValue > 0:
        var_name = variable.name
        print(f"Завод {var_name[2]} -> Споживач {var_name[1]}: {int(variable.varValue)}")

print(f"Витрати на транспортування: {int(value(cost))}")
