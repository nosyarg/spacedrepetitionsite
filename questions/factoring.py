from math import *
def gettext(a,b,c):
    return "Given the quadratic \("+str(a)+"x^2+"+str(b)+"x+"+str(c)+"=0\), what is the value of \(x\)?"
def getanswer(a,b,c):
    return {(-b+sqrt(b**2-4*a*c))/(2*a),(-b-sqrt(b**2-4*a*c))/(2*a)}
