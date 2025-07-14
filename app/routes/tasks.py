#importing necessary libraries
from flask import Blueprint,render_template,request,session,redirect,url_for,flash
from app import db
from app.models import Task,Register,Transfer_Task


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
    if 'user_id' in session:
        user_id = session.get('user_id')
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
    if 'user_id' in session:
        user_id = session.get('user_id')
    Task.query.filter_by(user_id=session['user_id']).delete() 
    db.session.commit()
    flash('All tasks cleared!','info')
    return redirect(url_for('tasks.view_tasks'))



#Defining route for deleting particular task
@tasks_bp.route('/delete/<int:task_id>',methods=["POST"])
def delete(task_id):
    if 'user_id' in session:
        user_id = session.get('user_id')
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

    return render_template('description.html',data=data,task_id=task_id)



# @tasks_bp.route("/send_task",methods=["GET","POST"])
# def send_task():
#     send_data=None
#     transfer_data=None
#     task_id=request.args.get('task_id')
#     sender=session.get('user_id')
#     if request.method=="POST":
#         search_user=request.form.get('search')
#         send_data=Register.query.filter_by(username=search_user).first()
#         receiver=send_data.uid
#         if send_data:
#             flash('User Found !!!','success')
#             transfer_data={
#                 'sender_id':sender,
#                 'receiver_id':receiver,
#                 'task_id':task_id
#             }
#         else:
#             flash('User not found !!!','danger')
#     return render_template("send_task.html",send_data=send_data,transfer_data=transfer_data)
@tasks_bp.route("/send_task", methods=["GET", "POST"])
def send_task():
    send_data = None
    transfer_data = None
    if 'user_id' in session:
        user_id = session.get('user_id')
    # Step 1: Save task_id in session if it's a GET request
    if request.method == "GET":
        task_id = request.args.get('task_id')
        session['task_id_to_send'] = task_id

    sender = session.get('user_id')
    task_id = session.get('task_id_to_send')  # Step 2: retrieve it for POST

    if request.method == "POST":
        search_user = request.form.get('search')
        send_data = Register.query.filter_by(username=search_user).first()

        if send_data:
            flash('User Found !!!', 'success')
            receiver = send_data.uid
            transfer_data = {
                'sender_id': sender,
                'receiver_id': receiver,
                'task_id': task_id  # ✅ this will now be correct
            }
        else:
            flash('User not found !!!', 'danger')

    return render_template("send_task.html", send_data=send_data, transfer_data=transfer_data)

@tasks_bp.route('/transfer',methods=["POST"])
def transfer():
    if 'user_id' in session:
        user_id = session.get('user_id')
    sender_id = request.form.get("sender_id")
    receiver_id = request.form.get("receiver_id")
    task_id = request.form.get("task_id")

    if not sender_id or not receiver_id or not task_id:
        flash("Missing transfer data", "danger")
        return redirect(url_for("tasks.send_task"))
    
    new_transfer = Transfer_Task(sender_id=sender_id, receiver_id=receiver_id, task_id=task_id)
    db.session.add(new_transfer)
    db.session.commit()

    flash('Task Sent', 'success')
    return redirect(url_for('tasks.send_task'))


# @tasks_bp.route('/transfer',methods=["POST"])
# def transfer():
#     sender_id = request.form.get("sender_id")
#     receiver_id = request.form.get("receiver_id")
#     task_id = request.form.get("task_id")
    
#     if not sender_id or not receiver_id or not task_id:
#         flash("Missing transfer data", "danger")
#         return redirect(url_for("tasks.send_task"))
    
#     new_transfer = Transfer_Task(sender_id=sender_id,receiver_id=receiver_id,task_id=task_id)
#     db.session.add(new_transfer)
#     db.session.commit()
#     if new_transfer:
#         flash('Task Sended','success')
#     else:
#         flash('error occured','danger')
    
#     return redirect(url_for('tasks.send_task'))



# @tasks_bp.route('/notifications')
# def notifications():
#     if 'user_id' not in session:
#         return redirect(url_for('auth.login')) 
#     user_id=session.get('user_id')
#     received_tasks=Transfer_Task.query.filter_by(receiver_id=user_id).all()
    
#     task_details = []
#     for task in received_tasks:
#         task_details.append({
#         'sender_name': task.sender.username,
#         'title': task.task.title,
#         'description': task.task.description
#     })

#     return render_template('notification.html',task_details=task_details)

# @tasks_bp.route('/notifications')
# def notifications():
#     if 'user_id' in session:
#         user_id = session.get('user_id')
#         received_tasks = Transfer_Task.query.filter_by(receiver_id=user_id).all()

#         task_details = []
#         for task in received_tasks:
#             # Safety check: make sure related task and sender exist
#             if task.task and task.sender:
#                 task_details.append({
#                     'sender_name': task.sender.username,
#                     'title': task.task.title,
#                     'description': task.task.description
#                 })
#                 session['transfer_id']=task.transfer_id
#             else:
#                 # Optional: Log or handle broken reference
#                 print(f"Broken transfer record: {task.transfer_id}")

#         return render_template('notification.html', task_details=task_details,transfer_id=session['transfer_id'])
#     else:
#         return redirect(url_for('auth.login'))


@tasks_bp.route('/notifications')
def notifications():
    if 'user_id' in session:
        user_id = session.get('user_id')
        received_tasks = Transfer_Task.query.filter_by(receiver_id=user_id).all()

        task_details = []
        for task in received_tasks:
            if task.task and task.sender:
                task_details.append({
                    'sender_name': task.sender.username,
                    'title': task.task.title,
                    'description': task.task.description,
                    'transfer_id': task.transfer_id  # Add this line
                })

        return render_template('notification.html', task_details=task_details)
    else:
        return redirect(url_for('auth.login'))




@tasks_bp.route('/addNotification',methods=["POST","GET"])
def addNotify():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == "POST":
        title=request.form.get('title')
        description=request.form.get('description')
    
    add_notify=Task(title=title, status='Pending', user_id=session['user_id'],description=description)
    db.session.add(add_notify)
    db.session.commit()
    if add_notify:
        flash('task added successfully','success')
        deleteNotify=Transfer_Task.query.filter_by(transfer_id=session['transfer_id']).delete()
        db.session.commit()
    else:
        flash('task not added successfully','danger')
    
    return render_template('notification.html')


@tasks_bp.route('/deleteNotification/<int:transfer_id>')
def deleteNotify(transfer_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if transfer_id:
        deleteNotify=Transfer_Task.query.filter_by(transfer_id=transfer_id).delete()
        db.session.commit()
        if deleteNotify:
            flash('Notification Deleted','danger')
    
    return render_template('notification.html')

