from pathlib import Path


MY_DIR = Path(__file__).parent.resolve()

DATA_DIR = MY_DIR / 'data'

DATA_DIR.mkdir(exist_ok=True)

SQL_DIR = MY_DIR / 'sql'
