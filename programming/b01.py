"""
Завдання №1.
Дано натуральне n.
Підрахувати кількість розв’язки нерівності x^2 + y^2 < n в натуральних (невід’ємних числах)
не використовуючи дій з дійсними числами.
"""

while True:
    try:
        n = int(input("Введіть число: "))

        if n > 0:
            break
        print("Будь ласка, введіть число більше 0.")

    except ValueError:
        print("Будь ласка, введіть число більше 0.")

count = 0
for x in range(n):

    for y in range(n):

        if not (x * x + y * y) < n:
            break
        print("x=%d, y=%d" % (x, y))
        count += 1

print("Кількість розв’язки нерівності x^2+y^2<%d: %d" % (n, count))
