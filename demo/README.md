# Usage Demo from SAC2KG Library

This Python library provides tools to convert SAC and JSON files into Knowledge Graphs following the VEO (Volcano Event Ontology) Schema. The library supports both direct usage through Python code and a Command-Line Interface (CLI) for flexible operation.

---

## Features
- **File Conversion**: Convert SAC and JSON files into knowledge graph formats such as N-Triples, Turtle, and RDF.
- **Folder Processing**: Traverse directories to process multiple files while replicating folder structures.
- **Ontology Integration**: Optionally include the VEO schema in the generated knowledge graphs.
- **CLI Utility**: Simple and user-friendly CLI for quick and efficient file processing.

---

## Installation

``` bash  
pip install -i https://test.pypi.org/simple/ sac2kg
```
---

## Usage

### CLI

The library includes a CLI tool for file and folder processing. Below are the available commands and options:

#### Command Syntax:

```bash
python main.py [OPTIONS] traceFile kgFile
```

#### Arguments:

- **`traceFile`**:  Path to the input trace file (SAC or JSON) or directory containing trace files if -d is specified.
- **`kgFile`**: Path to the output knowledge graph file or directory where the results will be stored if -d is specified.

#### Options:
- `-f, --format`  
  Supported input formats: `sac` (default) or `json`.  
  Example: `--format json`

- `-o, --output`  
  Output knowledge graph formats: `n3`, `ttl` (default), `rdf`.  
  Example: `--output ttl`

- `-s, --schema`  
  Include the VEO ontology/schema in the generated knowledge graph.  
  Example: `--schema`

- `-d, --directory`  
  Enable directory traversal to process multiple files. Only SAC files are recognized.  
  Example: `--directory`

---

### Examples

#### Convert a single SAC file to Turtle format:
```bash
python main.py my_trace.sac my_kg.ttl
```

#### Convert a JSON file to RDF format:
```bash
python main.py my_trace.json my_kg.rdf --format json --output rdf
```

#### Process an entire directory of SAC files:
```bash
python main.py input_dir output_dir --directory
```

#### Include the VEO schema in the output knowledge graph:
```bash
python main.py my_trace.sac my_kg.ttl --schema
```
