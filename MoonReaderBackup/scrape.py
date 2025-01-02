from libgen_api import LibgenSearch
import sqlite3
from pprint import pprint
from tqdm import tqdm

db_name = "3.db"
books_table = "books"
results_table = "libgen_results"



conn = sqlite3.connect(db_name)
c = conn.cursor()


# create libgen_resukts
# CREATE TABLE libgen_results (
#     ID INTEGER PRIMARY KEY,
#     Author TEXT,
#     Title TEXT,
#     Publisher TEXT,
#     Year INTEGER,
#     Language TEXT,
#     Pages INTEGER,
#     Size TEXT,
#     Extension TEXT,
#     Mirror_1 TEXT,
#     Mirror_2 TEXT,
#     Mirror_3 TEXT,
#     book_id INTEGER,  -- Foreign key column to reference 'books' table
#     FOREIGN KEY (book_id) REFERENCES books(_id)  -- Define the foreign key relationship
# );

# drop results_table
c.execute(f"DROP TABLE IF EXISTS {results_table}")

conn.execute(f"""
CREATE TABLE IF NOT EXISTS {results_table} (
    ID INTEGER,
    Author TEXT,
    Title TEXT,
    Publisher TEXT,
    Year INTEGER,
    Language TEXT,
    Pages INTEGER,
    Size TEXT,
    Extension TEXT,
    Mirror_1 TEXT,
    Mirror_2 TEXT,
    Mirror_3 TEXT,
    book_id INTEGER,  
    FOREIGN KEY (book_id) REFERENCES {books_table}(_id)
);
""")

search = LibgenSearch()

# # describe table and pprint the restults
# c.execute(f"PRAGMA table_info({results_table})")
# pprint(c.fetchall())

# fetching data from libgen

data = c.execute(f"SELECT * FROM {books_table}").fetchall()

results = []
for row in tqdm(data):
    book_title = row[1]
    res = search.search_title(book_title)
    for r in res:
        r["book_id"] = row[0]
        results.append(r)
        
# save results as json file
import json
with open("libgen_results.json", "w") as f:
    json.dump(results, f)
        
# insert results into the table
# cur.execute("""
# INSERT INTO libgen_results (ID, Author, Title, Publisher, Year, Language, Pages, Size, Extension, Mirror_1, Mirror_2, Mirror_3)
# VALUES (
#     :ID, 
#     :Author, 
#     :Title, 
#     :Publisher, 
#     :Year, 
#     :Language, 
#     :Pages, 
#     :Size, 
#     :Extension, 
#     :Mirror_1, 
#     :Mirror_2, 
#     :Mirror_3
# )
# """, data) 

print("Inserting data into the table...")

for result in tqdm(results):
    c.execute(f"""
    INSERT INTO {results_table} (ID, Author, Title, Publisher, Year, Language, Pages, Size, Extension, Mirror_1, Mirror_2, Mirror_3, book_id)
    VALUES (
        :ID, 
        :Author, 
        :Title, 
        :Publisher, 
        :Year, 
        :Language, 
        :Pages, 
        :Size, 
        :Extension, 
        :Mirror_1, 
        :Mirror_2, 
        :Mirror_3,
        :book_id
    )
    """, result)
    
conn.commit()


