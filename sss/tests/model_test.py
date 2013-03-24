from flask import Flask
from flask.ext.testing import TestCase
from uuid import uuid4

from model import Submission
from ext import db


class ModelTest(TestCase):
    db_uri = "sqlite:///:memory:"

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        db.app = app
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        db.drop_all()

    def testSubmissionCreateAndQuery(self):
        uuids = uuid4()
        dir(Submission)
        submission = Submission(uuids, 'my content')
        db.session.add(submission)
        db.session.flush()
        s = db.session.query(Submission).filter_by(ext_id=uuids).first()
        self.assertEquals(s, submission)
