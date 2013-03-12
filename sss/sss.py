#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import uuid
import logging

from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField

from ext import db
from model import Submission

app = Flask(__name__)
app.config.from_object('config')
try:
    app.config.from_envvar('SSS_CONFIG_PATH')
except RuntimeError:
    pass

Bootstrap(app)


@app.route('/')
def home():
    return render_template('home.html')


class OtherForm(Form):
    author = TextField('Author')
    title = TextField('Title')


@app.route('/upload', methods=['POST'])
def upload():
    form = OtherForm()
    print 'files' + request.form['files']
    return render_template(
        'upload.html',
        domain=request.form['domain'],
        fileret=request.form['files'],
        form=form)


@app.route('/finalise', methods=['POST'])
def finalise():
    return render_template('finalise.html', tag=uuid.uuid4())


@app.route('/deposit')
def deposit():
    return render_template('deposit.html')


def init_app():
    db.init_app(app)
    db.app = app

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-d', '--debug', dest='debug',
                      help='Run app in debug mode', action='store_true', default=False)

    (options, args) = parser.parse_args()

    if options.debug:
        print ' * Setting debug mode'
        app.config['DEBUG'] = True
        app.logger.setLevel(logging.ERROR)

    init_app()
    app.run(host=app.config['INTERFACE'], port=app.config['PORT'])
