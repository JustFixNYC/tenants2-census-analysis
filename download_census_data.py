import os
from us import states
import dotenv
import census

dotenv.load_dotenv()

CENSUS_API_KEY = os.environ['CENSUS_API_KEY']

# https://www.census.gov/prod/techdoc/cbp/cbp95/st-cnty.pdf
BRONX_COUNTY = '005'
KINGS_COUNTY = '047'
NEW_YORK_COUNTY = '061'
RICHMOND_COUNTY = '085'
QUEENS_COUNTY = '081'

# These column names can be found from
# the "ACS Subject Tables Variables", or you can find the
# dataset you want at https://data.census.gov/ and download
# the table that contains your data; it will contain a CSV
# with the variable names you want, among other things.
HOUSEHOLDS_MEDIAN_INCOME_DOLLARS = 'S1901_C01_012E'

c = census.Census(CENSUS_API_KEY, year=2018)

result = c.acs5st.get(
    ('NAME', HOUSEHOLDS_MEDIAN_INCOME_DOLLARS,),
    {
        'for': 'tract:*',
        'in': f'state:{states.NY.fips} county:{BRONX_COUNTY}',
    },
)

for item in result:
    # For some reason some of these are -666,666,666, which must
    # signify something important. We'll just ignore them for now.
    hmid = int(item[HOUSEHOLDS_MEDIAN_INCOME_DOLLARS])
    name = item['NAME']
    if hmid > 0:
        print(f"${hmid:<8,} {name}")
