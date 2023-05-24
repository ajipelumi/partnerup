#!/usr/bin/python3
""" API design for PartnerUp. """
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os
import secrets


app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key = secret_key
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_method(exception):
    """ Tears down any resource open after request cycle. """
    storage.close()


@app.errorhandler(404)
def not_found_method(error):
    """ Returns JSON-formatted 404 status code response. """
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    host = os.environ.get("PARTNERUP_API_HOST", "0.0.0.0")
    port = int(os.environ.get("PARTNERUP_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True)
