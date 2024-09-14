import os, sys


def f(a, b):
    c = a + b
    d = c * 2
    e = d / 3
    f = e - 1
    return f


class x:
    def __init__(self):
        self.v = 42

    def m(self, a):
        if a == self.v:
            print("Match!")
        else:
            print("No match!")


def main():
    x.m(42)
    y = [1, 2, 3, 4, 5]
    for i in range(len(y)):
        print(y[i])
    f = lambda x: x * 2
    print(f(3))


main()
