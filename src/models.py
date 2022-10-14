from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

#ESTA CLASE ES PARA TODOLIST -------------------------------------------------
class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tareas = db.Column(db.String(500), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.tareas

    def serialize(self):
        return {
            "id": self.id,
            "tareas": self.tareas,
        }

   