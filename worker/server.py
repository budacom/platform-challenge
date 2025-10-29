#!/usr/bin/env python3
"""Bitcoin Price Monitor Worker"""
import os
import time
import threading
from datetime import datetime
from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_URL = os.getenv('API_URL')
THRESHOLD = int(os.getenv('THRESHOLD', '100000'))
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '5000')) / 1000

def log(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}', flush=True)

def check_price():
    """Check Bitcoin price and alert if above threshold"""
    try:
        response = requests.get(f'{API_URL}/price')
        response.raise_for_status()
        data = response.json()
        price = data['price']
        
        log(f'Bitcoin: ${price}')
        
        if price > THRESHOLD:
            log(f'🚨 ALERT! Price ${price} is ABOVE threshold ${THRESHOLD}')
    except Exception as error:
        log(f'ERROR: Error checking price: {error}')

def run_flask():
    """Run Flask in a separate thread"""
    PORT = int(os.getenv('PORT', '3001'))
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    log(f'Starting monitor. Threshold: ${THRESHOLD}')
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Main loop runs in the main thread
    while True:
        check_price()
        time.sleep(CHECK_INTERVAL)

