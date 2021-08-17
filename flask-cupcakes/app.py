"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake, serialize

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes' #database cupcakes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route("/")
def index():
    """Render homepage."""
    return render_template("index.html")

@app.route ("api/cupcakes")
def list_cupcakes():
    """get data for all cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()] #serialize for JSON
#Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>']
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""
    cupcake_data = Cupcake.query.get_or_404(cupcake_id) #This should raise a 404 if the cupcake cannot be found.
    cupcake = cupcake_data.serialize()  #serialize for JSON
    return jsonify(cupcake=cupcake) #Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request."""
    #Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    data = request.json
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()), 201) # POST requests should return HTTP status of 201 CREATED

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id): #pass in ID to "patch" the correct cupcake
    """Update cupcake from data in request. Return updated data."""
    #Returns JSON like: {cupcake: [{id, flavor, rating, size, image}]}
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor'] #Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request.
    cupcake.rating = data['rating'] # You can always assume that the entire cupcake object will be passed to the backend.
    cupcake.size = data['size'] #can put default values if not entire object. 
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize()) #serialize for JSON with serialize()


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id): #id passed to URL
    """Delete cupcake and return confirmation message."""
    #Returns JSON of {message: "Deleted"}
    cupcake = Cupcake.query.get_or_404(cupcake_id) #This should raise a 404 if the cupcake cannot be found

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted") #Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}