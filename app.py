import os
from flask import Flask, request, session, redirect
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

def base_html(title, content):
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{title}</title>
        <style>
            *{{font-family:Arial,sans-serif;margin:0;padding:0;box-sizing:border-box}}
            body{{background:#f5f7fa;padding:20px}}
            .container{{max-width:600px;margin:0 auto;background:white;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,0.1);padding:30px}}
            h1{{color:#2563eb;text-align:center;margin-bottom:30px;font-size:28px}}
            .btn{{display:block;width:100%;padding:18px;margin:12px 0;background:#2563eb;color:white;text-decoration:none;border-radius:10px;text-align:center;font-size:16px;font-weight:bold;border:none;cursor:pointer}}
            .btn-green{{background:#16a34a}} .btn-red{{background:#dc2626}} .btn-orange{{background:#ea580c}}
            input{{width:100%;padding:14px;margin:8px 0;border:2px solid #e5e7eb;border-radius:8px;font-size:16px}}
            .success{{background:#dcfce7;color:#166534;padding:15px;border-radius:8px;margin:15px 0;text-align:center}}
            .card{{background:#eff6ff;padding:15px;border-radius:8px;margin:10px 0;border-left:4px solid #2563eb}}
            @media(max-width:600px){{.container{{padding:20px}}h1{{font-size:24px}}}}
        </style>
    </head>
    <body><div class="container">{content}</div></body>
    </html>
    '''

@app.route('/')
def home():
    content = '''
    <h1>Cornnor Logistics 🚚</h1>
    <p style="text-align:center;color:#6b7280;margin-bottom:30px">Fast. Reliable. Nationwide Delivery</p>
    <a href="/track" class="btn">📦 Track Parcel</a>
    <a href="/book" class="btn btn-green">✈️ Book Shipment</a>
    <a href="/admin" class="btn btn-red">🔐 Admin Login</a>
    '''
    return base_html('Cornnor Logistics', content)

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        code = request.form.get('code').upper()
        ship = Shipment.query.filter_by(tracking_code=code).first()
        if ship:
            return base_html('Track Result', f'<h1>📍 Tracking Result</h1><div class="success">Found!</div><div class="card"><b>Code:</b> {ship.tracking_code}<br><b>Status:</b> {ship.status}<br><b>From:</b> {ship.sender}<br><b>To:</b> {ship.receiver}<br><b>Date:</b> {ship.created_at.strftime("%d %b %Y")}</div><a href="/" class="btn">Home</a>')
        return base_html('Not Found', '<h1>❌ Not Found</h1><p style="text-align:center">Tracking code no dey our system</p><a href="/track" class="btn btn-orange">Try Again</a>')
    content = '<h1>📦 Track Your Parcel</h1><form method="post"><input name="code" placeholder="Enter tracking code e.g CNR12345" required><button class="btn">Track Now</button></form><br><a href="/" class="btn" style="background:#6b7280">← Back Home</a>'
    return base_html('Track Parcel', content)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        code = 'CNR' + str(random.randint(10000, 99999))
        ship = Shipment(tracking_code=code, sender=request.form.get('sender'), receiver=request.form.get('receiver'))
        db.session.add(ship)
        db.session.commit()
        return base_html('Success', f'<h1>✅ Booking Successful!</h1><div class="success"><h2>Save This Code:</h2><h1 style="font-size:32px;letter-spacing:3px">{code}</h1></div><div class="card"><b>From:</b> {ship.sender}<br><b>To:</b> {ship.receiver}<br><b>Status:</b> Processing</div><p style="text-align:center;color:#6b7280">Screenshot this page!</p><a href="/" class="btn">Done</a>')
    content = '<h1>✈️ Book Shipment</h1><form method="post"><label>Sender Name:</label><input name="sender" required><label>Receiver Name:</label><input name="receiver" required><button class="btn btn-green">Book & Get Tracking Code</button></form><br><a href="/" class="btn" style="background:#6b7280">← Back Home</a>'
    return base_html('Book Shipment', content)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['logged_in'] = True
            return redirect('/dashboard')
        return base_html('Login', '<h1>🔐 Admin Login</h1><p style="color:red;text-align:center">Wrong password!</p><form method="post"><input name="username" placeholder="Username" required><input name="password" type="password" placeholder="Password" required><button class="btn btn-red">Login</button></form>')
    content = '<h1>🔐 Admin Login</h1><form method="post"><input name="username" placeholder="Username" required><input name="password" type="password" placeholder="Password" required><button class="btn btn-red">Login</button></form><br><a href="/" class="btn" style="background:#6b7280">← Back Home</a>'
    return base_html('Admin Login', content)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/admin')
    ships = Shipment.query.order_by(Shipment.created_at.desc()).all()
    html = '<h1>📊 Admin Dashboard</h1><p style="color:#6b7280;margin-bottom:20px">Total Shipments: {}</p>'.format(len(ships))
    for s in ships:
        html += f'<div class="card"><b>{s.tracking_code}</b><br>{s.sender} → {s.receiver}<br><span style="color:#2563eb">{s.status}</span><br><small>{s.created_at.strftime("%d %b %Y %H:%M")}</small></div>'
    html += '<br><a href="/logout" class="btn btn-red">Logout</a>'
    return base_html('Dashboard', html)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run()
