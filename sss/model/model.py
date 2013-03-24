import datetime

from ext import db

import babel


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.UUID, unique=True, nullable=False)
    # metadata name is reserved, so using md
    md = db.relationship('SubmissionMetadata', backref='submission', uselist=False)

    def __repr__(self):
        return '<Submission %s>' % self.uuid


class SubmissionMetadata(db.Model):
    """DataCite-based metadata class. Format description is here:
    http://schema.datacite.org/meta/kernel-2.2/doc/DataCite-MetadataKernel_v2.2.pdf
    """
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))

    # mandatory
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(128))
    title = db.Column(db.String(256))
    publisher = db.Column(db.String(128))
    publication_year = db.Column(db.Date())

    # optional
    subject = db.Column(db.String(256))
    contributor = db.Column(db.String(256))
    date = db.Column(db.Date())
    language = db.Column(db.Enum(*babel.core.LOCALE_ALIASES.keys()))
    resource_type = db.Column(db.String(256))  # XXX should be extracted to a separate class
    alternate_identifier = db.Column(db.String(256))
    related_identifier = db.Column(db.String(256))
    size = db.Column(db.String(256))
    format = db.Column(db.String(256))  # file extension or MIME
    version = db.Column(db.Integer)
    rights = db.Column(db.String(256))  # not sure how to serialize rights
    description = db.Column(db.String(1024))

    # administrative metadata
    # XXX are we going to use them?
    # last_metadata_update = hook?
    # metadata_version_number = schema migration version?

    def __repr__(self):
        return '<SubmissionMetadataDataCite %s>' % self.id

    # using joined table inheritance for the 
    submission_type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'submission_metadata',
        'polymorphic_on': submission_type
    }


class LinguisticsMetadata(SubmissionMetadata):
    id = db.Column(db.Integer, db.ForeignKey('submission_metadata.id'), primary_key=True)

    phrase_popularity = db.Column(db.String(256))  # a stub field

    __mapper_args__ = {
        'polymorphic_identity': 'linguistics',
    }
