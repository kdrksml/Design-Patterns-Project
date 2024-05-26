# web_notification_service.py
from flask import Flask, render_template, jsonify, send_file
from threading import Thread
from parking_spot_observer import ParkingSpotObserver
import os
import json

app = Flask(__name__)
parking_status = {}

class WebNotificationService(ParkingSpotObserver):
    def update(self, statuses):
        global parking_status
        parking_status = statuses
        with open('static/status.json', 'w') as f:
            json.dump(statuses, f)
    
    def send_notification(self):
        # Flask app runs in a separate thread
        thread = Thread(target=lambda: app.run(debug=True, use_reloader=False))
        thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    if os.path.exists('static/status.json'):
        with open('static/status.json', 'r') as f:
            return jsonify(json.load(f))
    return jsonify(parking_status)

if __name__ == '__main__':
    web_service = WebNotificationService()
    web_service.send_notification()
