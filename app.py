from flask import Flask, render_template_string, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random, string, qrcode, io, base64, os, threading, webbrowser, time, requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cornnor_logistics_payment_2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cornnor_pay.db'
db = SQLAlchemy(app)
...all the code till the end...
