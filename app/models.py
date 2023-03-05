from . import db


class PropertyProfile(db.Model):
    __tablename__ = 'property_profiles'
    
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String(100))
    bedroom= db.Column(db.Integer)
    bathroom= db.Column(db.Integer)
    location= db.Column(db.String(255))
    price= db.Column(db.Integer)
    description= db.Column(db.String(400))
    type= db.Column(db.String(10))
    photo= db.Column(db.String(400))
    
    def __init__(self, title, bedroom, bathroom, location, price, description, type, photo):
        self.title = title
        self.bedroom = bedroom
        self.bathroom = bathroom
        self.location = location
        self.price = price
        self.description = description
        self.type = type
        self.photo = photo