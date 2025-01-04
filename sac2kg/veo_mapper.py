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

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import SKOS, RDF, RDFS

from .veo_model import *


SSN_SYSTEMS = Namespace("http://www.w3.org/ns/ssn/systems#")
SOSA = Namespace('http://www.w3.org/ns/sosa/')
GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
TIME = Namespace('http://www.w3.org/2006/time#')
VEO = Namespace(os.getenv('ONTO_BASE_URI'))

class VEOSemanticMapper: 
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


"""
    'originTime': _parse_origin_time(),  # Origin Time from multiple fields
    'beginTime': _parse_origin_time(),#_parse_begin_time(),  # Record Start Time
    'endTime': _parse_end_time(),  # Record End Time (calculated)
    'samplingRate': _calculate_sampling_rate(),  # Calculated Sampling Rate
    'recordDuration': _calculate_duration(),  # Duration of Record (seconds)

    @staticmethod
    def _parse_origin_time(sac_headers):
        try:
            year = sac_headers.get('nzyear', '1970')
            jday = sac_headers.get('nzjday', '001')
            hour = sac_headers.get('nzhour', '00')
            minute = sac_headers.get('nzmin', '00')
            second = sac_headers.get('nzsec', '00')
            millisecond = sac_headers.get('nzmsec', '000')
            date_str = f"{year}-{jday} {hour}:{minute}:{second}.{millisecond}"
            return datetime.strptime(date_str, '%Y-%j %H:%M:%S.%f').isoformat()
        except Exception as e:
            return None

    def _parse_end_time(veo_data_model):
        if veo_data_model['numberOfPoints'] != 'None' and veo_data_model['delta'] != 'None':
            try:
                duration = int(veo_data_model['numberOfPoints']) * float(veo_data_model['delta'])
                end_time = datetime.fromisoformat(veo_data_model['originTime']) + timedelta(seconds=duration)
                return end_time.isoformat()
            except Exception as e:
                return 'None'
        return 'None'

    def _calculate_sampling_rate(sac_headers):
        try:
            return 1 / float(sac_headers.get('delta', '1'))
        except ZeroDivisionError:
            return 'None'

    def _calculate_duration(veo_data_model):
        if veo_data_model['numberOfPoints'] != 'None' and veo_data_model['delta'] != 'None':
            try:
                return float(veo_data_model['numberOfPoints']) * float(veo_data_model['delta'])
            except Exception as e:
                return 'None'
        return 'None'

"""    