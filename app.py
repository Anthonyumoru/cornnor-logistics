import os
from flask import Flask, request, session, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cornnor.db'
db = SQLAlchemy(app)

ADMIN_USER = os.environ.get('ADMIN_USER', 'cornnor')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'Yelwa@2026!')

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_code = db.Column(db.String(20), unique=True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Processing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

HOME_HTML = '''
<h1 style="text-align:center;color:#2563eb">Cornnor Logistics 🚚</h1>
<div style="text-align:center;margin-top:50px">
    <a href="/track" style="padding:15px 30px;background:#2563eb;color:white;text-decoration:none;border-radius:8px;margin:10px">Track Parcel</a>
    <a href="/book" style="padding:15px 30px;background:#16a34a;color:white;text-decoration:none;border-radius:8px;margin:10px">Book Shipment</a>
    <a href="/admin" style="padding:15px 30px;background:#dc2626;color:white;text-decoration:none;border-radius:8px;margin:10px">Admin Login</a>
</div>
'''

@app.route('/')
def home():
    return HOME_HTML

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        code = request.form.get('code')
        ship = Shipment.query.filter_by(tracking_code=code).first()
        if ship:
            return f'<h2>Tracking: {code}</h2><p>Status: <b>{ship.status}</b><br>From: {ship.sender}<br>To: {ship.receiver}</p><a href="/">Home</a>'
        return 'Tracking code not found <a href="/track">Try again</a>'
    return '<h2>Track Your Parcel</h2><form method="post"><input name="code" placeholder="Enter tracking code"><br><br><button>Track</button></form><br><a href="/">Home</a>'

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        code = 'CNR' + str(random.randint(10000, 99999))
        ship = Shipment(tracking_code=code, sender=request.form.get('sender'), receiver=request.form.get('receiver'))
        db.session.add(ship)
        db.session.commit()
        return f'<h2>Booking Successful! ✅</h2><p>Your tracking code: <b>{code}</b><br>Save am well!</p><a href="/">Home</a>'
    return '<h2>Book Shipment</h2><form method="post">Sender: <input name="sender" required><br><br>Receiver: <input name="receiver" required><br><br><button>Book Now</button></form><br><a href="/">Home</a>'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['logged_in'] = True
            return redirect('/dashboard')
        return 'Wrong password <a href="/admin">Try again</a>'
    return '<h2>Admin Login</h2><form method="post"><input name="username" placeholder="Username"><br><br><input name="password" type="password" placeholder="Password"><br><br><button>Login</button></form>'

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/admin')
    ships = Shipment.query.all()
    html = '<h1>Dashboard</h1><h3>All Shipments:</h3>'
    for s in ships:
        html += f'<p>{s.tracking_code} - {s.sender} → {s.receiver} - Status: {s.status}</p>'
    html += '<br><a href="/logout">Logout</a>'
    return html

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run()
