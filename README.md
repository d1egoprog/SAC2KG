# SAC2KG a Neuro-Symbolic library for Volcano Event Detection

![Version](https://img.shields.io/badge/Version-0.3.3-blue) ![License](https://img.shields.io/badge/License-MIT-green) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14532821.svg)](https://doi.org/10.5281/zenodo.14532821)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  

The SAC2KG Python Library provides tools to load, manipulate, and generate RDF knowledge graphs based on the Volcano Event Ontology (VEO). Designed with simplicity and extensibility in mind, this library streamlines ontology-based data modeling for seismic sensor networks and related domains.  

---

## **Table of Contents**  
- [Introduction](#introduction)  
- [Features](#features)  
- [Installation](#installation)  
- [Quick Start](#quick-start)  
- [API Overview](#api-overview)  
- [Contributing](#contributing)  
- [License](#license)  

---

## **Introduction**  
This library is the Python implementation of the Volcano Event Ontology (VEO), enabling users to:  

- Generate RDF graphs compliant with VEO.  
- Validate and extend ontology-based models.  
- Interface with SOSA, TIME, and GEO vocabularies.  
- Simplify integration with machine learning workflows and early warning systems.  

---

## **Features**  
- **Ontology Management**: Load and extend the VEO ontology.  
- **Graph Generation**: Build RDF triples programmatically.  
- **Data Validation**: Ensure compliance with the ontology structure.  
- **Custom Mapping**: Map seismic data to the ontology classes and properties.  

---

## **Installation**  
Install the library from TestPyPI: 

``` bash  
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sac2kg
```

Alternatively, install the latest version from source:

``` bash  
git clone https://github.com/d1egoprog/sac2kg.git  
cd sac2kg  
pip install .  
```
## Usage

### As a Python Library

1. Download the [SAC](demo/example_trace.sac) (Seismic Analysis Code) or create a JSON file `example_trace.json` in some place of your file system. A [copy](demo/example_trace.json) is uploaded in the demo folder.

``` JSON
 {
    "seismic_network": "US",
    "station": "ANMO",
    "instrument": "Broadband Seismometer",
    "delta": 2.5,
    "axis": 0.75,
    "signal_type": "itime",
    "unit": "m/s",
    "positive_polarity": true,
    "latitude": 34.945,
    "longitude": -106.457,
    "elevation": 1850.0,
    "system_lifetime": "2023-12-15T08:00:00Z",
    "data_points": 10,
    "component": "Z",
    "data": [0.01, 0.12, -0.03, 0.04, -0.08, 0.10, -0.02, 0.03, -0.01, 0.07],
    "event": "Earthquake",
    "energy": 1.2e12,
    "magnitude": 4.5,
    "focal_mechanism": "Strike-slip",
    "source_latitude": 35.200,
    "source_longitude": -105.750,
    "source_elevation": 1500.0,
    "depth": 12.3,
    "alert_level": 2
}
```

2. Copy the code into a Python module file and execute it or intagrate in your solution.

``` Python  
import sac2kg

print('-------Reading a SAC file and create the VEO-KG-------------------')
g1 = sac2kg.read_from_json('example_trace.sac', ontology=False )
sac2kg.graph_store(g1, 'example_sac_kg.ttl', output='ttl')

print('-------Reading a JSON file and create the VEO-KG-------------------')
g2 = sac2kg.read_from_json('example_trace.json', ontology=False )
sac2kg.graph_store(g2, 'example_json_kg.ttl', output='ttl')
```

### Using the Command Line Interface (CLI)

The library provides a robust Command-Line Interface (CLI) tool located in the [demo/](demo/) folder. This tool simplifies the process of mapping SAC or JSON trace files into Knowledge Graphs following the VEO schema. Whether you are working with single files or entire directories, the CLI provides flexible options for various use cases.

To explore the CLI in action, navigate to the  [demo/](demo/) folder and use the provided script. Below is an overview of its features and an example use case.

``` bash
python -m sac2kg my_trace.sac my_kg
```

### Advanced Usage

- **Custom Ontology Extensions:** Extend the base ontology by adding new classes and properties using the provided ontology builder tools.
- **Integration with Existing RDF Graphs:** Merge the generated RDF graphs with other semantic web datasets.

## Documentation

Refer to the [full documentation](docs/index.md) for detailed usage instructions, API references, and advanced examples.

## Citations 

If this work is with your interest, you can read the associated [paper](), and if you use it in your research, please don't forget to cite 👍 this work; the suggested citation in BibTex format is:

``` BibTex
@article{Rincon2025,
    author = {Diego Rincon-Yanez and Sabrina Senatore and Declan O'Sullivan},
    doi = {TBP},
    issn = {16113349},
    journal = {Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics)},
    month = {June},
    title = {Scaling NeuroSymbolic AI integration for Seismic Event Detection},
    volume = {TBP},
    year = {To be Published},
}
```

## Contributing

Contributions are welcome! Please follow the [contribution guidelines](CONTRIBUTING.md).

### Steps to Contribute

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with a descriptive message.
4. Submit a pull request to the main repository.

## License

This library is licensed under the [MIT License](LICENSE).

## Troubleshooting

If there are any troubles or you have any questions, please open an issue stating the encountered problem. Contributing is always welcome. The [Github repository Issues URL](https://github.com/d1egoprog/SAC2KG/issues).  And contributing is always welcome. The [Github repository URL](https://github.com/d1egoprog/SAC2KG).


Happy hacking!! 🖖🖖.
