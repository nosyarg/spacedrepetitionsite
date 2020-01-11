from sympy import*
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import random

def gendata(inseed):
    print('inseed:' + str(inseed))
    random.seed(inseed)
    p = 0
    while p == 0:
        p = random.randint(-7,7)
        q = 0
    while q ==0:
        q = random.randint(-5,5)
        e = random.randint(2,6)
        x = Symbol('x')
    quadraticPatternExpr = (x**e-p)*(x**e-q)
    
    random.seed(inseed)
    m = random.randint(2, 5)
    p = random.choice([-5,-3,-2,-1,1,2, 3, 5])
    n = random.choice([-5,-3,-2,-1,1,2, 3, 5])
    q = random.choice([-5,-3,-2,-1,1,2, 3, 5])
    fancyFactorExpr = (m*x+p)*(n*x+q)    
    
    random.seed(inseed)
    a = random.randint(1,9)
    b = random.randint(1,9)
    sign1 = random.choice([-1,1])
    sign2 = random.choice([-1,1])
    x, t, r, y= symbols('x t r y')
    variables = random.choice([(x,1),(x,y),(r,t),(1,y)])        
    A = a*variables[0]
    B1 = sign1*b*variables[1]
    B2 = sign2*b*variables[1]    
    specialPatternExpr = (A+B1)*(A+B2)    
    
    random.seed(inseed)
    a = 0
    while a==0:
        a = random.randint(-5,5)
    b = 0
    while b==0:
        b = random.randint(-5,5)
    c = 0
    while c==0:
        c = random.randint(-5,5)
    d = 0
    while d==0:
        d = random.randint(-5,5)
    x, t, r, y= symbols('x t r y')    #variables = random.choice([(x,1),(x,y),(r,t)])
    variables = [x,1]        
    A = a*variables[0]**2
    C = c*variables[1]
    B = b*variables[0]
    D = d*variables[1]    
    factorByGroupingExpr = (A+C)*(B+D)    

    random.seed(inseed)    
    p=0
    while p ==0:
    	p = random.randint(-9,9)
    q = 0
    while q == 0:
    	q = random.randint(-9,9)    
    b = p+q
    c = p*q    
    x=Symbol('x')    
    easyFactorExpr = x**2+b*x+c   
    
    random.seed(inseed)
    A = 0
    while A == 0:
    	A = random.randint(-7,7)    
    e=random.randint(0,5)    
    GCF = A*x**e    
    expr = random.choice([easyFactorExpr, factorByGroupingExpr, specialPatternExpr, fancyFactorExpr, quadraticPatternExpr])    
    #expr = quadraticPatternExpr
    expr = GCF*expr
    
    return expr




def gettext(inseed):
    #print(inseed)
    expr = gendata(inseed)
    return "Completely factor the following: \("+ latex(expand(expr)) + "\)"
def getanswer(inseed):
    expr = gendata(inseed)
    return "\(" + latex(factor(expr)) + "\)"

def checkanswer(inseed,useranswer):
    expr = gendata(inseed)
    #answer = factor(expr)
    answer = sympify(str(expr))
    #print(answer) 
    useranswer = useranswer.replace('^', '**')
    useranswer = parse_expr(useranswer, transformations=transformations)
    #print(useranswer)
    #print(sympify(str(useranswer)), answer) # hopefully found a workaround ... the problem is that sympify "does stuff" ("evaluates") expressions, changes them to suit it
    print(answer, useranswer)
    return useranswer == answer



#print(gettext(0))
#print(getanswer(0))
seed = random.random()
print(checkanswer(seed, str(gendata(seed))))

#print(gendata(0))
#print(gendata(0))
#print(gendata(0))