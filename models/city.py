#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
     __tablename__ = 'cities'
    name = column(string(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
