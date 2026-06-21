import os
from flask import Flask, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev123')

ADMIN_USER = os.environ.get('ADMIN_USER', 'cornnor')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'Yelwa@2026!')

@app.route('/')
def home():
    return '<h1>Cornnor Logistics is LIVE ✅</h1><p><a href="/admin">Admin Login</a></p>'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['logged_in'] = True
            return redirect('/dashboard')
        return 'Wrong password <a href="/admin">Try again</a>'
    return '''
    <form method="post">
        <h2>Admin Login</h2>
        <input name="username" placeholder="Username"><br><br>
        <input name="password" type="password" placeholder="Password"><br><br>
        <button>Login</button>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/admin')
    return '<h1>Dashboard</h1><p>Welcome Cornnor! Site dey work ✅</p>'

if __name__ == '__main__':
    app.run()
