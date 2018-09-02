from csv import DictReader
from datetime import datetime

import click
from flask.cli import with_appcontext

from .extensions import db
from .models import (
    Visit,
    User,
)


@click.command()
@click.argument('file', type=click.File('r'))
@with_appcontext
def add_visits_from_file(file):
    
    reader = DictReader(
        file,
        fieldnames=['datetime', 'user', 'os', 'device']
    )
    
    for i, data in enumerate(reader):

        timestamp   = datetime.fromtimestamp(int(data['datetime']))
        user_id     = int(data['user'])
        os          = Visit.OsChoices(int(data['os']))
        device      = Visit.DeviceChoices(int(data['device']))

        user = User.query.get(user_id)
        if not user:
            user = User(id=user_id)

        visit = Visit(
            id=i,
            datetime=timestamp,
            user=user,
            os=os,
            device=device
        )

        db.session.add(visit)

    db.session.commit()
