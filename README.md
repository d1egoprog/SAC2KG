# SAC2KG  

![Version](https://img.shields.io/badge/Version-0.2.0-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  

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
Install the library from PyPI:  
``` bash  
pip install sac2kg
```

Alternatively, install the latest version from source:

``` bash  
git clone https://github.com/d1egoprog/sac2kg.git  
cd sac2kg  
pip install .  
```
## Usage

### Example: Mapping and Exporting Data

``` Python  
from sac2kg import GraphManager  

# Initialize the ontology generator  
veo = GraphManager()  

# Sample data to map
data = {
    "network": "TRZ",
    "station": "CPV",
    "instrument": "Seismometer",
    "latitude": 40.123,
    "longitude": -8.456,
    "elevation": 500,
    "data": [0.1, 0.2, 0.3],
}

# Map the data to the ontology
rdf_graph = mapper.map_to_ontology(data)

# Export the RDF graph
rdf_graph.serialize("output.ttl", format="turtle")
print("RDF data exported to output.ttl")
```

## Citations 

If this work is with your interest, you can read the associated [paper](), and if you use it in your research, please don't forget to cite 👍 this work; the suggested citation in BibTex format is:

``` BibTex
@article{Rincon2025a,
    author = {Diego Rincon-Yanez and Sabrina Senatore and Declan O'Sullivan},
    doi = {},
    issn = {},
    journal = {Submited to Evaluation to ESWC 2025 - Resource Track},
    month = {6},
    title = {From Data to Knowledge: A SAC2KG a Neuro-Symbolic library for Volcano Event Detection},
    volume = {},
    year = {2025},
}
``` 

### Advanced Usage

- **Custom Ontology Extensions:** Extend the base ontology by adding new classes and properties using the provided ontology builder tools.
- **Integration with Existing RDF Graphs:** Merge the generated RDF graphs with other semantic web datasets.

## Documentation

Refer to the [full documentation](docs/index.md) for detailed usage instructions, API references, and advanced examples.

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
