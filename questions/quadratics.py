from math import *
from random import *
def gettext(inseed):
    a,b,c = gendata(inseed)
    return "Given the quadratic \("+str(a)+"x^2+"+str(b)+"x+"+str(c)+"=0\), what is the value of \(x\)?"
'''
def getanswer(inseed):
    a,b,c = gendata(inseed)
    return [(-b+sqrt(b**2-4*a*c))/(2*a),(-b-sqrt(b**2-4*a*c))/(2*a)]
'''
def gendata(inseed):
    seed(inseed)
    a = int(10*random()+1)
    b = int(10*random()+1)
    c = -int(10*random()+1)
    return (a,b,c)
def checkanswer(inseed,useranswer):
    a,b,c = gendata(inseed)
    floatanswer = float(useranswer)
    correctanswers =  [(-b+sqrt(b**2-4*a*c))/(2*a),(-b-sqrt(b**2-4*a*c))/(2*a)]
    for ans in correctanswers:
        if(abs(ans-floatanswer)<.1):
            return 1
    return 0
