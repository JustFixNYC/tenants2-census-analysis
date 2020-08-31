import csv

from dirs import DATA_DIR
from db import db


PLUTO_CSV = DATA_DIR / "pluto.csv"

PLUTO_COLUMNS = {
    'bbl': 'text primary key',
    'borocode': 'integer',
    'tract2010': 'text',
    'ct2010': 'text',
    'cb2010': 'text',
}


def main() -> None:
    db.drop_and_create_table("pluto", PLUTO_COLUMNS)

    with db.bulk_insert('pluto', list(PLUTO_COLUMNS.keys()), batch_size=50_000) as ins:
        with open(PLUTO_CSV, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ins.add(row)


if __name__ == '__main__':
    main()
