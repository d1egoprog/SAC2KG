#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 

Longer description of this module is not made yet :).

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
"""

__author__ = "Diego Rincon-Yanez"
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__date__ = "2024/10/20"
__deprecated__ = False
__status__ = "Prototype"
__version__ = "0.3.1"

import os
import uuid
import urllib

from importlib.resources import files

from rdflib import Literal, URIRef, Namespace
from rdflib.namespace import XSD

# Ontology File location

SCHEMA_FILE = files('sac2kg.owl').joinpath('veo.schema.en.5.7.rdf')

# Namespaces definition

NAMESPACES = {
    'SSN_SYSTEMS': 'http://www.w3.org/ns/ssn/systems#',
    'SOSA': 'http://www.w3.org/ns/sosa/',
    'TIME': 'http://www.w3.org/2006/time#',
    'GEO': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'VEO': os.getenv('ONTO_BASE_URI'),
}

def build_point_uri(complement):
    return 'AAAA'

def build_place_uri(complement):
    return 'BBBB'

def build_time_uri(complement):
    return 'CCCC'


# Classes definition

def get_uri(key, value=None, nokey=False):
    namespace, slash, value_flag , uid = URI_MAPPER[key]
    uri = Namespace(NAMESPACES[namespace])
    full_uri = uri[key]
    if slash:
        if value_flag:
            complement = urllib.parse.quote(str(value))
        if type(uid) == bool:
            if uid:
                complement = uuid.uuid1()
        else:
            complement = uid(value)
        full_uri = uri[f'{key}/{complement}']

    if nokey:
        return full_uri
    return {key: full_uri}

VEO_CLASSES = ('SeismicNetwork', 'Station', 'Instrument', 
    'DataPoint', 'DataPointArray', 'DataPointMatrix', 'GroundDisplacement',
    'Event', 'Blast', 'Noise', 'LongPeriod', 'VolcanoTectonic'
    'AlertLevel', 'Location')

GEO_CLASSES = ('Point', 'Place')

TIME_CLASSES = ('Instant', 'Interval')

URI_MAPPER = {
    # KEY : (namespace, Slash, Value, UUID/Callback)
    'SeismicNetwork': ('VEO', True, True, False),
    'Station': ('VEO', True, True, False),
    'Instrument': ('VEO', True, True, False),
    'Point': ('GEO', True, False, build_point_uri),
    'DataPoint': ('VEO', True, False, True),
    'GroundDisplacement': ('VEO', True, False, True),
    'Instant': ('TIME', True, False, build_time_uri),
    'DataPointArray': ('VEO', True, False, True),
    'DataPointMatrix': ('VEO', True, False, True),
    'Interval': ('TIME', True, False, build_time_uri),
    'Event': ('VEO', True, False, True),
    'Blast': ('VEO', False, False, False),
    'Noise': ('VEO', False, False, False),
    'LongPeriod': ('VEO', False, False, False),
    'VolcanoTectonic': ('VEO', False, False, False),
    'Location': ('VEO', True, False, build_point_uri),
    'AlertLevel': ('VEO', True, True, False),
    'Place': ('GEO', True, False, build_place_uri),
}

# Literal Definitions

def get_literal(key, value, nokey=False):
    if isinstance(value, list):
        values = list()
        for i in value: values.append(Literal(i, datatype=LITERAL_MAPPER[key]))
        literal = values
    else:
        literal = Literal(value, datatype=LITERAL_MAPPER[key])
    if nokey:
        return literal
    return {key: literal}

VEO_LITERALS = ('delta','axis','signalType','unit','positivePolarity',
    'dataPoints', 'component', 'amplitude',
    'focalMechanism', 'energy', 'magnitude',
    'hasLevel')

TIME_SSN_LITERALS = ('dateTimeStamp', 'systemLifetime')

GEO_LITERALS = ('lat', 'long', 'ele', 'slat', 'slong', 'sele')

LITERAL_MAPPER = {
    'delta': XSD.float,
    'axis': XSD.int,
    'signalType': XSD.string,
    'unit': XSD.string,
    'positivePolarity': XSD.boolean,
    'lat': XSD.float,
    'long': XSD.float,
    'ele': XSD.float,
    'systemLifetime': XSD.dateTime,
    'dataPoints': XSD.integer,
    'component': XSD.string,
    'amplitude': XSD.float,
    'energy': XSD.float,
    'magnitude': XSD.float,
    'focalMechanism': XSD.string,
    'slat': XSD.float,
    'slong': XSD.float,
    'sele': XSD.float,
    'hasLevel': XSD.int,
}

CLASSES = GEO_CLASSES.__add__(GEO_CLASSES).__add__(TIME_CLASSES)
LITERALS = VEO_LITERALS.__add__(GEO_LITERALS).__add__(TIME_SSN_LITERALS)

# Fields related to the Context Model
CONTEXT = ('network','station','instrument','delta','axis',
        'signalType','unit','polarity','latitude','longitud',
        'elevation')

# Fields related to the Collection Model
COLLECTION = ('lifeTime','numberOfPoints','component','data')

# Fields related to the Knowledge Model
KNOWLEDGE = ('event','energy','magnitude','focalMechanism',
            'sourceLatitude','sourceLongitud','sourceElevation', 
            'alertLevel',)
