from main.app import create_app, db



app = create_app()
with app.app_context():
    db.metadata.bind = db.engine

