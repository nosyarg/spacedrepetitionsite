from sympy import*
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import random
def gettext(inseed):
    data = gendata(inseed)
    m = data['m']
    p = data['p']
    n = data['n']
    q = data['q']
    x = Symbol('x')
    expr = (m*x+p)*(n*x+q)
    return "Solve by factoring: \\(" + latex(expand(expr)) + " = 0 \\)" +"\n" + "(If you have multiple answers, enter them separated by a comma.)"
def checkanswer(inseed, user_answer):
    data = gendata(inseed)
    m = data['m']
    p = data['p']
    n = data['n']
    q = data['q']
    answer = set([Rational(-p,m), Rational(-q,n)])
    user_answer = user_answer.split(",")
    user_answer = [parse_expr(a) for a in user_answer]
    #print(user_answer)
    user_answer = set(user_answer)
    return answer == user_answer
def getanswer(inseed):
    data = gendata(inseed)
    m = data['m']
    p = data['p']
    n = data['n']
    q = data['q']
    solution_set = [Rational(-p,m), Rational(-q,n)]
    if Rational(-p,m) == Rational(-q,n):
        return "\\(" + latex(solution_set[0]) + "\\)"
    else:
        return "\\(" + latex(solution_set[0]) + ", " + latex(solution_set[1]) + "\\)"
def gendata(inseed):
    random.seed(inseed)
    m = random.choice([1, 2, 3, 5])
    p = random.choice([-5,-3,-2,-1,1,2,3,5])
    n = random.choice([-5,-3,-2,-1,1,2,3,5])
    q = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
    data = {'m':m, 'p':p, 'n': n, 'q':q}
    return data


#print(gettext(0))
#print(getanswer(0))
#print(checkanswer(0, '-1'))
#seed = random.random()
#print(checkanswer(seed, gendata(seed)))
#print(gendata(0))
#print(gendata(0))