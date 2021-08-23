"""
Name:       keep_alive.py
Purpose:    keep MCU Quote Bot alive

Authors:    Lin.I

Created:    05/13/2021
"""

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    app.run(host='0.0.0.0', port=8000)


def keep_alive():
    t = Thread(target=run)
    t.start()
