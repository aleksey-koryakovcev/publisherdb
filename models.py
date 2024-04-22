"""Создание моделей"""

import sqlalchemy as sq
from sqlalchemy.orm import DeclarativeBase, registry, relationship

reg = registry()

class Base(DeclarativeBase):
    """Декларативный базовый класс"""
    registry = reg

class Publisher(Base):
    """Создает модель Publisher"""
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=150), unique=True)

class Book(Base):
    """Создает модель Book"""
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=200), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publishers = relationship(Publisher, backref='book')

class Shop(Base):
    """Создает модель Shop"""
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=200), nullable=False)

class Stock(Base):
    """Создает модель Stock"""
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)

    books = relationship(Book, backref='stock')
    shops = relationship(Shop, backref='stock')

class Sale(Base):
    """Создает модель Sale"""
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    count = sq.Column(sq.Integer)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    stocks = relationship(Stock, backref='sale')

def create_tables(engine):
    """Функция, отвечающая за создание таблиц в БД"""
    Base.metadata.create_all(engine)
