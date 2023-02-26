import os
import psycopg2
import openai
from flask import Flask, redirect, render_template, request, url_for,session as session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from models import CustomQuery  # import your custom query class

app = Flask(__name__)
app.secret_key = "my_secret_key"
openai.api_key = os.getenv("OPENAI_API_KEY")## Call the API key under your account (in a secure way) 
                                            ##and store it in .env file
#db_url = os.environ.get('DATABASE_URL')
#conn = psycopg2.connect(db_url)
#engine = create_engine(os.getenv('DATABASE_URL'))
engine = create_engine("postgresql://admin:LK1joKixSkHrItiDOyhAneLKIrWwmsv9@dpg-cfp0vk82i3mo4bvetdjg-a.oregon-postgres.render.com/institute")
Base.metadata.create_all(bind=engine)
# Session = sessionmaker(bind=engine)
# Session = sessionmaker(bind=engine, query_class=CustomQuery)
# Session = sessionmaker(bind=engine, query_class=CustomQuery)()
# create a session factory bound to the engine and using the custom query class
Session = sessionmaker(bind=engine, query_cls=CustomQuery)
dbsession = Session()

# create a new user
#user = User(name='John', email='john@example.com', password='secret')
#session.add(user)
#session.commit()

# retrieve all users
#users = session.query(User).all()
#print(users)


#@app.route("/", methods=("GET", "POST"))
#def index():
 #   if request.method == "POST":
  #      intext = request.form["query"]
   #     response = GPT_Completion(intext)
    #    return render_template('creation.html', result=response)

    #result = request.args.get("result")
    #return render_template("index.html", result=result)
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            if session.get('role') != role and role != "ANY":
                return redirect(url_for('home'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
 
# @app.route('/')
# def index():
#     return render_template('login.html')
@app.route('/')
@login_required()
def index():
    return render_template('login.html')

@app.route('/dashboard')
@login_required()
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # user = User.query.filter_by(username=username, password=password).first()
        with Session() as dbsession:
            user = dbsession.query(User).filter_by(username=username, password=password).first()
        if user:
            session.update({'logged_in': True, 'username':user.username,'role':user.role})
            print("done")
            return redirect(url_for('dashboard'))

        else:
            print("undone")
            return render_template('login.html', error='Invalid username or password.')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    return f'Thank you for signing up, {name}! We will send a confirmation email to {email}.'

@app.route('/add_user/<string:id>/<string:name>/<string:password>/<string:role>', methods=['GET'])
def add_user(id, name, password, role):
    # session = Session()
    user = User(id=id, username=name, password=password, role=role)
    dbsession.add(user)
    dbsession.commit()
    dbsession.close()
    
    return 'User added successfully'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
