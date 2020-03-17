"""
Solving a quadratic: only one x

a(x-h)^2 + b= c ... can result in no real solution.
"""
from decimal import *
from sympy import*
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from numpy import random
getcontext().prec=10
def gettext(inseed):
    data = gendata(inseed)
    print('gettext thinks data is ', data)
    a = N(data[0])
    b = N(data[1])
    c = data[2]
    which_type = data[5]
    if which_type == 'cannonball':
        v0 = data[3]
        theta = data[4]
        x = Symbol('x')
        #y = a*x**2+b*x+c
        fcn_latex = '{a:.6f}x^2+{b:.3f}x+{c}'.format(a=a, b=b, c=c)
        text = """The vertical height \\(y\\) above the ground of 
        a cannonball shot from an initial height of 
        \\({h0}\\) feet with an initial 
        velocity of \\({v0}\\) feet per second 
        and initial launch angle (measured from the ground) 
        of \\({theta}^\circ\\) can be given as a 
        function of the horizontal distance \\(x\\) it has traveled 
        from the launching point (if we neglect air resistance) 
        by
        \\[
                y(x) = {fcn_latex}
        \\]
        Find the position \\(x\\) away from the launching point at which the 
        cannonball crashes to Earth.
        (Be sure to include units in your answer, 
        separating the units from the numerical part of your answer with a space.)
               """.format(h0=c, v0=v0, theta=theta, fcn_latex=fcn_latex)
    else:
        starting_height = data[3]
        x = Symbol('t')
        y = a*x**2+b*x+c
        fcn_latex = latex(y)
        text = """
        Let's imagine that a bullet leaves the muzzle of a gun at a position of
        {starting_height} inches (let's call it 
        {c} feet) from the ground.  
        Say that the bullet travels at {b} feet per second.  
        According to Newton's law of gravitation, the bullet falls to Earth 
        (neglecting air resistance) with an acceleration of 32 feet per second 
        per second.  (FYI: Acceleration measures the rate of change of the velocity.)
        \n
        All that combines to give you the following model for the position 
        \\(y\\) of the bullet relative to the ground after \\(t\\) seconds
        \\[
                y(t) = {fcn_latex}
        \\]
        Your task: Figure how quickly the party-goers need to leave the area!!
        """.format(starting_height=starting_height, c=c, b=b, fcn_latex=fcn_latex)
    return text
def checkanswer(inseed, user_answer):
    data = gendata(inseed)
    print('checkanswer thinks data is', data)
    a = data[0]
    #print(a)
    b = data[1]
    c = data[2]
    which_type = data[5]
    answer = N((-b-sqrt(b**2-4*a*c))/(2*a))
    #answer = round(answer, 2)
    user_answer = user_answer.split(" ")
    #user_answer = [parse_expr(a, transformations=transformations) for a in user_answer]
    print('user_answer', user_answer, 'answer', answer)
    #print(user_answer)
    user_answer[0] = N(user_answer[0])
    print('user answer is ', user_answer, ' and real answer is ', answer)
    if which_type == 'cannonball':
        units = (user_answer[1] == 'ft') or (user_answer[1] == 'ft.') \
        or (user_answer[1] == 'Ft') \
        or (user_answer[1] == 'Ft.') \
        or (user_answer[1] == 'feet') \
        or (user_answer[1] == 'Feet') 
    else:
        units = (user_answer[1] == 's') or (user_answer[1] == 'sec') \
        or (user_answer[1] == 'sec.') \
        or (user_answer[1] == 'Sec') \
        or (user_answer[1] == 'Sec.') \
        or (user_answer[1] == 'seconds') \
        or (user_answer[1] == 'Seconds') 
    print('units='+ str(units))
    return abs(answer - user_answer[0]) < 0.005 and units
def getanswer(inseed):
    data = gendata(inseed)
    which_type = data[5]
    a = data[0]
    b = data[1]
    c = data[2]
    num_answer = (-b-sqrt(b**2-4*a*c))/(2*a)
    num_answer = N(num_answer)
    if which_type == 'cannonball':
        solution = '{ans} ft'.format(ans=num_answer)
    else:
        solution = '{ans} sec'.format(ans=num_answer)
    return solution
def gendata(inseed):
    inseed = int(inseed*10**16 % 2**32)
    random.seed(inseed)
    def cannonballdata():
        theta = random.randint(15,75)
        v0 = random.randint(328, 656)
        v0 = 800
        h0 = random.randint(4,30)
        c = h0
        voy = v0*sin(theta*pi/180)
        vox = v0*cos(theta*pi/180)
        b = round(voy/vox,3)
        a = round(-16/vox**2,6)
        #symb_a = Symbol('{0:5f}'.format(abs(a)))    
        #print([a,b,c])
        return [a, b, c, v0, theta]
    def bulletdata():
        starting_height = random.randint(75,95)
        c = round(starting_height/12.0,3)
        veloc_factor = random.randint(15,32)
        velocity = veloc_factor*100
        b = velocity
        a = -16        
        return [a, b, c, starting_height, 0]
    which_type = random.choice(['cannonball', 'bullet'])
    which_type = 'cannonball'
    if which_type == 'cannonball':
        data = cannonballdata()
    else:
        data =  bulletdata()
    data.append(which_type)
    return data
seed = random.random()
#seed = 2
print(gettext(seed))
print('answer ir ' + getanswer(seed))
data = gendata(seed)
print(data)
which_type = data[5]
a = data[0]
b = data[1]
c = data[2]
useranswer = (-b-sqrt(b**2-4*a*c))/(2*a)
useranswer = round(useranswer, 2)
print(checkanswer(seed, '{useranswer} ft'.format(useranswer=useranswer)))
