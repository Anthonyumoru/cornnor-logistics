import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import paystack

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key')

paystack_secret = os.environ.get('PAYSTACK_SECRET')
paystack_public = os.environ.get('PAYSTACK_PUBLIC')

ADMIN_USER = 'cornnor'
ADMIN_PASS = 'Yelwa@2026!'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        if user == ADMIN_USER and passw == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Wrong login')
    return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
