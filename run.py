from sqlalchemy import inspect
from app import create_app, db
from app.models import Task,Register  # Force model import!

app = create_app()

with app.app_context():
    db.create_all()

    # ✅ Use SQLAlchemy Inspector to list table names (modern way)
    inspector = inspect(db.engine)
    print("Created tables:", inspector.get_table_names())
    if not Register.query.filter_by(username='admin').first():
        admin = Register(
            username='admin',
            password='admin_password', 
            email='admin@gmail.com',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)

