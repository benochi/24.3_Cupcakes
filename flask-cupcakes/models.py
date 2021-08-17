"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy
DEFAULT_IMG = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Cupcake class"""
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #flavor: a not-nullable text column
    flavor = db.Column(db.Text, nullable=False)
    #size: a not-nullable text column
    size = db.Column(db.Text, nullable=False)
    #rating: a not-nullable column that is a float
    rating = db.Column(db.Float, nullable=False)
    #image:
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMG) 

def serialize(self):
        """Serialize cupcake to a dict for JSON output."""
        return { #id, flavor, size, rating, image
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image,
        }

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)