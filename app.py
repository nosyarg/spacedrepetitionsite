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
    #__bind_key__ = 'users'
    username = db.Column(db.String(100),primary_key=True)
    masteries = db.Column(db.Text(),default = '{}')
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
    #__bind_key__ = 'users'
    check_username = request.form['username']
    allusers = User.query.order_by(User.username).all()
    for current in allusers:
        if(current.username == check_username):
            login_user(current)
            return redirect('/')
    return "USERNAME NOT FOUND"

@app.route('/login', methods=['GET'])
def loginget():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def registerpost():
    new_username = request.form['username']
    newuser = User(username = new_username,masteries = '{}')
    login_user(newuser)
    #__bind_key__ = 'users'
    db.session.add(newuser)
    db.session.commit()
    #os.mkdir('users/'+new_username)
    return redirect('/')

@app.route('/register', methods=['GET'])
def registerget():
    return render_template('register.html')

@app.route('/myskills')
def myskills():
    masteries = getmasteries(current_user.username)
    subjectlist = masteries.keys()
    masterylist = []
    for subj in subjectlist:
        duedatefull = datetime.fromtimestamp(masteries[subj]['due'])
        isdue = duedatefull < datetime.today()
        #print(duedatefull)
        #print(datetime.today())
        #print(isdue)
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
    #masterydata['due'] = int(datetime.today().strftime("%S"))
    masterydata['due'] = int(datetime.today().timestamp())
    masterydata['hasbeencorrect'] = 0
    updatemasteries(user,subject,masterydata)
    return redirect('/addskills')

@app.route('/practice/<string:skill>',methods=['GET'])
def practice(skill):
    skillclass = importlib.import_module('questions.'+skill[:-3])
    seed = random()
    seedstorage = open('seedstorage.txt','w')
    seedstorage.write(str(seed))
    seedstorage.close()
    return render_template('practice.html',questiontext=skillclass.gettext(seed),questionname=skill)

@app.route('/practice/<string:skill>',methods=['POST'])
def practicecheck(skill):
    skillclass = importlib.import_module('questions.'+skill[:-3])
    seedstorage = open('seedstorage.txt','r')
    seed = float(seedstorage.read())
    seedstorage.close()
    correctanswers = skillclass.getanswer(seed)
    useranswer = float(request.form['answer'])
    for ans in correctanswers:
        if abs(useranswer - ans) < .1:
            currentmasteries = getsubjectmastery(current_user.username,skill)
            currentmasteries['hasbeencorrect'] = 1
            #currentmasteries['history'].append((int(datetime.now().strftime("%S")),1))
            currentmasteries['history'].append((int(datetime.now().timestamp()),1))
            currentmasteries['due'] = calculatedue(currentmasteries)
            updatemasteries(current_user.username,skill,currentmasteries)
            return redirect('/myskills')
    currentmasteries = getsubjectmastery(current_user.username,skill)
    #currentmasteries['history'].append((int(datetime.now().strftime("%S")),0))
    currentmasteries['history'].append((int(datetime.now().timestamp()),0))
    currentmasteries['due'] = calculatedue(currentmasteries)
    updatemasteries(current_user.username,skill,currentmasteries)
    return 'incorrect!'

@app.route('/studentdata')
def studentdata():
    #__bind_key__ = 'users'
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

'''
def updatemasteries(user,subject,masterydata):
    masteries = getmasteries(user)
    masteries[subject] = masterydata
    masterystring = json.dumps(masteries)
    writefile = open('users/'+user+'/masteries.json','w')
    writefile.write(masterystring)
    writefile.close()

def getmasteries(user):
    if(not path.exists('users/'+user+'/masteries.json')):
        masteries = {}
    else:
        readfile = open('users/'+user+'/masteries.json','r')
        masteries = json.loads(readfile.read())
        readfile.close()
    return masteries
'''

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
        #return int((datetime.today() + timedelta(days=1)).strftime("%S"))
        timecorrect = timewithoutmistake(masteries['history'])
        if (timecorrect < timedelta(days=1).total_seconds()):
            return int((datetime.today() + timedelta(days=1)).timestamp())
        else:
            return int((datetime.today() + timedelta(seconds=timecorrect)).timestamp())
    else:#on incorrect, return current time.
        #return int(datetime.today().strftime("%S"))
        return int(datetime.today().timestamp())

def timewithoutmistake(history):
    if(len(history) == 0):
        #print('error handler')
        return 0
    for i in range(len(history)):
        testattempt = history[-i]
        print(testattempt[1])
        if(not testattempt[1]):
            firstright = history[-i+1]
            #print('loop')
            return datetime.now().timestamp() - firstright[0]
    #print('default')
    return datetime.now().timestamp() - history[0][0]


if __name__ == "__main__":
    app.run(debug=True)
