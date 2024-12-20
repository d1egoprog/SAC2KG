from datetime import datetime, timedelta

from pysac import SACTrace

class SAC2VEO:

    sac_headers = dict()

    @staticmethod
    def _parse_file(path):
        file = SACTrace.read(path)
        # Initialize SAC headers and VEO data model with default values

        veo_data_model = {
            'network': file.knetwk, #get('knetwk,  # Network Code
            'station': file.kstnm,  # Station Name
            'instrument': file.kinst,  # Instrument Name
            'delta': file.delta, #file.delta,  # Sampling Interval (s)
            'axis': file.cmpaz,  # Component Azimuth (degrees)
            'signalType': file.iftype,  # Signal Type
            'unit': file.kuser0,  # Unit of Measurement
            'polarity': file.lpspol,  # Polarity
            'latitude': file.stla,  # Station Latitude (degrees)
            'longitude': file.stlo,  # Station Longitude (degrees)
            'elevation': file.stel,  # Station Elevation (meters)
            'lifeTime': file.nvhdr,  # Header Version Number (for lifetime estimation)
            'numberOfPoints': file.npts,  # Number of Data Points
            'component': file.kcmpnm,  # Component Name (e.g., N, E, Z)
            'data': file.data,  # Placeholder for waveform data
            'event': file.kevnm,  # Event Name
            'energy': file.user0,  # Estimated Energy
            'magnitude': file.user1,  # Magnitude
            'focalMechanism': file.kuser1,  # Focal Mechanism Description
            'sourceLatitude': file.evla,  # Event Latitude (degrees)
            'sourceLongitud': file.evlo,  # Event Longitude (degrees)
            'sourceElevation': file.leven,  # Event Elevation (meters)
            'alertLevel': file.ka,  # Alert Level (if applicable)
            # New Mappings
            'depth': file.stdp,  # Source Depth (km)
        }
        return veo_data_model
