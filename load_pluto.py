import csv

from dirs import DATA_DIR
from db import db


PLUTO_CSV = DATA_DIR / "pluto.csv"

PLUTO_COLUMNS = {
    'bbl': 'text primary key',
    'borocode': 'integer',
    'tract2010': 'text',
    'cb2010': 'text',
}


def main() -> None:
    db.drop_and_create_table("pluto", PLUTO_COLUMNS)

    with db.bulk_insert('pluto', list(PLUTO_COLUMNS.keys()), batch_size=50_000) as ins:
        with open(PLUTO_CSV, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # For some reason, PLUTO adds a '.00000000' to the end of BBLs.
                row['bbl'] = row['bbl'][:10]
                row['borocode'] = int(row['borocode'], base=10)  # type: ignore
                # PLUTO leaves out the suffix if there is none, whereas the Census API
                # always sets the suffix to 00 in this case, so we'll do it too, which
                # will make joins easier.
                row['tract2010'] = f"{row['tract2010']:0<6}"
                ins.add(row)


if __name__ == '__main__':
    main()
