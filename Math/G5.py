import math

I_win = [False, False] 
# if you were to have i stones left,
# the statement "I will win" is I_win[i-1]

def divisors(n) : 
    l1 = []
    l2 = []  
    for i in range(1, int(math.sqrt(n) + 1)) : 
          
        if (n % i == 0) : 
            if (n / i == i) : 
                l1.append(i)
            else : 
                l1.append(i)
                l2.append(int(n / i)) 
    return l1 + l2[::-1][:-1]

n = 100000
for i in range(3,n):
    print("{}: {}".format(i-1, "Alice" if I_win[i-2] else "Bob"))
    ds = divisors(i)
    if len(ds) == 1: # if it's a prime:
        I_win.append(False)
        continue
    for d in ds:
        if not I_win[i-d-1]:
            I_win.append(True)
            break
    if len(I_win) < i:
        I_win.append(False)