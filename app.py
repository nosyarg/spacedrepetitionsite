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
    return render_template('index.html',currentuser = current_user.username)

@app.route('/login', methods=['POST'])
def loginpost():
    check_username = request.form['username']
    allusers = User.query.order_by(User.username).all()
    for current in allusers:
        if(current.username == check_username):
            try:
                login_user(current)
            except:
                return render_template('error.html',errortext = "LOGIN FAILED",currentuser = current_user.username)
            return redirect('/')
    return "USERNAME NOT FOUND"

@app.route('/login', methods=['GET'])
def loginget():
    return render_template('login.html',currentuser = current_user.username)

@app.route('/register', methods=['POST'])
def registerpost():
    new_username = request.form['username']
    newuser = User(username = new_username,masteries = '{}')
    try:
        login_user(newuser)
        db.session.add(newuser)
        db.session.commit()
    except:
        return render_template('error.html', errortext = "registration error",currentuser = current_user.username)
    return redirect('/')

@app.route('/register', methods=['GET'])
def registerget():
    return render_template('register.html',currentuser = current_user.username)

@app.route('/myskills')
def myskills():
    masteries = getmasteries(current_user.username)
    subjectlist = masteries.keys()
    masterylist = []
    for subj in subjectlist:
        duedatefull = datetime.fromtimestamp(masteries[subj]['due'])
        isdue = duedatefull < datetime.today()
        duedate = str(duedatefull.month) + '/' + str(duedatefull.day)
        hasbeencorrect = 'yes' if(masteries[subj]['hasbeencorrect']) else 'no'
        masterylist.append((subj,duedate,hasbeencorrect,isdue))
    return render_template('myskills.html', masterylist=masterylist,currentuser = current_user.username)

@app.route('/addskills')    
def addskills():
    masteries = getmasteries(current_user.username)
    ownedskills = masteries.keys()
    allskills = [f for f in os.listdir('questions') if os.path.isfile(os.path.join('questions', f))] 
    notowned = [skill for skill in allskills if not (skill in ownedskills)]
    return render_template('addskills.html',notowned=notowned,currentuser = current_user.username)

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
    return render_template('practice.html',questiontext=skillclass.gettext(seed),questionname=skill,currentuser = current_user.username)

@app.route('/practice/<string:skill>',methods=['POST'])
def practicecheck(skill):
    skillclass = importlib.import_module('questions.'+skill[:-3])
    seed = session['seed']
    correctanswers = skillclass.getanswer(seed)
    useranswer = float(request.form['answer'])
    for ans in correctanswers:
        if abs(useranswer - ans) < .1:
            currentmasteries = getsubjectmastery(current_user.username,skill)
            currentmasteries['hasbeencorrect'] = 1
            currentmasteries['history'].append((int(datetime.now().timestamp()),1))
            currentmasteries['due'] = calculatedue(currentmasteries)
            updatemasteries(current_user.username,skill,currentmasteries)
            return redirect('/myskills')
    currentmasteries = getsubjectmastery(current_user.username,skill)
    currentmasteries['history'].append((int(datetime.now().timestamp()),0))
    currentmasteries['due'] = calculatedue(currentmasteries)
    updatemasteries(current_user.username,skill,currentmasteries)
    return render_template('error.html', errortext = 'incorrect!',currentuser = current_user.username)

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
    return render_template('studentdata.html',allskills=allskills,allrows=allrows,currentuser = current_user.username)

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
    if(lastattempt[1]):
        timecorrect = timewithoutmistake(masteries['history'])
        if (timecorrect < timedelta(days=1).total_seconds()):
            return int((datetime.today() + timedelta(days=1)).timestamp())
        else:
            return int((datetime.today() + timedelta(seconds=timecorrect)).timestamp())
    else:#on incorrect, return current time.
        return int(datetime.today().timestamp())

def timewithoutmistake(history):
    if(len(history) == 0):
        return 0
    for i in range(len(history)):
        testattempt = history[-i]
        print(testattempt[1])
        if(not testattempt[1]):
            firstright = history[-i+1]
            return datetime.now().timestamp() - firstright[0]
    return datetime.now().timestamp() - history[0][0]


if __name__ == "__main__":
    app.run(debug=True)
