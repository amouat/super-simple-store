#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import uuid
import logging
import os
import urllib2

from flask import (Flask, request, render_template, jsonify, flash,
                   send_from_directory, url_for)
from werkzeug import secure_filename
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField
from flask.ext.wtf.html5 import EmailField

app = Flask(__name__)
Bootstrap(app)

#app.config.from_object(__name__)
app.config['BOOTSTRAP_FONTAWESOME'] = True
app.config['SECRET_KEY'] = 'wtfkey'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def home():
    return render_template('home.html')


class OtherForm(Form):
    author = TextField('Author')
    title = TextField('Title')
    keywords = TextField('Keywords')
    pub = TextField('Publication')
    email = EmailField('Email')

    #using generator allows us to order output and avoid csrf field
    def basic_field_iter(self):
        for f in [self.author, self.title, self.keywords]:
            yield f

    def adv_field_iter(self):
        yield self.pub
        yield self.email


@app.route('/addmeta', methods=['POST'])
def addmeta():
    print 'here'
    form = OtherForm()

    return render_template(
        'addmeta.html',
        domain=request.form['domain'],
        fileret=request.form.get('filelist'),
        form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':

        #Possibly not correct, but trying to mimic requests on working code
        return ""

    if request.method == 'POST':

        #You can't use the data_file.content_length method as it is 0 usually
        #Note that I've hard coded the server name, obviously you will need
        #to fix this

        data_file = request.files['files[]']
        dir_id = str(uuid.uuid4())
        temp_dir_name = str(app.config['UPLOAD_FOLDER']) + "/" + dir_id
        try:
            os.makedirs(temp_dir_name)
        except OSError as ex:
            flash("Caught Server Error: " + ex.strerror)

        sec_file = secure_filename(data_file.filename)
        file_name = os.path.join(temp_dir_name, sec_file)
        data_file.save(file_name)

        #Can also supply a thumbnail url, but I don't think we need to

        return jsonify(
            files=[dict(
                name=sec_file,
                size=os.stat(file_name).st_size,  # content_length usually 0
                type=data_file.content_type,
                delete_url=url_for('getfiles', dir_id=dir_id,
                                   filename=sec_file),
                delete_type="DELETE",
                url=url_for('getfiles', dir_id=dir_id, filename=sec_file))])


#Handle getting and deleting of files
@app.route('/files/<dir_id>/<filename>', methods=['GET', 'DELETE'])
def getfiles(dir_id, filename):
    if request.method == 'GET':

        return send_from_directory(app.config['UPLOAD_FOLDER'] + "/" + dir_id,
                                   urllib2.unquote(filename))

    if request.method == 'DELETE':

        file_dir = app.config['UPLOAD_FOLDER'] + "/" + dir_id
        try:
            os.remove(file_dir + "/" + urllib2.unquote(filename))
            if not os.listdir(file_dir):
                os.rmdir(file_dir)
        except OSError as ex:
            flash("Caught Server Error: " + ex.strerror)

        return ""


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
