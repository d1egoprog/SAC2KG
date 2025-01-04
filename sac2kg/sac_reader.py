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

import numpy as np

from datetime import datetime

from pysac import SACTrace

class SAC2VEO:

    sac_headers = dict()
    
    @staticmethod
    def _parse_origin_time(file):
        try:
            year = file.nzyear
            jday = file.nzjday
            hour = file.nzhour
            minute = file.nzmin
            second = file.nzsec
            millisecond = file.nzmsec
            date_str = f"{year}-{jday} {hour}:{minute}:{second}.{millisecond}"
            return datetime.strptime(date_str, '%Y-%j %H:%M:%S.%f').isoformat()
        except Exception as e:
            return None

    @staticmethod
    def _parse_file(path: str):
        file = SACTrace.read(path)
        # Initialize SAC headers and VEO data model with default values

        veo_data_model = {
            'seismic_network': file.knetwk, #get('knetwk,  # Network Code
            'station': file.kstnm,  # Station Name
            'instrument': file.kinst,  # Instrument Name
            'delta': file.delta, #file.delta,  # Sampling Interval (s)
            'axis': len(file.kcmpnm), #file.cmpaz,  # Component Azimuth (degrees)
            'signal_type': file.iftype,  # Signal Type
            'unit':  file.idep,  # Unit of Measurement
            'positive_polarity': file.lpspol,  # Polarity
            'latitude': file.stla,  # Station Latitude (degrees)
            'longitude': file.stlo,  # Station Longitude (degrees)
            'elevation': file.stel,  # Station Elevation (meters)
            'system_lifetime': SAC2VEO._parse_origin_time(file),  # Header Version Number (for lifetime estimation)
            'data_points': file.npts,  # Number of Data Points
            'component': file.kcmpnm,  # Component Name (e.g., N, E, Z)
            'data': file.data.tolist(),  # Placeholder for waveform data
            'event': file.kevnm,  # Event Name
            'energy': None,  # Estimated Energy
            'magnitude': file.mag,  # Magnitude
            'focal_mechanism': file.imagtyp,  # Focal Mechanism Description
            'source_latitude': file.evla,  # Event Latitude (degrees)
            'source_longitude': file.evlo,  # Event Longitude (degrees)
            'source_elevation': file.leven,  # Event Elevation (meters)
            'depth': file.stdp,  # Source Depth (km)
            'alert_level': None,  # Alert Level (if applicable)
        }
        return veo_data_model

"""
Maps a VEOBaseModel dictionary to SACTrace-compatible fields.

:param veo_data_model: Dictionary containing VEOBaseModel fields.
:return: Dictionary of SACTrace-compatible fields.
"""
class VEO2SAC:

    def __init__(self, model):
        sac_data = {
            'knetwk': model['seismic_network'],
            'kstnm': model['station'],
            'kinst': model['instrument'],
            'delta': model['delta'],
            'kcmpnm': model['component'],
            'iftype': model['signal_type'],
            'lpspol': model['positive_polarity'],
            'stla': model['latitude'],
            'stlo': model['longitude'],
            'stel': model['elevation'],
            'npts': len(model['data']),
            'data':  np.array(model['data']),
            'kevnm': model['event'],
            'mag': model['magnitude'],
            'evla': model['source_latitude'],
            'evlo': model['source_longitude'],
            'stdp': model['depth'],
        }

        self.sac = SACTrace(**sac_data)

    def save_file(self, path):
        self.sac.write(path)