import os

from numpy import random

from rdflib import Literal, Namespace, URIRef
from rdflib.namespace import XSD

VEO_URI = os.getenv('ONTO_BASE_URI')
GEO_URI = 'http://www.w3.org/2003/01/geo/wgs84_pos#'

@staticmethod
def getNetworkURI(data):
    return 'Test'

data_model = {
    'Network': 'file.knetwk', #get('knetwk,  # Network Code
    'Station': 'file.kstnm',  # Station Name
    'Instrument': 'file.kinst',  # Instrument Name
    'delta': 'file.delta', #file.delta,  # Sampling Interval (s)
    'axis': 'file.cmpaz',  # Component Azimuth (degrees)
    'signalType': 'file.iftype',  # Signal Type
    'unit': 'file.kuser0',  # Unit of Measurement
    'polarity': 'file.lpspol',  # Polarity
    'latitude': 'file.stla',  # Station Latitude (degrees)
    'longitude': 'file.stlo',  # Station Longitude (degrees)
    'elevation': 'file.stel',  # Station Elevation (meters)
    'lifeTime': 'file.nvhdr',  # Header Version Number (for lifetime estimation)
    'numberOfPoints': 'file.npts',  # Number of Data Points
    'component': 'file.kcmpnm',  # Component Name (e.g., N, E, Z)
    'data': 'file.data',  # Placeholder for waveform data
    'event': 'file.kevnm',  # Event Name
    'energy': 'file.user0',  # Estimated Energy
    'magnitude': 'file.user1',  # Magnitude
    'focalMechanism': 'file.kuser1',  # Focal Mechanism Description
    'sourceLatitude': 'file.evla',  # Event Latitude (degrees)
    'sourceLongitud': 'file.evlo',  # Event Longitude (degrees)
    'sourceElevation': 'file.leven',  # Event Elevation (meters)
    'alertLevel': 'file.ka',  # Alert Level (if applicable)
    # New Mappings
    'depth': 'file.stdp',  # Source Depth (km)
}


SEMANTIC_MODEL_CLASSES = {
    'Network': URIRef(f'{VEO_URI}SeismicNetwork/{getNetworkURI(data_model['Network'])}'),
    'Station': URIRef(f'{VEO_URI}Station/'),
    'Instrument': URIRef(f'{VEO_URI}Instrument/'),
    'Location': URIRef(f'{GEO_URI}Point/'),
    'DataPoint': URIRef(f'{VEO_URI}DataPoint/'),
    'GroundDisplacement': URIRef(f'{VEO_URI}GroundDisplacement/'),
    'DataPointArray': URIRef(f'{VEO_URI}DataPointArray/'),
    'DataPointMatrix': URIRef(f'{VEO_URI}DataPointMatrix/'),
    'Event': URIRef(f'{VEO_URI}Event/'),
    'Blast': URIRef(f'{VEO_URI}Blast/'),
    'Noise': URIRef(f'{VEO_URI}Noise/'),
    'LongPeriod': URIRef(f'{VEO_URI}LongPeriod/'),
    'VolcanoTectonic': URIRef(f'{VEO_URI}VolcanoTectonic/'),
    'AlertLevel': URIRef(f'{VEO_URI}Location/'),
    'SourceLocation': URIRef(f'{VEO_URI}Location/'),
    'Place': URIRef(f'{VEO_URI}Place/'),
}

SEMANTIC_MODEL_LITERALS = {
    'delta': Literal(0.5, datatype=XSD.float),
    'axis': Literal('3', datatype=XSD.float),
    'signalType': Literal('Analog', datatype=XSD.string),
    'unit': Literal('Displacement', datatype=XSD.string),
    'polarity': Literal(0.3, datatype=XSD.float),
    'latitude':  Literal(0.2, datatype=XSD.float),
    'longitude': Literal(0.2, datatype=XSD.float),
    'elevation': Literal(0.35, datatype=XSD.float),
    'lifeTime': Literal(0.35, datatype=XSD.dateTime),
    'numberOfPoints': Literal(3000, datatype=XSD.integer),
    'component': Literal('AX', datatype=XSD.string),
    'data': None,
    'energy': Literal(0.2, datatype=XSD.float),
    'magnitude': Literal(0.2, datatype=XSD.float),
    'focalMechanism': Literal(0.2, datatype=XSD.float),
    'sourceLatitude': Literal(0.2, datatype=XSD.float),
    'sourceLongitude': Literal(0.2, datatype=XSD.float),
    'sourceElevation': Literal(0.2, datatype=XSD.float),
}

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

SM = dict()
SM.update(SEMANTIC_MODEL_CLASSES)
SM.update(SEMANTIC_MODEL_LITERALS)
