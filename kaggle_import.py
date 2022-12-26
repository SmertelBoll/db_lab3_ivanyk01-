import psycopg2
import csv

username = ''
password = ''
database = ''

INPUT_CSV_FILE = 'Global Power Plant.csv'

query_0 = """
DELETE FROM powerplants;
DELETE FROM fuels;
DELETE FROM owners;
"""

query_1 = """
INSERT INTO fuels(fuel_name) VALUES (%s)
"""

query_2 = """
INSERT INTO owners(owner_name) VALUES (%s)
"""

query_main = """
INSERT INTO powerplants(id,	name, country, capacity, latitude, longtitude, owner, fuel_type)
VALUES
(%s, %s, %s, %s, %s, %s, (SELECT owner_id FROM owners WHERE owner_name = %s), (SELECT fuel_id FROM fuels WHERE fuel_name = %s));
"""

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_0)
    with open(INPUT_CSV_FILE, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf)
        next(reader)
        owners = []
        fuels = []

        for row in reader:
            owners.append(row[7])
            fuels.append(row[6])

        for fuel in list(set(fuels)):
            cur.execute(query_1, tuple([fuel]))
        for owner in list(set(owners)):
            cur.execute(query_2, tuple([owner]))

    conn.commit()

    with open(INPUT_CSV_FILE, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf)
        next(reader)
        for row in reader:
            cur.execute(query_main, (row[2], row[1], row[0], float(row[3]), float(row[4]), float(row[5]), row[7], row[6]))

    conn.commit()