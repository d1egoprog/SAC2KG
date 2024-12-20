from rdflib import Graph

from sac2kg.veo_mapper import VEOSemanticMapper
from sac2kg.veo_model import data_model
from sac2kg.sac_reader import SAC2VEO

class GraphManager:

    def __init__(self, path):
        self.graph = Graph()

    def add_graph(self, new_graph):
        self.graph += new_graph

    def save_graph(self, file_path, format="turtle"):
        self.graph.serialize(destination=file_path, format=format)

    def __str__(self):
        return self.graph.serialize(format='turtle')
