from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class ClientDetails(db.Model):
    __tablename__ = 'ClientDetails'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    initial_contact = db.Column(db.String(100))
    point_of_contact = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Note(db.Model):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('ClientDetails.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Contract(db.Model):
    __tablename__ = 'Contracts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('ClientDetails.id'))
    contract_details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Feedback(db.Model):
    __tablename__ = 'Feedbacks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('ClientDetails.id'))
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Meeting(db.Model):
    __tablename__ = 'Meetings'
    meeting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('ClientDetails.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('EmployeeDetails.user_id'))
    scheduled_at = db.Column(db.DateTime)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class EmployeeDetails(db.Model):
    __tablename__ = 'EmployeeDetails'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    name = db.Column(db.String(100))
    role = db.Column(db.String(20))
    permissions = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
