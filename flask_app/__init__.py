from flask import Flask

app = Flask(__name__)

app.secret_key = "llave secretaa!"  # Para el inicio de session 

app.config['UPLOAD_FOLDER'] = 'flask_app/static/images'