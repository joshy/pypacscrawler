import logging
import os
import schedule
import datetime

from flask import Flask, g, jsonify, render_template, request
from flask_assets import Bundle, Environment

from pypacscrawler.query import query_day

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('pypacscrawler.default_config')
app.config.from_pyfile('config.cfg')
version = app.config['VERSION'] = '1.0.0'


@app.route('/')
def main():
    print('asdfasf')
    day = query_date = datetime.datetime.strptime('2010-01-01', '%Y-%m-%d')
    result = query_day(app, 'CT', day, '10000-135959')
    return render_template('index.html',
        version=app.config['VERSION'],
        result=result)
