from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    web = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, id, first_name, last_name, company_name, city, state, zip, email, web, age):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.city = city
        self.state = state
        self.zip = zip
        self.email = email
        self.web = web
        self.age = age
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company_name': self.company_name,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'email': self.email,
            'web': self.web,
            'age': self.age
        }