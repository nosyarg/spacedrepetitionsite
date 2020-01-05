from sympy import*
import random
def gettext(inseed):
    p,q,e = gendata(inseed)
    x = Symbol('x')
    expr = (x+p)*(x+q)
    expr = expr.subs(x, x**e)
    return "Completely factor the following: \\(" + latex(expand(expr)) + "\\)"
def checkanswer(inseed, user_answer):
    p,q,e = gendata(inseed)
    x = Symbol('x')
    user_answer = sympify(user_answer)
    expr = (x**e+p)*(x**e+q)
    answer = factor(expr)
    if answer == user_answer:
      return True
    else:
      return False
def gendata(inseed):
    random.seed(inseed)
    p = random.randint(-7,7)
    q = random.randint(-5,5)
    e = random.randint(2,6)
    return (p,q,e)
