"""
Solving a quadratic: only one x

ax^2 + b= c ... can result in no real solution.
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
    c = a*parity*sqr + b
    x = Symbol('x')
    return "Solve by factoring: \\(" + latex(expand(a*x**2+b)) \
            +" =" + latex(c) + "\\)" +"\n\n" \
            + "(If you have multiple answers, enter them separated by a comma. \n\n"\
            + "Enter square roots using 'sqrt', as in 'sqrt(2)' for \\(" \
            + latex(sqrt(2)) + "\\).)"
def checkanswer(inseed, user_answer):
    data = gendata(inseed)
    sqr = data['sqr']
    parity = data['parity']
    if parity == 1:
        answer = set([-sqrt(sqr), sqrt(sqr)])
        user_answer = user_answer.split(",")
        user_answer = [parse_expr(a, transformations=transformations) for a in user_answer]
        #print(user_answer)
        user_answer = set(user_answer)
        return answer == user_answer
    else:
        return 'no' in user_answer or 'No' in user_answer or 'NO' in user_answer
        
def getanswer(inseed):
    data = gendata(inseed)
    sqr = data['sqr']
    parity = data['parity']
    if parity == 1:
        solution_set = [-sqrt(parity*sqr), sqrt(parity*sqr)]
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
    data = {'sqr':sqr, 'a':a, 'b': b, 'parity': parity}
    return data

seed = random.random()
#seed = 1
print(gettext(seed))
print(getanswer(seed))
data = gendata(seed)
parity = data['parity']
sqr = data['sqr']
print(checkanswer(seed, '-sqrt({0}), sqrt({0})'.format(sqr)))
print(checkanswer(seed, 'No real Solution'))
#seed = random.random()
#print(checkanswer(seed, gendata(seed)))
#print(gendata(0))
#print(gendata(0))