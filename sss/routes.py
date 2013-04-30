#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import uuid
import os
import urllib2
import datetime

from sss import app
from flask import (request, render_template, jsonify, flash,
                   send_from_directory, url_for)
from werkzeug import secure_filename
from flask.ext.wtf import Form, TextField
from flask.ext.wtf.html5 import EmailField
from wtforms.ext.sqlalchemy.orm import model_form
from sss import db
from model.model import Submission, SubmissionMetadata


class OtherForm(Form):
    """To be replaced with code to automatically generate form based on
    model."""
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


@app.route('/addtestdata')
def addtestdata():
    """For testing purposes only; creates a test DB entry. Should really be
    a POST or PUT operation."""
    sub = Submission(content='amtest')
    meta = SubmissionMetadata("Creator", "title", "pub",
                              datetime.date(2012, 2, 10))

    sub.md = meta
    db.session.add(sub)
    db.session.commit()

    return "Added " + sub.uuid


@app.route('/gettestdata<uuidarg>')
def gettestdata(uuidarg):
    """Returns the submission with the given UUID."""

    sub = Submission.query.filter_by(uuid=uuidarg).first()
    ret = "Id: " + str(sub.id) + "<br/>"
    if sub.md is not None:
        ret += "Title: " + str(sub.md.title)

    return ret


@app.route('/listall')
def listall():
    """Lists all test data."""

    ret = ""
    for sub in db.session.query(Submission).order_by(Submission.id):
        ret += "&nbsp;&nbsp;" + str(sub.uuid) + "<br/>"

    return "Got: <br/>" + ret


@app.route('/testmeta')
def testmeta():
    """Creates a new submission form using model_form and returns it"""
    """WIP"""
    SubForm = model_form(Submission, base_class=Form, exclude=['md'])
    sub = Submission()
    meta = SubmissionMetadata()
    sub.md = meta
    base_form = SubForm(request.form, sub)
    meta_form = model_form(SubmissionMetadata, base_class=Form,
                           exclude=['submission'])

    return render_template(
        'testmeta.html',
        domain="Linguistics",
        fileret="[]",
        base_form=base_form,
        meta_form=meta_form)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/addmeta', methods=['POST'])
def addmeta():
    """Form for adding metadata."""
    form = OtherForm()

    return render_template(
        'addmeta.html',
        domain=request.form['domain'],
        fileret=request.form.get('filelist'),
        form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle file uploads. Called from code, not directly by user."""
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


@app.route('/files/<dir_id>/<filename>', methods=['GET', 'DELETE'])
def getfiles(dir_id, filename):
    """Handle getting and deleting of files."""
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
    """Completes deposit and returns UUID."""
    """Just a placeholder currently."""
    return render_template('finalise.html', tag=uuid.uuid4())


@app.route('/deposit')
def deposit():
    return render_template('deposit.html')
