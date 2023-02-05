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
@app.route("/api/v1/cupcakes")
def get_cupcakes():
    """ Get all cupcakes """
    cupcakes = Cupcake.query.all()
    # serialize cupcake to valid json
    json_resp = jsonify(cupcakes=[ck.serialize_cupcake() for ck in cupcakes])
    return (json_resp, 200)

# GET /api/cupcakes/[cupcake-id]
@app.route("/api/v1/cupcakes/<int:cupcake_id>")
def get_cupcake_details(cupcake_id):
    """ Get cupcake details """
    cupcake = Cupcake.query.get(cupcake_id)
    # does cupcake exist
    if not cupcake:
        return (jsonify(message=f"cupcake id {cupcake_id} does not exist"), 404)
    # cupcake exist
    json_resp = jsonify(cupcake=cupcake.serialize_cupcake())
    return (json_resp, 200)

# POST /api/cupcakes