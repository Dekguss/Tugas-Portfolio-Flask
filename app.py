import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

messages_collection = db.messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/say_hi')
def say_hi():
    return jsonify({'msg': 'Welcome To My Portfolio Website'})

@app.route('/save_message', methods=['POST'])
def save_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        message_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }

        messages_collection.insert_one(message_data)

        return jsonify({'msg': 'Pesan Anda telah disimpan!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)