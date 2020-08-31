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

 and run `python download_census_data.py`.

### Download PLUTO data

You will need to manually download [PLUTO][] and extract its main CSV to
`data/pluto.csv`.

[PLUTO]: https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page
