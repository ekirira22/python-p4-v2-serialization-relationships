# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = 'zookeepers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birthday = db.Column(db.Date)

    animals = db.relationship('Animal', back_populates='zookeeper')

    # don't forget that every tuple needs at least one comma!
    serialize_rules = ('-animals.zookeeper',)

    def __repr__(self):
        return f'<Zookeper {self.name}, a {self.birthday}>'


class Enclosure(db.Model, SerializerMixin):
    __tablename__ = 'enclosures'

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean)

    animals = db.relationship('Animal', back_populates='enclosure')

    # don't forget that every tuple needs at least one comma!
    serialize_rules = ('-animals.enclosure',)

    def __repr__(self):
        return f'<Enclosure {self.environment}, a {self.open_to_visitors}>'


class Animal(db.Model, SerializerMixin):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    species = db.Column(db.String)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    enclosure = db.relationship('Enclosure', back_populates='animals')
    zookeeper = db.relationship('Zookeeper', back_populates='animals')

    # don't forget that every tuple needs at least one comma!
    serialize_rules = ('-enclosure.animals', '-zookeeper.animals')

    def __repr__(self):
        return f'<Animal {self.name}, a {self.species}>'
