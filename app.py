import os
import psycopg2
import openai
from flask import Flask, redirect, render_template, request, url_for,session as session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role, UserRole
from models import CustomQuery  # import your custom query class

app = Flask(__name__)
app.secret_key = "my_secret_key"
openai.api_key = os.getenv("OPENAI_API_KEY")## Call the API key under your account (in a secure way) 
                                            ##and store it in .env file
# db_url = os.environ.get('DATABASE_URL')
#conn = psycopg2.connect(db_url)
engine = create_engine(os.getenv('DATABASE_URL'))
#engine = create_engine("postgresql://admin:LK1joKixSkHrItiDOyhAneLKIrWwmsv9@dpg-cfp0vk82i3mo4bvetdjg-a.oregon-postgres.render.com/institute")
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

# # Define a function to get the role names for a user
# def get_role_names(user_name):
#     return [roles.role_name for role in user.roles]

def get_role_names(user_name):
    session = Session()
    user = session.query(User).filter_by(user_name=user_name).first()
    role_names = [role.role_name for role in user.roles]
    session.close()
    return role_names
 
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
    # Get the current user and roles from the session
    current_user = {
        "username": session['username'],
        "roles": session['roles']
    }
    # Define the available privileges for each role
    privileges = {
        "admin": {
            "Academic": ["Add", "Edit", "Delete"],
            "Courses": ["Add", "Edit", "Delete"],
            "Enrollment": ["View", "Add", "Edit", "Delete"]
        },
        "director": {
            "Academic": ["View"],
            "Courses": ["View", "Add"],
            "Enrollment": ["View"]
        },
        "student": {
            "Academic": ["View"],
            "Courses": ["View"],
            "Enrollment": ["View", "Add"]
        }
    }

    # Get the privileges of each role for the current user
    user_privileges = {}
    for role_name in current_user["roles"]:
        role_privileges = privileges.get(role_name, {})
        user_privileges.update(role_privileges)

    # Render the dashboard template with the user information and privileges
    return render_template('dashboard.html', user=current_user, privileges=user_privileges)

    # return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_password = request.form['password']
        # user = User.query.filter_by(username=username, password=password).first()
        with Session() as dbsession:
            user = dbsession.query(User).filter_by(user_name=user_name, user_password=user_password).first()
        if user:
            # session.update({'logged_in': True, 'username':user.username,'role':user.role})
            session.update({'logged_in': True, 'username':user.user_name,'roles':get_role_names(user_name)})
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

@app.route('/add_user/<string:id>/<string:name>/<string:password>', methods=['GET'])
def add_user(id, name, password):
    # session = Session()
    user = User(user_id=id, user_name=name, user_password=password)
    dbsession.add(user)
    dbsession.commit()
    dbsession.close()
    return 'User added successfully'

@app.route('/add_role/<int:id>/<string:role_name>', methods=['GET'])
def add_role(id, role_name):
    # session = Session()
    role = Role(role_id=id, role_name=role_name)
    dbsession.add(role)
    dbsession.commit()
    dbsession.close()
    
    return 'Role added successfully'

@app.route('/user_role/<string:user_id>/<int:role_id>', methods=['GET'])
def add_user_role(user_id, role_id):
    # session = Session()
    user_role = UserRole(user_id=user_id, role_id=role_id)
    dbsession.add(user_role)
    dbsession.commit()
    dbsession.close()
    
    return 'User to Role mapping has been done successfully'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
