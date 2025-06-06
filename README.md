# A CrowdTruth analysis of the PANLI dataset


## Overview

This repository contains an analysis of the PANLI dataset using the CrowdTruth framework. The goal is to evaluate annotation quality and gather insights from crowdsourced data.

## What is PANLI?

PANLI is a dataset designed for evaluating natural language inference (NLI) tasks. It includes a variety of sentence pairs annotated for entailment, contradiction, or neutrality.

## What is CrowdTruth?

CrowdTruth is a methodology and set of tools for measuring the quality of crowdsourced annotations by capturing inter-annotator disagreement, providing a more nuanced understanding of ambiguous data. See also the [CrowdTruth repository](https://github.com/CrowdTruth/CrowdTruth-core).

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

Run these commands after activating the Poetry shell, or by prefixing with `poetry run`.

- **To run the full pipeline:**
    ```bash
    kedro run
    ```

- **To run a specific pipeline or node:**
    ```bash
    kedro run --pipelines=<pipeline_name>
    kedro run --nodes=<node_name>
    ```

Replace `<pipeline_name>` or `<node_name>` with the desired pipeline. Available pipelines, as defined in `pipeline_registry.py`, include:

- `compute_crowdtruth_metrics`: Computes CrowdTruth metrics to evaluate annotation quality and inter-annotator agreement.
- `selection`: Filters and selects relevant data subsets for further analysis.
- `analysis`: Performs in-depth analysis and generates visualizations based on the processed data.

 For more options, see the [Kedro documentation](https://docs.kedro.org/en/stable/index.html).

## Using Kedro with JupyterLab

To interactively explore data and run Kedro pipelines in notebooks, you can use Kedro's JupyterLab integration.

Run the following command after activating the Poetry shell, or by prefixing with `poetry run`:


```bash
kedro jupyter lab
```


This will launch JupyterLab with the Kedro context preloaded, allowing you to access Kedro datasets, pipelines, and configuration directly within your notebooks.

## Citation

If you use this repository, please consider citing:

* van Son, C. M. (2024). *Representative Resources for Perspective-Aware Natural Language Inference* (PhD thesis, Vrije Universiteit Amsterdam). [https://doi.org/10.5463/thesis.644](https://doi.org/10.5463/thesis.644)

    <details>
    <summary>BibTeX</summary>
    ```bibtex
    @phdthesis{ba18bc83a2be4b29805c6b91aaa9a152,
        title = "Representative Resources for Perspective-Aware Natural Language Inference",
        author = "{van Son}, {Chantal Michelle}",
        year = "2024",
        month = nov,
        day = "1",
        doi = "10.5463/thesis.644",
        language = "English",
        type = "PhD-Thesis - Research and graduation internal",
        school = "Vrije Universiteit Amsterdam",
    }
    ```
    </details>


* Dumitrache, A., Inel, O., Aroyo, L., Timmermans, B., & Welty, C. (2018). CrowdTruth 2.0: Quality Metrics for Crowdsourcing with Disagreement. *arXiv preprint arXiv:1808.06080*. https://arxiv.org/abs/1808.06080

    <details>
    <summary>BibTeX</summary>

    ```bibtex
    @article{CrowdTruth2,
        author    = {Anca Dumitrache and Oana Inel and Lora Aroyo and Benjamin Timmermans and Chris Welty},
        title     = {CrowdTruth 2.0: Quality Metrics for Crowdsourcing with Disagreement},
        year      = {2018},
        url       = {https://arxiv.org/abs/1808.06080},
    }
    ```
    </details>

## License

This project is licensed under the Apache License 2.0.