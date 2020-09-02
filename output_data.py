from typing import Dict, List, Any
import json

from db import db
from dirs import SQL_DIR, DATA_DIR


OUTPUT_DATA_SQL_FILE = SQL_DIR / "output_data.sql"

OUTPUT_DATA_JS_FILE = DATA_DIR / "data.js"

IGNORE_COLUMNS = {"bbl", "cb2010"}


def output_data() -> None:
    with db.cursor() as cur:
        cur.execute(OUTPUT_DATA_SQL_FILE.read_text())
        rows = cur.fetchall()
        assert len(rows) > 0, "At least one row must be returned"
        columns = [
            column for column in rows[0].keys()
            if column not in IGNORE_COLUMNS
        ]
        data: List[Dict[str, Any]] = []
        for row in rows:
            data.append({
                column: row[column] for column in columns
            })
        data_json = json.dumps(data, indent=2)
        OUTPUT_DATA_JS_FILE.write_text(f"var data = {data_json};\n")
    print(f"Wrote {OUTPUT_DATA_JS_FILE}.")


if __name__ == '__main__':
    output_data()
