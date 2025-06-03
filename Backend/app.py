from flask import Flask
from flask_cors import CORS

# Initialize Flask application and enable CORS
app = Flask(__name__)
CORS(app)