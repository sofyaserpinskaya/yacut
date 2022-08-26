from datetime import datetime

from flask import url_for

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('get_original_url', short=self.short, _external=True),
        )
