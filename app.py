from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration for PostgreSQL connection
db_password = os.environ["VACIT_ROOT_PSWD"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:' + db_password + '@localhost/vacIT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
