from app import db,bcrypt

class Register(db.Model):
    __tablename__='register'
    uid=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(200),unique=True)
    role=db.Column(db.String(20),default="user")
    tasks = db.relationship('Task', backref='user', lazy=True)

    # def set_password(self, raw_password):
    #     self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    # def check_password(self, raw_password):
    #     return bcrypt.check_password_hash(self.password, raw_password)


class Task(db.Model):
    __tablename__='task'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(300), nullable=False)
    status=db.Column(db.String(20), default="Pending")
    user_id = db.Column(db.Integer, db.ForeignKey('register.uid'), nullable=False)


class Transfer_Task(db.Model):
    __tablename__ = 'transfer_task'
    transfer_id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    sender_id = db.Column(db.Integer, db.ForeignKey('register.uid'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('register.uid'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    # Relationships (optional but useful)
    sender = db.relationship('Register', foreign_keys=[sender_id], backref='sent_tasks')
    receiver = db.relationship('Register', foreign_keys=[receiver_id], backref='received_tasks')
    task = db.relationship('Task', foreign_keys=[task_id], backref='transfers')


