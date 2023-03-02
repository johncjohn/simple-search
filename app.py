import os
import psycopg2
import openai
from flask import Flask, redirect, render_template, request, url_for,session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role, UserRole, Permission
from models import CustomQuery  # import your custom query class

app = Flask(__name__)
app.secret_key = "my_secret_key"
openai.api_key = os.getenv("OPENAI_API_KEY")## Call the API key under your account (in a secure way) 
                                            ##and store it in .env file
engine = create_engine(os.getenv('DATABASE_URL'))
#engine = create_engine("postgresql://admin:LK1joKixSkHrItiDOyhAneLKIrWwmsv9@dpg-cfp0vk82i3mo4bvetdjg-a.oregon-postgres.render.com/institute")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine, query_cls=CustomQuery)
dbsession = Session()

from functools import wraps

def login_required(roles=['ANY']):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            if 'ANY' not in roles and session.get('roles') not in roles:
                return redirect(url_for('home'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# # Define a function to get the role names for a user

def get_role_names(user_name, dbsession):
    user = dbsession.query(User).filter_by(user_name=user_name).first()
    role_names = [role.role_name for role in user.roles]
    return role_names

def get_privileges(role_names, dbsession):
    privileges = {}
    for role_name in role_names:
        role = dbsession.query(Role).filter_by(role_name=role_name).first()
        permissions = role.permissions
        for permission in permissions:
            category = permission.category
            privilege = permission.privilege
            if role_name not in privileges:
                privileges[role_name] = {}
            if category not in privileges[role_name]:
                privileges[role_name][category] = []
            privileges[role_name][category].append(privilege)
    return privileges


# @app.route('/')
# def index():
#     return render_template('login.html')
@app.route('/')
@login_required()
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_password = request.form['password']
        # user = User.query.filter_by(username=username, password=password).first()
        with Session() as dbsession:
            user = dbsession.query(User).filter_by(user_name=user_name, user_password=user_password).first()
        if user:
            role_names = get_role_names(user_name, dbsession)
            privileges=get_privileges(role_names,dbsession)
            session.update({'logged_in': True, 'username':user.user_name, 'roles': role_names, 'privileges':privileges})
            print("done")
            return redirect(url_for('dashboard'))            
        else:
            print("undone")
            flash('Invalid username or password. Please try again.')
            return render_template('login.html', error='Invalid username or password.')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# @app.route('/submit', methods=['POST'])
# def submit():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     return f'Thank you for signing up, {name}! We will send a confirmation email to {email}.'

@app.route('/dashboard', methods=['GET'])
@login_required()
def dashboard():
    # Retrieve session variables
    username = session.get('username')
    roles = session.get('roles')
    privileges = session.get('privileges')
    print(username,roles,privileges)
    # Render the dashboard template with the session variables
    # return render_template('dashboard.html', username=username, roles=roles, privileges=privileges)
    return "Congratulations!"

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

@app.route('/role_permission/<int:permission_id>/<int:role_id>/<string:category>/<string:privilege>', methods=['GET'])
def add_role_permssion(permission_id, role_id,category,privilege):
    # session = Session()
    role_perm = Permission(permission_id=permission_id, role_id=role_id,category=category,privilege=privilege)
    dbsession.add(role_perm)
    dbsession.commit()
    dbsession.close()
    
    return 'Role to Permission mapping has been done successfully'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
