from sympy import*
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import random
def gettext(inseed):
    expr = gendata(inseed)
    return "Completely factor the following: \\(" + latex(expand(expr)) + "\\)"
def checkanswer(inseed, user_answer):
    user_answer = user_answer.replace('^', '**')
    user_answer = parse_expr(user_answer, transformations=transformations)
    expr = gendata(inseed)
    answer = sympify(str((expr)))
    return answer == user_answer
def gendata(inseed):
    x = Symbol('x')
    random.seed(inseed)
    p = random.randint(-7,7)
    q = random.randint(-5,5)
    e = random.randint(2,6)
    expr = (x**e+p)*(x**e+q)
    return expr


#print(gettext(0))
seed = random.random()
print(checkanswer(seed, str(gendata(seed))))
#print(gendata(0))
#print(gendata(0))