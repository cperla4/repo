a = int(input())
b = int(input())

def x(begin, end):
    for i in range(end):
        if begin > end:
            break
        else:
            begin = begin ++1
            print(begin)
a = a - 1
b = b - 1
x(a,b)
