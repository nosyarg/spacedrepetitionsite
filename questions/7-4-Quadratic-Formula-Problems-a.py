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
    parity = data['parity']
    a = data['a']
    b = data['b']
    c = data['c']
    x = Symbol('x')
    return "Solve by any method.  \\(" + latex(expand(a*x**2+b*x+c)) \
            +" = 0 \\)" +"\n" \
            + "(If you have multiple answers, enter them separated by a comma. \n"\
            + "Enter square roots using 'sqrt', as in 'sqrt(2)' for \\(" \
            + latex(sqrt(2)) + "\\).)"
def checkanswer(inseed, user_answer):
    data = gendata(inseed)
    parity = data['parity']
    a = data['a']
    b = data['b']
    c = data['c']
    if parity == 1:
        answer = [(-b-sqrt(b**2-4*a*c))/(2*a), (-b+sqrt(b**2-4*a*c))/(2*a)]
        answer = [float(a) for a in answer]
        answer = set(answer)
        user_answer = user_answer.split(",")
        user_answer = [parse_expr(a, transformations=transformations) for a in user_answer]
        #print('user_answer', user_answer)
        user_answer = [float(a) for a in user_answer]
        #print(user_answer)
        user_answer = set(user_answer)
        #print('user answer is ', user_answer, ' and real answer is ', answer)
        return answer == user_answer
    else:
        return 'no' in user_answer or 'No' in user_answer or 'NO' in user_answer
def getanswer(inseed):
    data = gendata(inseed)
    parity = data['parity']
    a = data['a']
    b = data['b']
    c = data['c']
    if parity == 0:
        if b*2 - 4*a*c == 0:
            return "\\(" + latex(Rational(-b,2*a)) + "\\)"
    elif parity == 1:
        solution_set = [(-b-sqrt(b**2-4*a*c))/(2*a), (-b+sqrt(b**2-4*a*c))/(2*a)]
        return "\\(" + latex(solution_set[0]) + ", " + latex(solution_set[1]) + "\\)"
    else:
        solution = 'There is no real solution.'
        return solution
def gendata(inseed):
    inseed = int(inseed*10**16 % 2**32)
    random.seed(inseed)
    parity = random.choice([-1,1,1])
    a=0
    while a ==0:
        a = random.randint(-7,7)
    b = int(random.normal(0, 5))
    c = int(random.normal(0, 5))
    if parity == 1:
        while b**2 - 4*a*c < 0:
            a=0
            while a ==0:
                a = random.randint(-7,7)
            b = int(random.normal(0, 5))
            c = int(random.normal(0, 5))
    else:
        while b**2 - 4*a*c >= 0:
            a=0
            while a ==0:
                a = random.randint(-7,7)
            b = int(random.normal(0, 5))
            c = int(random.normal(0, 5))
    data = {'a':a, 'b': b, 'c': c, 'parity': parity}
    return data
seed = random.random()
##seed = 2
print(gettext(seed))
#print(getanswer(seed))
#data = gendata(seed)
#print(data)
#parity = data['parity']
#a = data['a']
#b = data['b']
#c = data['c']
#d = b**2 - 4*a*c
#if parity == 1:
#    print(checkanswer(seed, '(-{b}-sqrt({d}))/{w}, (-{b}+sqrt({d}))/{w}'.format(w=2*a, b=b, d=d)))
#else:
#    print(checkanswer(seed, 'No real Solution'))
