import os
import psycopg2
import openai
import uuid
from flask import Flask, redirect, render_template, request, url_for,session,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Role, UserRole, Permission
from models import CustomQuery  # import your custom query class
from actions.user_profile import create_user_profile, edit_user_profile, view_user_profile

app = Flask(__name__)
app.secret_key = "my_secret_key"
openai.api_key = os.getenv("OPENAI_API_KEY")## Call the API key under your account (in a secure way) 
                                            ##and store it in .env file
#engine = create_engine(os.getenv('DATABASE_URL'))
engine = create_engine("postgresql://admin:LK1joKixSkHrItiDOyhAneLKIrWwmsv9@dpg-cfp0vk82i3mo4bvetdjg-a.oregon-postgres.render.com/institute")
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
                return redirect(url_for('login'))
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
    # return "hi"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_password = request.form['password']
        # user = User.query.filter_by(username=username, password=password).first()
        with Session() as dbsession:
            user = dbsession.query(User).filter_by(user_name=user_name, user_password=user_password).first()
            # user = dbsession.query(User).filter_by(user_name=user_name).first()
            #user = dbsession.query(User).filter_by(user_name=user_name).filter_by(user_password=user_password).first()
        if user:
            # and user.user_password == user_password:
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

@app.route('/signup', methods=['POST'])
def signup():
    # get the form data
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']
    
    # check if the passwords match
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('login'))
    
    # check if the email or username is already taken
    with Session() as dbsession:
        user_email = dbsession.query(User).filter_by(user_email=email).first()
        user_name = dbsession.query(User).filter_by(user_name=name).first()
        if user_email or user_name:
            flash('Email or username already taken', 'error')
            return redirect(url_for('login'))
    
    # create a new user with the 'user' role
        user_id = str(uuid.uuid4())
        user = User(user_id=user_id, user_name=name, user_email=email, user_password=password)
        user_role = UserRole(user_id=user_id, role_id=1)
    # user.roles.append(Role(role_name='user'))
    with Session() as dbsession:
        dbsession.add(user)
        dbsession.add(user_role)
        dbsession.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
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
    active_role=roles[0]
    # print(username,roles,privileges,active_role)
    # Render the dashboard template with the session variables
    # print(privileges)
    return render_template('dashboard.html', username=username, roles=roles, privileges=privileges,active_role=active_role)
    #return "Congratulations!"

# @app.route('/<categoryName>/<privilege>')
@app.route('/<path:categoryName>/<privilege>')
def handle_category_privilege(categoryName, privilege):
    print("Category Name:", categoryName)
    print("Privilege:", privilege)
    print("session:", session.get('privileges'))
    if categoryName == "User Profile" and privilege == "Create":
        result = create_user_profile()
    elif categoryName == "User Profile" and privilege == "Edit":
        result = edit_user_profile()
    elif categoryName == "User Profile" and privilege == "View":
        result = view_user_profile()
    elif categoryName == "Account Settings" and privilege == "Edit":
        result = edit_account_settings()
    else:
        result = "Invalid categoryName or privilege value"
    return result


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
