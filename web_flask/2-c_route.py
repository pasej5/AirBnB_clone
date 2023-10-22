#!/usr/bin/python3
"""Flask web application: C is Fun"""
from flask import Flask
app = FLask(__name__)


@app.route('/', strict_slashes=false)
def hello_hbnb():
    """when /: display 'Hello HBNB!'"""
    return “Hello HBNB!”


@app.route('/hbnb', strict_slashes=false)
def hbnb():
    """when /hbnb: display 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=false)
def c_is_fun(text):
    """/c/<text>: display 'C ' followed text"""
    return "C " + text.replace('_', ' ')


if __name__ == "__main__":
    """Main Fuction"""
    app.run(host='0.0.0.0', port=5000)
