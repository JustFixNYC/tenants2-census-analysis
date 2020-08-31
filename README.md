## Quick start

### Install dependencies

```
python3 -m venv venv
source venv/bin/activate   # Or `venv/Scripts/activate` on Windows
pip install -r requirements.txt
```

### Setup environment variables

```
cp .env.sample .env
```

Now edit `.env` as needed.

### Download Census data

Run `python download_census_data.py`.

### Download PLUTO data

You will need to manually download [PLUTO][] and extract its main CSV to
`data/pluto.csv`.

Then run `python load_pluto.py`.

### Download user statistics

You will need to manually download user statistics in JSON format
from the tenants2 platform. The dataset is called
"User statistics with BBLs" and can be downloaded from the admin
interface under the "Download data" tab.

Copy the file to `data/userstats-with-bbls.json`.

Then run `python load_userstats.py`.

### Run analysis

To run the analysis, do:

```
sqlite3 data/db.sqlite3 < user_census_stats.sql
```

[PLUTO]: https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page
