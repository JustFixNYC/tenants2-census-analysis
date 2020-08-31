from dirs import DATA_DIR
from db import db

import json


USERSTATS_PATH = DATA_DIR / 'userstats-with-bbls.json'

USERSTATS_COLUMNS = {
    'user_id': 'integer primary key',
    'bbl': 'text',
    'is_nycha_bbl': 'integer',
    'letter_mail_choice': 'text',
    'latest_hp_action_pdf_creation_date': 'text',
}


def load_userstats():
    user_stats = [
        {
            'bbl': stats['pad_bbl'],
            **stats,
        }
        for stats in json.loads(USERSTATS_PATH.read_text())
    ]

    db.drop_and_create_table('userstats', USERSTATS_COLUMNS)
    db.insert_many('userstats', list(USERSTATS_COLUMNS.keys()), user_stats)


if __name__ == '__main__':
    load_userstats()
