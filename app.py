from flask import *
import importlib
from flask_sqlalchemy import *
from flask_login import login_user, current_user, LoginManager, UserMixin
from random import *
from os import path, listdir
import json
from datetime import *

app = Flask(__name__)

app.secret_key = b'change this secret key asap'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(db.Model):
    username = db.Column(db.String(100),primary_key=True)
    masteries = db.Column(db.Text(),default = {})
    is_authenticated = False
    is_active = True
    is_anonymous = False
    def get_id(self):
        return self.username
    def __str__(self):
        return self.username
    def __repr__(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    allusers = User.query.order_by(User.username).all()
    for current in allusers:
        if(current.username == username):
            return current

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def loginpost():
    check_username = request.form['username']
    allusers = User.query.order_by(User.username).all()
    for current in allusers:
        if(current.username == check_username):
            try:
                login_user(current)
            except:
                return render_template('error.html',errortext = "LOGIN FAILED")
            return redirect('/')
    return "USERNAME NOT FOUND"

@app.route('/login', methods=['GET'])
def loginget():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def registerpost():
    new_username = request.form['username']
    newuser = User(username = new_username,masteries = '{}')
    try:
        login_user(newuser)
        db.session.add(newuser)
        db.session.commit()
    except:
        return render_template('error.html', errortext = "registration error")
    return redirect('/')

@app.route('/register', methods=['GET'])
def registerget():
    return render_template('register.html')

@app.route('/myskills')
def myskills():
    masteries = getmasteries(current_user.username)
    ownedskills = masteries.keys()
    allskills = [f for f in os.listdir('questions') if os.path.isfile(os.path.join('questions', f))] 
    notowned = [skill for skill in allskills if not (skill in ownedskills)]
    for skill in notowned:
        subject = skill
        user = current_user.username
        masterydata = {}
        masterydata['history'] = []
        masterydata['due'] = int(datetime.today().timestamp())
        masterydata['hasbeencorrect'] = 0
        updatemasteries(user,subject,masterydata)
    masteries = getmasteries(current_user.username)
    subjectlist = sorted(masteries.keys())
    masterylist = []
    for subj in subjectlist:
        duedatefull = datetime.fromtimestamp(masteries[subj]['due'])
        isdue = duedatefull < datetime.today()
        duedate = str(duedatefull.month) + '/' + str(duedatefull.day)
        hasbeencorrect = 'yes' if(masteries[subj]['hasbeencorrect']) else 'no'
        masterylist.append((subj,duedate,hasbeencorrect,isdue))
    return render_template('myskills.html', masterylist=masterylist)

@app.route('/addskills')    
def addskills():
    masteries = getmasteries(current_user.username)
    ownedskills = masteries.keys()
    allskills = [f for f in os.listdir('questions') if os.path.isfile(os.path.join('questions', f))] 
    notowned = [skill for skill in allskills if not (skill in ownedskills)]
    return render_template('addskills.html',notowned=notowned)

@app.route('/add/<string:skill>')
def add(skill):
    subject = skill
    user = current_user.username
    masterydata = {}
    masterydata['history'] = []
    masterydata['due'] = int(datetime.today().timestamp())
    masterydata['hasbeencorrect'] = 0
    updatemasteries(user,subject,masterydata)
    return redirect('/addskills')

@app.route('/practice/<string:skill>',methods=['GET'])
def practice(skill):
    skillclass = importlib.import_module('questions.'+skill[:-3])
    seed = random()
    session['seed'] = seed
    return render_template('practice.html',questiontext=skillclass.gettext(seed),questionname=skill)

@app.route('/practice/<string:skill>',methods=['POST'])
def practicecheck(skill):
    skillclass = importlib.import_module('questions.'+skill[:-3])
    seed = session['seed']
    #correctanswers = skillclass.getanswer(seed)
    useranswer = request.form['answer']
    if skillclass.checkanswer(seed,useranswer):
        '''
        currentmasteries = getsubjectmastery(current_user.username,skill)
        currentmasteries['hasbeencorrect'] = 1
        currentmasteries['history'].append((int(datetime.now().timestamp()),1))
        currentmasteries['due'] = calculatedue(currentmasteries)
        updatemasteries(current_user.username,skill,currentmasteries)
        '''
        return render_template('correct.html')
        '''
    currentmasteries = getsubjectmastery(current_user.username,skill)
    currentmasteries['history'].append((int(datetime.now().timestamp()),0))
    currentmasteries['due'] = calculatedue(currentmasteries)
    updatemasteries(current_user.username,skill,currentmasteries)
    '''
    correctanswer = skillclass.getanswer(seed)
    return render_template('incorrect.html', skill=skill,correctanswer=correctanswer)

@app.route('/test/<string:skill>',methods=['GET'])
def test(skill):
    skillclass = importlib.import_module('questions.'+skill[:-3])
    seed = random()
    session['seed'] = seed
    return render_template('test.html',questiontext=skillclass.gettext(seed),questionname=skill)

@app.route('/test/<string:skill>',methods=['POST'])
def testcheck(skill):
    skillclass = importlib.import_module('questions.'+skill[:-3])
    seed = session['seed']
    #correctanswers = skillclass.getanswer(seed)
    useranswer = request.form['answer']
    if skillclass.checkanswer(seed,useranswer):
        currentmasteries = getsubjectmastery(current_user.username,skill)
        currentmasteries['hasbeencorrect'] = 1
        currentmasteries['history'].append((int(datetime.now().timestamp()),1))
        currentmasteries['due'] = calculatedue(currentmasteries)
        updatemasteries(current_user.username,skill,currentmasteries)
        return render_template('correct.html')
    currentmasteries = getsubjectmastery(current_user.username,skill)
    currentmasteries['history'].append((int(datetime.now().timestamp()),0))
    currentmasteries['due'] = calculatedue(currentmasteries)
    updatemasteries(current_user.username,skill,currentmasteries)
    correctanswer = skillclass.getanswer(seed)
    return render_template('incorrect.html', skill=skill,correctanswer=correctanswer)

@app.route('/studentdata')
def studentdata():
    allusers = User.query.order_by(User.username).all()
    allskills = [f for f in os.listdir('questions') if os.path.isfile(os.path.join('questions', f))] 
    allrows = []
    for current in allusers:
        currentmasteries = getmasteries(current.username)
        userskills = currentmasteries.keys()
        currentrow = []
        currentrow.append(current.username)
        for skill in allskills:
            if skill in userskills:
                if(currentmasteries[skill]['hasbeencorrect']):
                    currentrow.append('yes')
                else:
                    currentrow.append('no')
            else:
                currentrow.append('no')
        allrows.append(currentrow)
    return render_template('studentdata.html',allskills=allskills,allrows=allrows)

def updatemasteries(user,subject,masterydata):
    masteries = getmasteries(user)
    masteries[subject] = masterydata
    masterystring = json.dumps(masteries)
    currentuser = User.query.filter_by(username = user).first()
    currentuser.masteries = masterystring
    db.session.commit()

def getmasteries(user):
    currentuser = User.query.filter_by(username = user).first()
    masteries = json.loads(currentuser.masteries)
    return masteries

def getsubjectmastery(user,subject):
    masteries = getmasteries(user)
    return masteries[subject]

def calculatedue(masteries):
    lastattempt = masteries['history'][-1]
    totalattempts = len(masteries['history'])
    if(lastattempt[1]):#on correct, update the interval until the next question.
        timecorrect = timewithoutmistake(masteries['history'])
        if (timecorrect < timedelta(days=1).total_seconds()):
            return int((datetime.today() + timedelta(days=1)).timestamp())
        else:
            return int((datetime.today() + timedelta(seconds=1*timecorrect)).timestamp())#this line could be changed to give faster or slower spacing
    else:#on incorrect, return current time.
        return int(datetime.today().timestamp())

def timewithoutmistake(history):#calculate the amount of time which has passed since a student has made a mistake on a problem type
    if(len(history) == 0):
        return 0
    for i in range(len(history)):
        testattempt = history[-i]
        print(testattempt[1])
        if(not testattempt[1]):
            firstright = history[-i+1]
            return datetime.now().timestamp() - firstright[0]
    return datetime.now().timestamp() - history[0][0]
'''
def checkanswer(useranswer,correctanswers):
    for correctans in correctanswers:
        if isfloat(correctans):
            if(checkfloat(useranswer,correctans)):
                return 1
        else:
            if(checkstring(useranswer,correctans)):
                return 1
    return 0

def isfloat(floatstr):
    try:
        float(floatstr)
        return 1
    except ValueError:
        return 0

def checkfloat(userans,correctans):
    return abs(userans - correctans) < .1

def checkstring(userans,correctans):
    return userans == correctans
'''

if __name__ == "__main__":
    app.run(debug=True,threaded=True,host = '0.0.0.0')
