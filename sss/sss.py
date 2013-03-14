#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import uuid
import logging

from flask import Flask, request, render_template, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField
from flaskext.uploads import UploadSet, ALL, configure_uploads

app = Flask(__name__)
Bootstrap(app)

#app.config.from_object(__name__)
app.config['BOOTSTRAP_FONTAWESOME'] = True
app.config['SECRET_KEY'] = 'wtfkey'


#I think the idea is you can serve multiple apps from one config
def upload_dir(app):
    return "uploads"

fileset = UploadSet('files', ALL, upload_dir)
configure_uploads(app, fileset)


@app.route('/')
def home():
    return render_template('home.html')


class OtherForm(Form):
    author = TextField('Author')
    title = TextField('Title')


@app.route('/file_upload', methods=['POST'])
def file_upload():
    filename = fileset.save(request.files['files'])
    flash("saved?")
    return render_template('deposit.html')


@app.route('/finalise', methods=['POST'])
def finalise():
    return render_template('finalise.html', tag=uuid.uuid4())


@app.route('/deposit')
def deposit():
    return render_template('deposit.html')


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

    app.run(host='0.0.0.0')
