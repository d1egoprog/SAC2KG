import os

from datetime import datetime

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import SKOS, RDF, RDFS

from .veo_model import SM

SCHEMA_FILE = 'owl/veo.schema.en.5.7.rdf'

SSN_SYSTEMS = Namespace("http://www.w3.org/ns/ssn/systems#")
SOSA = Namespace('http://www.w3.org/ns/sosa/')
GEO = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')
TIME = Namespace('http://www.w3.org/2006/time#')

VEO = Namespace(os.getenv('ONTO_BASE_URI'))

class VEOSemanticMapper: 
  veo_graph = Graph()

  missing_value = URIRef(VEO['MissingValue'])

  def __init__(self, schema=False):
    self.veo_graph.bind('sosa', SOSA)
    self.veo_graph.bind("geo", GEO)
    self.veo_graph.bind("time", TIME)
    self.veo_graph.bind("veo", VEO)
    
    if schema:
      self.veo_graph.parse(SCHEMA_FILE)
    
    self.veo_graph.add((self.missing_value, RDF.type, RDFS.Resource))
    self.veo_graph.add((self.missing_value, SKOS.note, Literal("The value is missing due to unavailable or incomplete sensor data.")))

  @staticmethod  
  def get_context_model(graph):
    graph.add((SM['Network'], RDF.type, VEO.SeismicNetwork))
    graph.add((SM['Station'], RDF.type, VEO.Station))
    graph.add((SM['Instrument'], RDF.type, VEO.Instrument))
    graph.add((SM['Location'], RDF.type, GEO.Point))

    graph.add((SM['Network'], SOSA.hosts, SM['Station']))

    graph.add((SM['Station'], VEO.isLocatedIn, SM['Location'])) 
    graph.add((SM['Location'], GEO.lat, SM['latitude']))
    graph.add((SM['Location'], GEO.long, SM['longitude']))
    graph.add((SM['Location'], GEO.ele, SM['elevation']))
    
    graph.add((SM['Station'], VEO.isComposedBy, SM['Instrument']))
    graph.add((SM['Instrument'], SOSA.hosts, SM['Station']))
    graph.add((SM['Instrument'], VEO.delta, SM['delta']))
    graph.add((SM['Instrument'], VEO.axis, SM['axis']))
    graph.add((SM['Instrument'], VEO.signalType, SM['signalType']))
    graph.add((SM['Instrument'], VEO.unit, SM['unit']))
    graph.add((SM['Instrument'], VEO.positivePolarity, SM['polarity']))
    return graph


  @staticmethod    
  def get_collection_model(graph):
    graph.add((SM[''], RDF.type, VEO.DataPointArray))
    graph.add((SM[''], VEO.dataPoints, SM['numberOfPoints']))
    graph.add((SM[''], VEO.systemLifetime, SM['lifeTime']))
    #random.randint(100, size=(SEMANTIC_MODEL_EXAMPLE['numberOfPoints']))
    for amplitude in range(10):
      graph.add((SM['DataPoint'], RDF.type, VEO.DataPoint))

      graph.add((SM['GroundDisplacement'], RDF.type, VEO.GroundDisplacement))
      graph.add((SM['GroundDisplacement'], VEO.amplitude, SM['amplitude']))
      graph.add((SM['GroundDisplacement'], VEO.component, SM['component']))

    
    return graph

  @staticmethod
  def get_knowledge_model(graph):
    #self.graph.add((SM['dataPointMatrix'], rdf.type, VEO.DataPointMatrix))
    graph.add((SM['event'], RDF.type, VEO.Event))
    graph.add((SM['volcanoTectonic'], RDF.type, VEO.VolcanoTectonic))
    graph.add((SM['sourceLocation'], RDF.type, VEO.Location))
    graph.add((SM['alertLevel'], RDF.type, VEO.AlertLevel))
    graph.add((SM['place'], RDF.type, GEO.Place))

    #self.graph.add((SM['dataPointMatrix'], VEO.describes, SM['event']))

    graph.add((SM['event'], VEO.isIdentifiedAs, SM['volcanoTectonic'] ))
    graph.add((SM['event'], VEO.magnitude, SM['magnitude']))
    graph.add((SM['event'], VEO.energy, SM['energy']))
    graph.add((SM['event'], VEO.focalMechanism, SM['focalMechanism']))

    graph.add((SM['event'], VEO.hasSourceLocation, SM['sourceLocation'] ))
    graph.add((SM['sourceLocation'], GEO.lat, SM['sourceLatitude']))
    graph.add((SM['sourceLocation'], GEO.long, SM['sourceLongitude']))
    graph.add((SM['sourceLocation'], GEO.ele, SM['sourceElevation']))
    
    graph.add((SM['event'], VEO.definedBy, SM['alertLevel']))
    graph.add((SM['alertLevel'], VEO.affects, SM['place']))
    return graph
