#!/usr/bin/env python
from sss import db, app

if __name__ == '__main__':
    db.app = app
    db.init_app(app)
    # creates an empty (without data) database with schema
    db.create_all()

    # now we can create any initial data that we may need for the application to run for the first time
