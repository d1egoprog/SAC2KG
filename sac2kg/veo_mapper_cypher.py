#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from neo4j import GraphDatabase

# Neo4j config
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"

class VEOCypherMapper: 
  
    def __init__(self, base_model=None):
        self.base_model = base_model
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session(database="neo4j") as session:
            session.execute_write(get_context_model, base_model)
            session.execute_write(get_collection_model, base_model)
            session.execute_write(get_knowledge_model, base_model)
            driver.close()   

def get_context_model(tx, model):
    tx.run("MERGE (sn:SeismicNetwork {name: $name})", name=model.seismic_network)
    tx.run("MERGE (s:Station {name: $name})", name=model.station)  

    tx.run("MERGE (po:Point {lat: $lat, long: $long, ele: $ele})",
        lat=model.latitude, long=model.longitude, ele=model.elevation)

    tx.run("MERGE (ins:Instrument " 
           "{name: $name, delta: $delta, axis: $axis, signal_type: $signal_type})",
        name=model.instrument, delta=model.delta, 
        axis=model.axis, signal_type=model.signal_type)

    tx.run("MATCH (sn:SeismicNetwork {name: $nameSb}) "
        "MATCH (s:Station {name: $nameSt}) "
        "MERGE (sn)-[:HOSTS]->(s) ",
        nameSb=model.seismic_network, nameSt=model.station)

    tx.run("MATCH (s:Station {name: $name}) "
        "MATCH (po:Point {lat: $lat, long: $long, ele: $ele}) "
        "MERGE (s)-[:LOCATED_IN]->(po) ",
        name=model.station, lat=model.latitude,
        long=model.longitude, ele=model.elevation)

    tx.run("MATCH (s:Station {name: $name}) "
        "MATCH (ins:Instrument {delta: $delta, axis: $axis, signal_type: $signal_type}) "
        "MERGE (s)-[:IS_COMPOSED_BY]->(ins) ",
        name=model.station, delta=model.delta,
        axis=model.axis, signal_type=model.signal_type)
    return None

def get_collection_model(tx, model):
    tx.run("MERGE (dpa:DataPointArray "
           "{id: $id, dataPoints: $dp, systemLifetime: $slt, data: $pl, component: $c }) ",
        id=model.data_point_array, dp=model.data_points,
        pl=model.data, c=model.component, slt=model.system_lifetime)
    
    tx.run(" MATCH (sn:SeismicNetwork {name: $sN}) "
           " MATCH (dpa:DataPointArray {id: $id}) "
           " MERGE (sn)-[:GENERATES]->(dpa) ",
        sN=model.seismic_network,
        id=model.data_point_array)
    
    tx.run(" MATCH (ins:Instrument "
           "{name: $name, delta: $delta, axis: $axis, signal_type: $signal_type}) "
           " MATCH (dpa:DataPointArray {id: $dpa}) "
           " MERGE (dpa)-[:MADE_BY_SENSOR]->(ins) ",
        dpa=model.data_point_array,
        name=model.instrument, delta=model.delta, 
        axis=model.axis, signal_type=model.signal_type)
    return None

def get_knowledge_model(tx, model):

    tx.run("MERGE (l:Location {lat: $lat, long: $long, ele: $ele, depth: $de})",
        lat=model.source_latitude, long=model.source_longitude, ele=model.source_elevation, de=model.depth)
    
    tx.run("MERGE (e:Event {identified_event: $e, magnitude: $m, energy: $ene, focalMechanism: $fm})",
           e=model.event, m=model.magnitude,
           ene=model.energy, fm=model.focal_mechanism)

    tx.run("MERGE (al:AlertLevel {id: $al})",
            al=model.alert_level)
    
    tx.run(" MATCH (dpa:DataPointArray {id: $dpa}) "
           " MATCH (e:Event {identified_event: $e, magnitude: $m, energy: $ene, focalMechanism: $fm}) "
           " MERGE (dpa)-[:DESCRIBES]->(e) ",
        e=model.event, m=model.magnitude,
        ene=model.energy, fm=model.focal_mechanism,
        dpa=model.data_point_array)

    tx.run(" MATCH (l:Location {lat: $lat, long: $long, ele: $ele, depth: $de}) "
           " MATCH (e:Event {identified_event: $e, magnitude: $m, energy: $ene, focalMechanism: $fm}) "
           " MERGE (e)-[:HAS_SOURCE_LOCATION]->(l) ",
        e=model.event, m=model.magnitude,
        ene=model.energy, fm=model.focal_mechanism,
        lat=model.source_latitude, long=model.source_longitude, ele=model.source_elevation, de=model.depth)
    
    tx.run("MATCH (e:Event {identified_event: $e, magnitude: $m, energy: $ene, focalMechanism: $fm}) "
        "MATCH (al:AlertLevel {id: $al}) "
        "MERGE (e)-[:HAS_ALERT_LEVEL]->(al)",
        e=model.event, m=model.magnitude,
        ene=model.energy, fm=model.focal_mechanism,
        al=model.alert_level)
    return None









