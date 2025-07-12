#importing necessary libraries
from flask import Blueprint,render_template,request,session,redirect,url_for,flash
from app import db
from app.models import Task,Register


#Using the blueprint object for tasks_bp 
tasks_bp=Blueprint('tasks',__name__)


#Defining route for home page or view_tasks 
@tasks_bp.route('/')
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.filter_by(user_id=session['user_id']).all()

    return render_template('tasks.html',tasks=tasks)


#Defining route for add_tasks 
@tasks_bp.route('/add', methods=["POST"])
def add_task():
    if 'user_id' not in session:
        return redirect( url_for('auth.login'))
    
    title=request.form.get('title')
    description=request.form.get('description')

    if title:
        new_task = Task(title=title, status='Pending', user_id=session['user_id'],description=description)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully','success')

    return redirect(url_for('tasks.view_tasks'))



#Defining route for toggle_status 
@tasks_bp.route('/toggle/<int:task_id>',methods=["POST"])
def toggle_status(task_id):
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first() 

    if task:
        if task.status =='Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status ='Done'
        else:
            task.status = 'Pending'

        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))




#Defining route for clear_tasks 
@tasks_bp.route('/clear',methods=['POST'])
def clear_tasks():
    Task.query.filter_by(user_id=session['user_id']).delete() 
    db.session.commit()
    flash('All tasks cleared!','info')
    return redirect(url_for('tasks.view_tasks'))



#Defining route for deleting particular task
@tasks_bp.route('/delete/<int:task_id>',methods=["POST"])
def delete(task_id):
    Task.query.filter_by(user_id=session['user_id'],id=task_id).delete()
    db.session.commit()
    flash('task cleared!','info')
    return redirect(url_for('tasks.view_tasks'))



@tasks_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    else:
        user = Register.query.filter_by(uid=session['user_id']).first()

        return render_template('profile.html',data=user)


@tasks_bp.route('/description/<int:task_id>',methods=["GET","POST"])
def description(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    else:
       data= Task.query.filter_by(user_id=session['user_id'],id=task_id).first()

    return render_template('description.html',data=data)

# @tasks_bp.route('/profile')
# def profile():
#     if 'user_id' not in session:
#         return redirect(url_for('auth.login'))
    
#     user = Register.query.filter_by(uid=session['user_id']).first()
#     return render_template('profile.html', data=user)




@tasks_bp.route("/send_task",methods=["GET","POST"])
def send_task():
    send_data=None
    if request.method=="POST":
        search_user=request.form.get('search')
        send_data=Register.query.filter_by(username=search_user).first()
        if send_data:
            flash('User Found !!!','success')
        else:
            flash('User not found !!!','danger')
    return render_template("send_task.html",send_data=send_data)