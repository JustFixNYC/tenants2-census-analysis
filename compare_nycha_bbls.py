from typing import List, Optional, Dict, Any
from pathlib import Path
import json

from db import db

# SQL for 'ownername' fields matching NYCHA in PLUTO.
NYCHA_OWNERNAMES = "('NYC HOUSING AUTHORITY', 'NYCHA')"

SCRAPED_NYCHA_JSON = json.loads(Path('nycha_bbls.json').read_text())

for _item in SCRAPED_NYCHA_JSON:
    _item['bbl'] = str(_item['bbl'])
del _item


def get_bbls_from_pluto() -> List[str]:
    with db.cursor() as cur:
        cur.execute(f"SELECT bbl FROM pluto WHERE ownername IN {NYCHA_OWNERNAMES}")
        return [row['bbl'] for row in cur.fetchall()]


def fetchone(query: str) -> Optional[Dict[str, Any]]:
    with db.cursor() as cur:
        cur.execute(query)
        return cur.fetchone()


def main():
    pluto_bbls = get_bbls_from_pluto()
    pluto_bbls_set = set(pluto_bbls)
    scraped_bbls_set = set(item['bbl'] for item in SCRAPED_NYCHA_JSON)

    not_in_scrape_set = pluto_bbls_set.difference(scraped_bbls_set)
    print("NYCHA BBLs in PLUTO that aren't in our scrape:\n")
    for bbl in not_in_scrape_set:
        bldgclass = fetchone(f"SELECT bldgclass FROM pluto WHERE bbl = '{bbl}'")['bldgclass']
        print(f"{bbl} - BldgClass: {bldgclass} - https://whoownswhat.justfix.nyc/bbl/{bbl}")
    print(f"\nTotal: {len(not_in_scrape_set)}\n")

    print("BBLs in our scrape that aren't owned by NYCHA in PLUTO:\n")
    count = 0
    for item in SCRAPED_NYCHA_JSON:
        bbl = item['bbl']
        if bbl not in pluto_bbls_set:
            count += 1
            with db.cursor() as cur:
                cur.execute(f"SELECT ownername FROM pluto WHERE bbl = '{bbl}'")
                row = cur.fetchone()
                if row:
                    owner = f"OwnerName: {row['ownername']}"
                else:
                    owner = "BBL is not in PLUTO"
            print(f"{bbl} - {item['development']} - {owner}")
    print(f"\nTotal: {count}")


if __name__ == '__main__':
    main()
