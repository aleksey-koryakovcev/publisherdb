import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql+psycopg2://postgres:********@localhost:5432/publisherdb'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as file:
    tests_data = json.load(file)

for i in tests_data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[i.get('model')]
    session.add(model(id=i.get('pk'), **i.get('fields')))
session.commit()
