# view snapshot of results from results table

import sqlite3
from pprint import pprint
from tqdm import tqdm

db_name = "3.db"
books_table = "books"
results_table = "libgen_results"

conn = sqlite3.connect(db_name)
c = conn.cursor()

c.execute(f"SELECT * FROM {results_table} LIMIT 2")

pprint(c.fetchall())