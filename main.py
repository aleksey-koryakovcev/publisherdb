"""Подключается к БД к PostgreSQL,
импортирует модели данных из models,
заполняет БД тестовыми данными"""

import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql+psycopg2://postgres:aleksey_k@localhost:5432/publisherdb'
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

def publisher_id(session):
    """Принимает id издателя"""
    enter = input('Enter the publisher id: ')
    q = session.query(Publisher).filter(Publisher.id == enter)
    for i in q.all():
        return f'Publisher id {enter} -> {i.name}'

def publisher_name(session):
    """Принимает имя издателя"""
    enter = input('Enter the name publisher: ')
    q = session.query(Publisher).filter(Publisher.name == enter)
    for i in q.all():
        return f'Name publisher {enter} -> id {i.id}'

def shop_by_publisher_name(session):
    """Принимает имя издателя и
    выводит в каком магазине была продана книга"""
    enter = input('Enter the name publisher: ')
    q = session.query(Shop).join(Stock).join(Book).join(
        Publisher).filter(Publisher.name == enter)
    for i in q.all():
        return i

session.commit()

if __name__ == '__main__':
    publisher_id(session)
    publisher_name(session)
    shop_by_publisher_name(session)
