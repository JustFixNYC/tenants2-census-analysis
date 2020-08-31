import os
from us import states
import dotenv
import census

dotenv.load_dotenv()

CENSUS_API_KEY = os.environ['CENSUS_API_KEY']

# https://www.census.gov/prod/techdoc/cbp/cbp95/st-cnty.pdf
BRONX_COUNTY = '005'

c = census.Census(CENSUS_API_KEY, year=2017)

result = c.acs5st.get(
    # These column names can be found from
    # the "ACS Subject Tables Variables", or you can find the
    # dataset you want at https://data.census.gov/ and download
    # the table that contains your data; it will contain a CSV
    # with the variable names you want, among other things.
    ('NAME', 'S1901_C01_012E',),
    {
        'for': 'tract:*',
        'in': f'state:{states.NY.fips} county:{BRONX_COUNTY}',
    },
)

print(result)
