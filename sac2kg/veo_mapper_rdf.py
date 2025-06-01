#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the `VEOSemanticMapper` class, which is responsible for mapping seismic data into a semantic 
representation using RDF and the VEO ontology. It utilizes the `rdflib` library to construct and manipulate RDF graphs.
The module defines three main static methods for generating different semantic models:

1. `get_context_model`: Constructs the context model, which includes information about seismic networks, stations, 
  instruments, and their relationships.
2. `get_collection_model`: Constructs the collection model, which includes data points, their attributes, and 
  relationships to seismic networks and instruments.
3. `get_knowledge_model`: Constructs the knowledge model, which includes events, their attributes, locations, 
  alert levels, and relationships to other entities.
Additionally, the module provides utility methods for parsing and calculating seismic data attributes such as origin 
time, end time, sampling rate, and record duration.

Environment Variables:
- `ONTO_BASE_URI`: The base URI for the VEO ontology.

Namespaces:
- `SSN_SYSTEMS`: Namespace for SSN systems.
- `SOSA`: Namespace for SOSA ontology.
- `GEO`: Namespace for Geo ontology.
- `TIME`: Namespace for Time ontology.
- `VEO`: Namespace for the VEO ontology.

Classes:
- `VEOSemanticMapper`: A class for creating and managing RDF graphs based on the VEO ontology.

Attributes:
- `veo_graph`: An RDF graph used to store semantic data.

Usage:
- Instantiate the `VEOSemanticMapper` class to create and manage RDF graphs.
- Use the static methods to generate specific semantic models based on the provided data.
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

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

from sac2kg.veo_model import *


SSN_SYSTEMS = Namespace("http://www.w3.org/ns/ssn/systems#")
SOSA = Namespace('http://www.w3.org/ns/sosa/')
GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
TIME = Namespace('http://www.w3.org/2006/time#')
VEO = Namespace(os.getenv('ONTO_BASE_URI'))

class VEORDFMapper: 
  veo_graph = Graph()

  #missing_value = URIRef(VEO['MissingValue'])

  def __init__(self, schema=False):
    self.veo_graph.bind('sosa', SOSA)
    self.veo_graph.bind("geo", GEO)
    self.veo_graph.bind("time", TIME)
    self.veo_graph.bind("veo", VEO)
    
    if schema:
      self.veo_graph.parse(SCHEMA_FILE)
    
    #self.veo_graph.add((self.missing_value, RDF.type, RDFS.Resource))
    #self.veo_graph.add((self.missing_value, SKOS.note, Literal("The value is missing due to unavailable or incomplete sensor data.")))

  @staticmethod  
  def get_context_model(graph, model):
    graph.add((model.SM['SeismicNetwork'], RDF.type, VEO.SeismicNetwork))
    graph.add((model.SM['Station'], RDF.type, VEO.Station))
    graph.add((model.SM['Instrument'], RDF.type, VEO.Instrument))

    graph.add((model.SM['SeismicNetwork'], SOSA.hosts, model.SM['Station']))

    graph.add((model.SM['Point'], RDF.type, GEO.Point))
    graph.add((model.SM['Station'], VEO.isLocatedIn, model.SM['Point'])) 
    graph.add((model.SM['Point'], GEO.lat, model.SM['lat']))
    graph.add((model.SM['Point'], GEO.long, model.SM['long']))
    graph.add((model.SM['Point'], GEO.ele, model.SM['ele']))
    
    graph.add((model.SM['Station'], VEO.isComposedBy, model.SM['Instrument']))
    graph.add((model.SM['Instrument'], SOSA.hosts, model.SM['Station']))
    graph.add((model.SM['Instrument'], VEO.delta, model.SM['delta']))
    graph.add((model.SM['Instrument'], VEO.axis, model.SM['axis']))
    graph.add((model.SM['Instrument'], VEO.signalType, model.SM['signalType']))
    graph.add((model.SM['Instrument'], VEO.positivePolarity, model.SM['positivePolarity']))
    #graph.add((model.SM['Instrument'], VEO.unit, model.SM['unit']))
    return graph

  @staticmethod    
  def get_collection_model(graph, model):
    graph.add((model.SM['DataPointArray'], RDF.type, VEO.DataPointArray))
    graph.add((model.SM['DataPointArray'], VEO.dataPoints, model.SM['dataPoints']))
    graph.add((model.SM['DataPointArray'], SSN_SYSTEMS.systemLifetime, model.SM['systemLifetime']))
    graph.add((model.SM['SeismicNetwork'], VEO.generates, model.SM['DataPointArray']))
 
    for data_point, ground_displacement, amplitude in model.point_list:
      graph.add((data_point, RDF.type, VEO.DataPoint))
      graph.add((data_point, SOSA.phenomenonTime, model.SM['systemLifetime']))
      graph.add((data_point, SOSA.madeBySensor, model.SM['Instrument']))
      graph.add((model.SM['DataPointArray'], SOSA.hasMember, data_point))
      graph.add((ground_displacement, RDF.type, VEO.GroundDisplacement))
      graph.add((data_point, VEO.isListOf, ground_displacement))
      graph.add((ground_displacement, VEO.amplitude, amplitude))
      graph.add((ground_displacement, VEO.component, model.SM['component'])) 
    return graph  

  @staticmethod
  def get_knowledge_model(graph, model):
    graph.add((model.SM['DataPointMatrix'], RDF.type, VEO.DataPointMatrix))
    graph.add((model.SM['DataPointMatrix'], VEO.isComposedOf, model.SM['DataPointArray']))
    graph.add((model.SM['DataPointMatrix'], VEO.describes, model.SM['Event']))
    graph.add((model.SM['DataPointMatrix'], VEO.detectedAs, VEO.VolcanoTectonic))
    graph.add((model.SM['Event'], RDF.type, VEO.Event))
    graph.add((model.SM['Location'], RDF.type, VEO.Location))
    graph.add((model.SM['AlertLevel'], RDF.type, VEO.AlertLevel))
    graph.add((model.SM['Place'], RDF.type, GEO.Place))

    graph.add((model.SM['Event'], VEO.isIdentifiedAs,  VEO.VolcanoTectonic))
    graph.add((model.SM['Event'], VEO.magnitude, model.SM['magnitude']))
    graph.add((model.SM['Event'], VEO.energy, model.SM['energy']))
    graph.add((model.SM['Event'], VEO.focalMechanism, model.SM['focalMechanism']))

    graph.add((model.SM['Event'], VEO.hasSourceLocation, model.SM['Location'] ))
    graph.add((model.SM['Location'], GEO.lat, model.SM['slat']))
    graph.add((model.SM['Location'], GEO.long, model.SM['slong']))
    graph.add((model.SM['Location'], GEO.ele, model.SM['sele']))
    
    graph.add((model.SM['Event'], VEO.definedBy, model.SM['AlertLevel']))
    graph.add((model.SM['AlertLevel'], VEO.affects, model.SM['Place']))
    return graph
