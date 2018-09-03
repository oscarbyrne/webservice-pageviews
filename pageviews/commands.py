from csv import DictReader
from datetime import datetime

import click
from flask.cli import with_appcontext
from tqdm import tqdm

from .extensions import db
from .models import (
    Visit,
    User,
)


def count_lines_in_file(file):
    """
    From stackoverflow: https://stackoverflow.com/a/850962
    """
    lines = 0
    buf_size = 1024 * 1024
    read_f = file.read # loop optimization
    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    file.seek(0)
    return lines

@click.command()
@click.argument('file', type=click.File('r'))
@with_appcontext
def add_visits_from_file(file):
    
    reader = DictReader(
        file,
        fieldnames=['datetime', 'user', 'os', 'device']
    )
    
    enumerated = enumerate(reader)
    length = count_lines_in_file(file)

    for i, data in tqdm(enumerated, total=length):

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
