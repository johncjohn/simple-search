# user_profile.py - module that contains functions for different actions on new signed up users
from flask import Flask, redirect, render_template, request, url_for,session,flash
def create_user_profile():
    # perform create action for user profile
    
    return "Create User Profile"

def edit_user_profile():
    # perform edit action for user profile
    username = session.get('username')
    if request.method == 'POST':
        # process form data and save to database
        pass
    return render_template('pages/user_profile.html',username=username)
    # return "Edit User Profile"

def view_user_profile():
    # perform view action for user profile
    return "View User Profile"

def edit_account_settings():
    # perform edit action for account settings
    return "Edit Account Settings"
