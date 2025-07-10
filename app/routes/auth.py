#importing necessary libraries
from flask import Blueprint,render_template,request,session,redirect,url_for,flash
from app import db
from app.models import Register

#Using the blueprint object for auth_bp 
auth_bp=Blueprint('auth',__name__)


#Defining route for login 
@auth_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')

        user=Register.query.filter_by(username=username).first()
        if user and user.password==password :
            session['user']=user.username
            session['user_id'] = user.uid 
            flash('Login Successfully','success')
            return redirect(url_for('tasks.view_tasks'))

        else:
            flash('Invalid username or password','danger')

    return render_template('login.html')


#Defining route for logout functionality
@auth_bp.route('/logout')
def logout():
    # session.pop('user', None)
    session.clear()
    flash('Logged Out','info')
    return redirect(url_for('auth.login'))


#Defining route for register functionality
@auth_bp.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")

        if username and password and email:
            new_register=Register(username=username,password=password,email=email)
            db.session.add(new_register)
            db.session.commit()
            flash('Successfully Registered','success')
    return render_template("register.html")