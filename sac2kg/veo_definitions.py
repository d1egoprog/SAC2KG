#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

This module defines the structure and utilities for working with the VEO (Volcanic Event Ontology) 
and related ontologies. It provides functionality for generating URIs and literals for various 
classes and properties, as well as defining namespaces, ontology file locations, and mappings 
for semantic data representation.

Key Features:
- Namespace definitions for VEO, GEO, TIME, SOSA, and SSN_SYSTEMS.
- URI generation for ontology classes and properties using `get_uri`.
- Literal generation for ontology properties using `get_literal`.
- Mappings for classes and literals to their respective namespaces and datatypes.
- Context, Collection, and Knowledge model field definitions for semantic data organization.

Constants:
- `BUILD_DATE`, `AUTHOR_NAME`, `COMPONENT_VERSION`: Metadata loaded from environment variables.
- `NAMESPACES`: Dictionary defining ontology namespaces.
- `SCHEMA_FILE`: Path to the ontology schema file.
- `URI_MAPPER`: Mapping of ontology classes to their namespace, URI structure, and generation logic.
- `LITERAL_MAPPER`: Mapping of ontology literals to their respective XSD datatypes.
- `CLASSES`, `LITERALS`: Aggregated tuples of ontology classes and literals.
- `CONTEXT`, `COLLECTION`, `KNOWLEDGE`: Field definitions for different semantic models.

Functions:
- `build_point_uri(complement)`: Placeholder function for generating URIs for GEO points.
- `build_place_uri(complement)`: Placeholder function for generating URIs for GEO places.
- `build_time_uri(complement)`: Placeholder function for generating URIs for TIME instances.
- `get_uri(key, value=None, nokey=False)`: Generates a URI for a given ontology class or property.
- `get_literal(key, value, nokey=False)`: Generates a literal for a given ontology property.

This module is intended for use in semantic data modeling and ontology-based applications, 
particularly in the context of volcanic event data representation.
"""

import os
from dotenv import load_dotenv
load_dotenv()

BUILD_DATE = os.getenv('BUILD_DATE')
AUTHOR_NAME = os.getenv('AUTHOR_NAME')
COMPONENT_VERSION = os.getenv('COMPONENT_VERSION')

__author__ = AUTHOR_NAME
__date__ = BUILD_DATE
__version__ = COMPONENT_VERSION
__copyright__ = "Copyright 2024, Diego Rincon-Yanez"
__status__ = "Prototype"
__deprecated__ = False

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
    'Blank': ('VEO', False, False, False),
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
