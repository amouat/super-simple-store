# all the imports
from __future__ import with_statement
from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, TextField
import uuid

# create our little application :)
app = Flask(__name__)
Bootstrap(app)

app.config.from_object(__name__)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
