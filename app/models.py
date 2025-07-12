from app import db

class Register(db.Model):
    __tablename__='register'
    uid=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(200),unique=True)
    role=db.Column(db.String(20),default="user")
    tasks = db.relationship('Task', backref='user', lazy=True)


class Task(db.Model):
    __tablename__='task'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(300), nullable=False)
    status=db.Column(db.String(20), default="Pending")
    user_id = db.Column(db.Integer, db.ForeignKey('register.uid'), nullable=False)



