"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI="postgresql:///cupcake",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # SQLALCHEMY_ECHO=True,
    SECRET_KEY="xxsecretxxkeyxxyesxx",
    DEBUG_TB_INTERCEPT_REDIRECTS=False
)

# connect db
connect_db(app)
# debug
debug = DebugToolbarExtension(app)

# GET /api/cupcakes
@app.route("/api/cupcakes")
def get_cupcakes():
    """ Get all cupcakes """
    cupcakes = Cupcake.query.all()
    # serialize cupcake and send
    json_resp = jsonify(cupcakes=[ck.serialize_cupcake() for ck in cupcakes])
    return (json_resp, 200)

# GET /api/cupcakes/[cupcake-id]
@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_details(cupcake_id):
    """ Get cupcake details """
    cupcake = Cupcake.query.get(cupcake_id)
    # does cupcake exist
    if not cupcake:
        return (jsonify(message=f"cupcake id {cupcake_id} does not exist"), 404)
    # cupcake exist => serialize and send
    json_resp = jsonify(cupcake=cupcake.serialize_cupcake())
    return (json_resp, 200)

# POST /api/cupcakes
@app.route("/api/cupcake", methods=["POST"])
def create_cupcake():
    """ Create cupcake """
    req_cupcake = {
        "flavor": request.json['flavor'],
        "size": request.json['size'],
        "rating": float(request.json['rating']),
        "image": request.json['image']
    }
    # create cupcake
    cupcake = Cupcake(**req_cupcake)
    # add to database
    db.session.add(cupcake)
    db.session.commit()
    # serialize cupcake
    serialized_cupcake = cupcake.serialize_cupcake()
    return (jsonify(cupcake=serialized_cupcake), 200)