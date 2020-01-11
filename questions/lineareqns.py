from sympy import *
from random import *

def gettext(inseed):
    a,b = gendata(inseed)
    x = Symbol('x')
    return "Given the linear equation \(" + latex(a*x+b) + "=0\), what is the value of \(x\)?"
'''
def getanswer(inseed):
    a,b = gendata(inseed)
    return [-b/a]
'''
def gendata(inseed):
    seed(inseed)
    a = int(10*random()+1)
    b = -int(10*random()+1)
    return (a,b)

def checkanswer(inseed,useranswer):
    a,b = gendata(inseed)
    floatanswer = float(sympify(useranswer))
    return (abs(floatanswer - (-b/a)) < .1)
