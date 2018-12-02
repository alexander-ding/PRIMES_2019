import math

def test(n):
    return math.sqrt(abs(2019-n**2))

for i in range(1000):
    n = test(i)
    if n-int(n) < 0.001:
        print(i, n)

def more(x,y):
    return 3*x+4*y, 2*x+3*y

x=3
y=2
for i in range(100):
    print(x,y)
    x,y=more(x,y)