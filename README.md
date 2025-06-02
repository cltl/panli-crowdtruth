# A CrowdTruth analysis of the PANLI dataset


## Overview

This repository contains an analysis of the PANLI dataset using the CrowdTruth framework. The goal is to evaluate annotation quality and gather insights from crowdsourced data.

## What is PANLI?

PANLI is a dataset designed for evaluating natural language inference (NLI) tasks. It includes a variety of sentence pairs annotated for entailment, contradiction, or neutrality.

## What is CrowdTruth?

CrowdTruth is a methodology and set of tools for measuring the quality of crowdsourced annotations by capturing inter-annotator disagreement, providing a more nuanced understanding of ambiguous data.

## Kedro Pipeline

This project is structured as a [Kedro](https://kedro.org/) pipeline, enabling reproducible, modular, and scalable data workflows. Kedro manages data processing, experiment tracking, and configuration, making it easier to organize and automate the analysis steps for the PANLI dataset. All data transformations and CrowdTruth metric computations are implemented as Kedro nodes and pipelines.

## Repository Structure

- `conf/` - Kedro configuration files for managing project settings and parameters.
- `data/` - Contains the PANLI dataset, preprocessed files, and results such as visualizations.
- `notebooks/` - Jupyter notebooks for data exploration and analysis.
- `src/` - Source code for running CrowdTruth metrics and processing data.

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/panli-crowdtruth.git
    ```
2. Install [Poetry](https://python-poetry.org/) for dependency management:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    Or follow the [official installation guide](https://python-poetry.org/docs/#installation).

3. Install the project dependencies:
    ```bash
    poetry install
    ```

4. Activate the virtual environment:
    ```bash
    poetry shell
    ```

## Running the Kedro Pipelines

You can execute the entire data analysis workflow or run individual pipeline segments using Kedro's command-line interface.

- **To run the full pipeline:**
    ```bash
    kedro run
    ```

- **To run a specific pipeline or node:**
    ```bash
    kedro run --pipelines=<pipeline_name>
    kedro run --nodes= <node_name>
    ```

Replace `<pipeline_name>` or `<node_name>` with the desired pipeline. Available pipelines, as defined in `pipeline_registry.py`, include:

- `compute_crowdtruth_metrics`
- `selection`
- `analysis`

 For more options, see the [Kedro documentation](https://docs.kedro.org/en/stable/04_user_guide/03_cli.html).

## Citation

If you use this repository, please cite the original PANLI dataset and CrowdTruth papers.

## License

This project is licensed under the Apache License 2.0.