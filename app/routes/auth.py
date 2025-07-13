#importing necessary libraries
from flask import Blueprint,render_template,request,session,redirect,url_for,flash,abort
from app import bcrypt
from app import db
from app.models import Register,Task,Transfer_Task

#Using the blueprint object for auth_bp 
auth_bp=Blueprint('auth',__name__)




#Defining route for login 
@auth_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')

        user=Register.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password) :
            session['user']=user.username
            session['user_id'] = user.uid 
            session['role']=user.role
            flash('Login Successfully','success')

            if session.get('user_id') and session.get('role') == 'admin':
                return redirect(url_for('auth.admin'))
            else:
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
        hash_password=bcrypt.generate_password_hash(password).decode('utf-8')

        if username and password and email:
            existing_user = Register.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists', 'danger')
                return redirect(url_for('auth.register'))
            new_register=Register(username=username,password=hash_password,email=email)
            db.session.add(new_register)
            db.session.commit()
            flash('Successfully Registered','success')
    return render_template("register.html")


@auth_bp.route('/admin')
def admin():
    if session.get('user_id') and session.get('role') == 'admin':
        Users=Register.query.all()
        return render_template('admin.html',Users=Users,session=session)
    else:
        return abort(403)
    

@auth_bp.route('/admin_task')
def admin_task():
    if session.get('user_id') and session.get('role') == 'admin':
        Tasks=Task.query.all()
        return render_template('admin_task.html',Tasks=Tasks,session=session)
    else:
        return abort(403)
    
# @auth_bp.route('/admin_notification')
# def admin_notification():
#     if session.get('user_id') and session.get('role') == 'admin':
#         Tasks=Transfer_Task.query.all()
#         return render_template('admin_notification.html',Tasks=Tasks,session=session)
#     else:
#         return abort(403)
@auth_bp.route('/admin_transfer')
def admin_transfer():
    if session.get('user_id') and session.get('role') == 'admin':
        Transfers = Transfer_Task.query.all()
        return render_template('admin_transfer.html', Transfers=Transfers, session=session)
    else:
        return abort(403)
