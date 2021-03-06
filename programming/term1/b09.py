"""
Дано натуральне (ціле невід’ємне) число a та ціле додатне число d.
Обчислити частку від ділення q та залишок r при діленні a на d,
не використовуючи операцій цілочислового ділення та операцій
обчислення залишку від цілочисленого ділення.
"""


def div_mod(a, d):
    r = a
    q = 0

    while r >= d:
        q += 1
        r -= d

    return r, q


if __name__ == '__main__':
    while True:
        try:
            a = int(input("Введіть натуральне число a: "))
            d = int(input("Введіть ціле додатне число d: "))

            r, q = div_mod(a, d)
            print("q=%d r=%d" % (q, r))

        except ValueError:
            pass
