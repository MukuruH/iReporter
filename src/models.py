"""
Data models

Author: Abraham Arishian    
"""
import json


class Incident:
    def __init__(self, id=None, createdOn=None, createdBy=None, type=None, location=None,
                 status=None, Images=[], Videos=[], comment=None):
        """ Create a new Incident. """
        self.id = id
        self.createdOn = createdOn
        self.createdBy = createdBy
        self.type = type
        self.location = location
        self.status = status
        self.Images = Images
        self.Videos = Videos
        self.comment = comment


def convert_to_dict(object):
    """ Convert a class instance to a dictionary. """
    return object.__dict__
