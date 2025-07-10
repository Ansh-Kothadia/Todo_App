# from app import create_app, db
# from app.models import Task

# app=create_app()

# with app.app_context():
#     db.create_all()


# if __name__=="__main__":
#     app.run(debug=True)
# from app import create_app, db
# from app.models import Task  # ✅ This forces model registration

# app = create_app()

# with app.app_context():
#     db.create_all()  # ✅ This now knows about Task
#     print("Created tables:", db.engine.table_names())

# if __name__ == "__main__":
#     app.run(debug=True)
from sqlalchemy import inspect
from app import create_app, db
from app.models import Task  # Force model import!

app = create_app()

with app.app_context():
    db.create_all()

    # ✅ Use SQLAlchemy Inspector to list table names (modern way)
    inspector = inspect(db.engine)
    print("Created tables:", inspector.get_table_names())

if __name__ == "__main__":
    app.run(debug=True)

