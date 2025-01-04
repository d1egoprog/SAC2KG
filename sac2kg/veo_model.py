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

from dataclasses import dataclass, field
from typing import List

from datetime import datetime

@dataclass
class VEOBaseModel:
    seismic_network: str = None
    station: str = None
    instrument: str = None
    delta: float = None
    axis: float = None
    signal_type: str = None
    unit: str = None
    positive_polarity: bool = None
    latitude: float = None
    longitude: float = None
    elevation: float = None
    system_lifetime: datetime = None #datetime.now()
    data_points: int = None
    component: str = None
    data: List[float] = None #field(default_factory=lambda: [0.1, 0.3])
    event: str = None
    energy: float = None
    magnitude: float = None
    focal_mechanism: str = None
    source_latitude: float = None
    source_longitude: float = None
    source_elevation: float = None
    depth: float = None
    alert_level: int = None

from sac2kg.veo_definitions import *

@dataclass
class VEORDF(VEOBaseModel):

    def __post_init__(self):
        self.SM = dict()
        self.SM.update(self.parse_classes())
        self.SM.update(self.parse_literals())
        if len(self.data) != 0:
            self.point_list = self.parse_data()
    
    def parse_classes(self) -> dict:
        classes = dict()
        classes.update(get_uri('Blast'))
        classes.update(get_uri('Noise'))
        classes.update(get_uri('LongPeriod'))
        classes.update(get_uri('VolcanoTectonic'))


        if self.seismic_network != None:
            classes.update(get_uri('SeismicNetwork', self.seismic_network))
        if self.station != None:
            classes.update(get_uri('Station', self.station))
        if self.instrument != None:
            classes.update(get_uri('Instrument', self.instrument))
        #if self.latitude != None and self.longitude != None:
        
        classes.update(get_uri('Point', (self.latitude, self.longitude, self.elevation)))
        classes.update(get_uri('DataPointArray'))
        classes.update(get_uri('DataPointMatrix'))
        classes.update(get_uri('Event'))
        classes.update(get_uri('AlertLevel', self.alert_level))
        classes.update(get_uri('Location', (self.latitude, self.longitude, self.elevation)))
        classes.update(get_uri('Place'))
        
        classes.update(get_uri('Interval'))
        
        return classes

    def parse_literals(self) -> dict:
        literals = dict()

        if self.delta != None:
            literals.update(get_literal('delta', self.delta))
        if self.axis != None:
            literals.update(get_literal('axis', self.axis))
        if self.signal_type != None:
            literals.update(get_literal('signalType', self.signal_type))
        if self.unit != None:
            literals.update(get_literal('unit', self.unit))
        if self.positive_polarity != None:
            literals.update(get_literal('positivePolarity', self.positive_polarity))
        if self.latitude != None:
            literals.update(get_literal('lat', self.latitude))
        if self.longitude != None:
            literals.update(get_literal('long', self.longitude))
        if self.elevation != None:
            literals.update(get_literal('ele', self.elevation))

        literals.update(get_literal('dataPoints', self.data_points))
        literals.update(get_literal('systemLifetime', self.system_lifetime))
        literals.update(get_literal('component', self.component))
        literals.update(get_literal('amplitude', self.data))
        literals.update(get_literal('focalMechanism', self.focal_mechanism))
        literals.update(get_literal('energy', self.energy))
        literals.update(get_literal('magnitude', self.magnitude))
        literals.update(get_literal('hasLevel', self.alert_level))
        literals.update(get_literal('slat', self.source_latitude))
        literals.update(get_literal('slong', self.source_longitude))
        literals.update(get_literal('sele', self.source_elevation))
        return literals
    
    def parse_data(self) -> dict:
        point_list = list()
        for amplitude in self.data:
            dp = get_uri('DataPoint',nokey=True)
            ins = get_uri('Instant', nokey=True)
            gd = get_uri('GroundDisplacement',nokey=True)
            amp = get_literal('amplitude', amplitude, nokey=True)
            point_list.append((dp, gd, amp))
        return point_list
