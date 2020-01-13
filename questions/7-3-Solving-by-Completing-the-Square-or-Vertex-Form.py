"""
Solving a quadratic: only one x

a(x-h)^2 + b= c ... can result in no real solution.
"""

from sympy import*
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from numpy import random
def gettext(inseed):
    data = gendata(inseed)
    sqr = data['sqr']
    parity = data['parity']
    a = data['a']
    b = data['b']
    h = data['h']
    c = a*parity*sqr + b
    x = Symbol('x')
    return "Solve by any method.  Recommended: completing the square or vertex form: \\(" + latex(expand(a*(x-h)**2+b)) \
            +" =" + latex(c) + "\\)" +"\n" \
            + "(If you have multiple answers, enter them separated by a comma. \n"\
            + "Enter square roots using 'sqrt', as in 'sqrt(2)' for \\(" \
            + latex(sqrt(2)) + "\\).)"
def checkanswer(inseed, user_answer):
    data = gendata(inseed)
    h = data['h']
    sqr = data['sqr']
    parity = data['parity']
    if parity == 1:
        answer = set([h-sqrt(sqr), h+sqrt(sqr)])
        user_answer = user_answer.split(",")
        user_answer = [parse_expr(a, transformations=transformations) for a in user_answer]
        #print(user_answer)
        user_answer = set(user_answer)
        return answer == user_answer
    else:
        return 'no' in user_answer or 'No' in user_answer or 'NO' in user_answer
        
def getanswer(inseed):
    data = gendata(inseed)
    h = data['h']
    sqr = data['sqr']
    parity = data['parity']
    if parity == 1:
        solution_set = [h-sqrt(sqr), h+sqrt(sqr)]
        return "\\(" + latex(solution_set[0]) + ", " + latex(solution_set[1]) + "\\)"
    else:
        solution = 'There is no real solution.'
        return solution
def gendata(inseed):
    inseed = int(inseed*10**16 % 2**32)
    random.seed(inseed)
    sqr = random.choice([1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 16, 25, 36, 49, 64, 81, 100, 121])
    parity = random.choice([-1,1,1])
    #parity = -1
    a=0
    while a ==0:
        a = random.randint(-7,7)
    b = int(random.normal(0, 7))
    h = 0
    while h ==0:
        h = random.randint(-9,9)
    data = {'sqr':sqr, 'a':a, 'b': b, 'h': h, 'parity': parity}
    return data

seed = random.random()
#seed = 1
print(gettext(seed))
#print(getanswer(seed))
#data = gendata(seed)
#parity = data['parity']
#sqr = data['sqr']
#h = data['h']
#print(checkanswer(seed, '{h}-sqrt({sqr}), {h}+sqrt({sqr})'.format(h=h, sqr=sqr)))
#print(checkanswer(seed, 'No real Solution'))
