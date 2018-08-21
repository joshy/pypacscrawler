import json
import logging
import os
from datetime import datetime

import luigi
import requests
import schedule
from flask import Flask, g, jsonify, render_template, request
from flask_assets import Bundle, Environment

from pypacscrawler.config import get_report_show_url
from pypacscrawler.query import query_accession_number
from tasks.ris_pacs_merge_upload import MergePacsRis, DailyUpConvertedMerged

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('pypacscrawler.default_config')
app.config.from_pyfile('config.cfg')
version = app.config['VERSION'] = '1.0.0'


assets = Environment(app)
js = Bundle("js/jquery-3.3.1.min.js",
            "js/jquery.noty.packaged.min.js",
            "js/script.js",
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

@app.template_filter('to_date')
def to_date(date_as_int):
    if date_as_int:
        return datetime.strptime(str(date_as_int),
                                 '%Y%m%d').strftime('%d.%m.%Y')
    else:
        return ''


@app.route('/')
def main():
    return render_template(
        'index.html', version=app.config['VERSION'])


@app.route('/search')
def search():
    accession_number = request.args.get('accession_number', '')
    day = request.args.get('day', '')
    w = luigi.worker.Worker(no_install_shutdown_handler=True)
    if accession_number:
        task = MergePacsRis({'acc': accession_number})
    elif day:
        task = MergePacsRis({'day': day})
    w.add(task)
    w.run()
    if task.complete():
        with task.output().open('r') as r:
            results = json.load(r)
            for result in results:
                result['_childDocuments_'] = sorted(
                    result['_childDocuments_'],
                    key=lambda k: int(k['SeriesNumber']))

        return render_template(
            'result.html',
            accession_number=accession_number,
            day=day,
            version=app.config['VERSION'],
            results=results)
    else:
        return render_template(
            'error.html',
            accession_number=accession_number,
            day=day,
            version=app.config['VERSION'],
            results={})


@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json(force=True)
    accession_number = data.get('acc', '')
    day = data.get('day', '')
    logging.debug('Accession number to upload is: {}'.format(accession_number))
    if not any([accession_number, day]):
        return 'no accession number or day given', 400

    w = luigi.worker.Worker(no_install_shutdown_handler=True)
    if accession_number:
        print('acc')
        task = DailyUpConvertedMerged({'acc': accession_number})
    else:
        print('day')
        task = DailyUpConvertedMerged({'day': day})
    w.add(task)
    w.run()
    headers = {'content-type': "application/json"}
    if task.complete():
        return json.dumps({'status':'ok'})
    else:
        return 'Task error', 400