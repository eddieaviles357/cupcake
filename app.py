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

@app.route('/api/v1/cupcakes')
def get_cupcakes():
    """ Get all cupcakes """
    cupcakes = Cupcake.query.all_or_404()
    cupcakes = {k: v for k,v in cupcakes}
    json_resp = jsonify(cupcakes=cupcakes)
    return (json_resp, 200)