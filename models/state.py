#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
import Base
from model.city import City

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = column(string(128), nullable=False)
    cities = relationship("City", cascade="delete", backref="State")

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """geter atrebute"""
            list_City = []
            all_City = model.storage.all(City)
            for city in all_City.values():
                if city.id == self.id:
                    list_City.append(city)
            return list_City
