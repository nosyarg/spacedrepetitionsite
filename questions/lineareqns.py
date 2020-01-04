from math import *
from random import *

def gettext(inseed):
    a,b = gendata(inseed)
    return "Given the linear equation \("+str(a)+'x' + str(b) + "=0\), what is the value of \(x\)?"

def getanswer(inseed):
    a,b = gendata(inseed)
    return [-b/a]

def gendata(inseed):
    seed(inseed)
    a = int(10*random()+1)
    b = -int(10*random()+1)
    return (a,b)

def checkanswer(useranswer,inseed):
    a,b = gendata(inseed)
    floatanswer = float(useranswer)
    return (abs(floatanswer - (-b/a)) < .1)
