from shop import db, app

from datetime import datetime



""" 
    - Table for Addproduct in the database 
    - Having many-one Relationship with Brand and Category Table 
"""
class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brand', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('category', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default="image.jpg")
    image_3 = db.Column(db.String(150), nullable=False, default="image.jpg")


    def __repr__(self):
        return '<Addproduct %r>' % self.name


""" 
    - Table for Brand in the database 
    - Having one-many Relationship with Addproduct 
"""
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


""" 
    - Table for Category in the database 
    - Having one-many Relationship with Addproduct 
"""
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30), nullable=False, unique=True)

with app.app_context():   # all database operations under with
    db.create_all() 