from flask import *
from flask_sqlalchemy import *
from flask_login import login_user, current_user, LoginManager, UserMixin
from random import *

app = Flask(__name__)

app.secret_key = b'change this secret key asap'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db',
    'questions': 'sqlite:///questions.db',
    'problems': 'sqlite:///problems.db',
    'assessments': 'sqlite:///assessments.db'
}
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(db.Model):
    __bind_key__ = 'users'
    username = db.Column(db.String(100),primary_key=True)
    is_authenticated = False
    is_active = True
    is_anonymous = False
    def get_id(self):
        return self.username
    def __str__(self):
        return self.username
    def __repr__(self):
        return self.username

class Question(db.Model):
    __bind_key__ = 'questions'
    idnum = db.Column(db.Integer(),primary_key=True)
    typename = db.Column(db.String(100),nullable=True) 
    inputs = db.Column(db.String(1000),nullable=False) 
    answer = db.Column(db.String(1000),nullable=False) 

class Problem(db.Model):
    __bind_key__ = 'problems'
    idnum = db.Column(db.Integer(),primary_key=True)
    text = db.Column(db.String(100),nullable=True) 
    inputs = db.Column(db.String(1000),nullable=True) 
    answer = db.Column(db.String(1000),nullable=False) 

class Assessment(db.Model):
    __bind_key__ = 'assessments'
    idnum = db.Column(db.Integer(),primary_key=True)
    owner = db.Column(db.String(1000))
    questionlist = db.Column(db.String(10000))
    seed = db.Column(db.Integer())

@login_manager.user_loader
def load_user(username):
    allusers = User.query.order_by(User.username).all()
    for current in allusers:
        if(current.username == username):
            return current

@app.route('/viewassessment/<int:idnum>')
def viewassignment(idnum):
    return "VIEWING" + str(idnum)

@app.route('/assess/<int:idnum>')
def assess(idnum):
    allassessments = Assessment.query.order_by(Assessment.idnum).all()
    for current in allassessments:
        if(current.idnum == idnum):
           thisassessment = current 
    problemnums = eval(thisassessment.questionlist)
    questions = []
    for i in problemnums:
        question = Problem.query.filter_by(idnum = i).first()
        questions.append(question)
    return render_template('assess.html',questions=questions)

@app.route('/availableassessments')
def availableassessments():
    assessments = Assessment.query.order_by(Assessment.idnum)
    return render_template('availableassessments.html',assessments=assessments)

@app.route('/newassessment', methods=['GET'])
def newassessmentget():
    return render_template('newassessment.html')

@app.route('/newassessment', methods=['POST'])
def newassessmentpost():
    numquestions = int(request.form['numquestions'])
    inputlist = []
    for i in range(numquestions):
        import questions.factoring
        a = int(10*random()+1)
        print(a)
        b = int(10*random()+1)
        print(b)
        c = -int(10*random()+1)
        print(c)
        if(db.session.query(db.func.max(Problem.idnum)).scalar()== None):
            newid = 0
        else:
            newid = db.session.query(db.func.max(Problem.idnum)).scalar()+1
        nextproblem = Problem(idnum = newid+1,text = questions.factoring.gettext(a,b,c),answer = str(questions.factoring.getanswer(a,b,c)))
        try:
            __bind_key__ = 'problem'
            db.session.add(nextproblem)
            db.session.commit()
        except:
            return('problem creating assessment')
        inputlist.append(nextproblem.idnum)
    if(db.session.query(db.func.max(Assessment.idnum)).scalar()== None):
        newid = 0
    else:
        newid = db.session.query(db.func.max(Assessment.idnum)).scalar()+1
    completeassessment = Assessment(idnum = newid,owner = current_user.username,questionlist = str(inputlist))
    try:
        __bind_key__ = 'assessment'
        db.session.add(completeassessment)
        db.session.commit()
    except:
        return('problem creating assessment')
    return render_template('newassessment.html')

@app.route('/assessments')
def assessments():
    return render_template('assessments.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myassessments')
def myassessments():
    assessments = Assessment.query.order_by(Assessment.idnum)
    return render_template('myassessments.html',assessments=assessments)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        __bind_key__ = 'users'
        check_username = request.form['username']
        allusers = User.query.order_by(User.username).all()
        for current in allusers:
            if(current.username == check_username):
                login_user(current)
                return redirect('/')
        return "USERNAME NOT FOUND"
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        newuser = User(username = new_username)
        login_user(newuser)
        try:
            __bind_key__ = 'users'
            db.session.add(newuser)
            db.session.commit()
            return redirect('/')
        except:
            return("ERROR WITH REGISTRATION")
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
