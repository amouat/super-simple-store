#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import uuid
import logging
import os

from flask import Flask, request, render_template, jsonify
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField


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


@app.route('/uptest', methods=['GET'])
def uptest():
    return render_template('uptest.html')


@app.route('/jqupload', methods=['GET', 'POST'])
def jqupload():
    if request.method == 'GET':

        #Probably not correct, but trying to mimic requests on working code
        return ""

    if request.method == 'POST':

        #The code correctly gets the file and saves it
        #A response is sent, but something seems to fail on the JS side
        #Note delete URLs and file URLs are given, but not implemented currently
        #AFAICT the client never used them
        #
        #You can't use the data_file.content_length method as it is 0 usually
        #Note that I've hard coded the server name, obviously you will need
        #to fix this

        data_file = request.files['files[]']
        file_name = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        data_file.save(file_name)

        import urllib
        del_url = "http://inv:5000" + request.path + "?" + urllib.urlencode(
            {"f":  os.path.split(file_name)[1]})

        print 'del_url' + del_url
        #Can also supply a thumbnail url

        return jsonify(
            files=[dict(
                name=data_file.filename,
                size=os.stat(file_name).st_size,  # content_length usually 0
                type=data_file.content_type,
                delete_url=del_url,
                delete_type="DELETE",
                url="http://inv:5000/" + file_name)])


@app.route('/upload', methods=['POST'])
def upload():
    form = OtherForm()
    print 'files' + request.form['files']
    fil = request.files['file']

    if fil:
        filename = uuid.uuid4()  # this should be returned to user in finalise
        fil.save(os.path.join(app.config['UPLOAD_FOLDER'], str(filename)))

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
