import sympy as sp
from sympy.geometry import *

sp.init_printing(use_unicode=True)
a,b,c = sp.symbols('a,b,c', positive=True)
p1,p2 = sp.symbols('p1,p2', positive=True)
p3 = 2- p1 - p2

def compute_area(l1,l2,l3):
    s = (l1+l2+l3)/2
    return sp.sqrt(s*(s-l1)*(s-l2)*(s-l3))

A1 = compute_area((p2+p3-1)*a, (p2+p3-1)*b, (p2+p3-1)*c)
A2 = compute_area((p1+p3-1)*a, (p1+p3-1)*b, (p1+p3-1)*c)
A3 = compute_area((p2+p1-1)*a, (p2+p1-1)*b, (p2+p1-1)*c)
print(sp.latex((A1+A2+A3)/3))