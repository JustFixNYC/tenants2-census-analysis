import os
from db import Database
from typing import Optional, List, Dict, Any
from us import states
import dotenv
import census

dotenv.load_dotenv()

CENSUS_API_KEY = os.environ['CENSUS_API_KEY']

# These are FIPS codes for NYC's counties. Taken from:
# https://www.census.gov/prod/techdoc/cbp/cbp95/st-cnty.pdf
BRONX_COUNTY = '005'
KINGS_COUNTY = '047'
NEW_YORK_COUNTY = '061'
RICHMOND_COUNTY = '085'
QUEENS_COUNTY = '081'

COUNTY_TO_BORO_CODE = {
    NEW_YORK_COUNTY: 1,
    BRONX_COUNTY: 2,
    KINGS_COUNTY: 3,
    QUEENS_COUNTY: 4,
    RICHMOND_COUNTY: 5,
}

COUNTY_NAMES = {
    NEW_YORK_COUNTY: "New York",
    BRONX_COUNTY: "Bronx",
    KINGS_COUNTY: "Kings",
    QUEENS_COUNTY: "Queens",
    RICHMOND_COUNTY: "Richmond",
}

ALL_COUNTIES = list(COUNTY_TO_BORO_CODE.keys())

# These column names can be found from
# the "ACS Subject Tables Variables", or you can find the
# dataset you want at https://data.census.gov/ and download
# the table that contains your data; it will contain a CSV
# with the variable names you want, among other things.
HOUSEHOLDS_MEDIAN_INCOME_DOLLARS = 'S1901_C01_012E'

CENSUS_COLUMNS = {
    'borocode': 'integer',
    'tract2010': 'text',
    'households_median_income_dollars': 'integer',
}


def get_county_tract_data(fips_county_code: str) -> List[Dict[str, Any]]:
    '''
    Return Census data for all the tracts in a county, transformed
    so as to be ready for insertion into our database.
    '''

    c = census.Census(CENSUS_API_KEY, year=2018)

    rows: List[Dict[str, Any]] = []

    census_rows = c.acs5st.get(
        ('NAME', HOUSEHOLDS_MEDIAN_INCOME_DOLLARS,),
        {
            'for': 'tract:*',
            'in': f'state:{states.NY.fips} county:{fips_county_code}',
        },
    )

    for row in census_rows:
        hmid = int(row[HOUSEHOLDS_MEDIAN_INCOME_DOLLARS])
        rows.append({
            'borocode': COUNTY_TO_BORO_CODE[row['county']],
            'tract2010': row['tract'],
            # https://github.com/datamade/census/issues/72
            'households_median_income_dollars': None if hmid <= 0 else hmid,
        })

    return rows


def download_census_data_into_db():
    from db import db

    db.drop_and_create_table("census", CENSUS_COLUMNS)

    for county in ALL_COUNTIES:
        county_name = COUNTY_NAMES[county]
        print(f"Downloading data for {county_name} county.")
        rows = get_county_tract_data(county)
        db.insert_many('census', list(CENSUS_COLUMNS.keys()), rows)


if __name__ == '__main__':
    download_census_data_into_db()
