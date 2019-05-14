"""
Завдання №19
Числа Армстронга.
Написати програму, яка виводить всі трьохзначні числа, рівні сумі кубів своїх цифр.
"""

for n in range(100, 1000):
    x = n // 100
    y = n // 10 % 10
    z = n % 10

    sum_cubes = x*x*x + y*y*y + z*z*z

    if sum_cubes == n:
        print(n)