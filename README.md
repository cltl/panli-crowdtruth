# A CrowdTruth analysis of the PANLI dataset

> A reproducible analysis pipeline for measuring annotation quality and ambiguity in the PANLI dataset, using the CrowdTruth framework and Kedro.

## Overview

This repository analyzes the **PANLI** dataset using the **CrowdTruth** framework, a methodology for evaluating crowdsourced annotations by embracing disagreement and ambiguity. The goal is to assess annotation quality, reveal perspective variation, and support deeper insight into natural language inference (NLI).

The full analysis is described in:

> van Son, C. M. (2024). *Representative Resources for Perspective-Aware Natural Language Inference* (PhD thesis, Vrije Universiteit Amsterdam). [https://doi.org/10.5463/thesis.644](https://doi.org/10.5463/thesis.644)

## Background

### What is PANLI?

**[PANLI](https://github.com/cltl/panli)** is a benchmark dataset for **perspective-aware natural language inference (NLI)**, constructed from real-world vaccination discourse. Each sentence pair is annotated for entailment, contradiction, or neutrality, with special attention to multiple perspectives.

### What is CrowdTruth?

**[CrowdTruth](https://github.com/CrowdTruth/CrowdTruth-core)** is a methodology that leverages inter-annotator disagreement to measure annotation quality and ambiguity—especially useful in subjective or complex tasks like NLI.



## Project Structure

This project is implemented as a [Kedro](https://kedro.org/)  pipeline to ensure modular, scalable, and reproducible workflows.

```bash
📁 conf/        # Configuration files (Kedro settings and parameters)
📁 data/        # Raw and intermediate data (PANLI, results, plots)
📁 notebooks/   # Jupyter notebooks for exploration and reporting
📁 src/         # Source code: data processing, CrowdTruth computation
```


## Getting Started

1. Clone the repository
    ```bash
    git clone https://github.com/yourusername/panli-crowdtruth.git
    cd panli-crowdtruth
    ```
2. Install [Poetry](https://python-poetry.org/) (if needed)
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    Or follow the [official installation guide](https://python-poetry.org/docs/#installation).

3. Install dependencies
    ```bash
    poetry install
    ```

4. Activate the virtual environment
    ```bash
    poetry shell
    ```

## Running the Kedro Pipelines

Once the environment is activated, you can use Kedro to run the pipelines:


- **Run the full analysis pipeline:**
    ```bash
    kedro run
    ```

- **Run a specific pipeline or node:**
    ```bash
    kedro run --pipelines=<pipeline_name>
    kedro run --nodes=<node_name>
    ```

Available pipelines include:

- `compute_crowdtruth_metrics`: Computes CrowdTruth metrics to evaluate annotation quality and inter-annotator agreement.
- `selection`: Filters and selects relevant subsets of PANLI.
- `analysis`: Performs in-depth analysis and generates visualizations based on the processed data.

See `src/panli_crowdtruth/pipeline_registry.py` for the full list.


##  Working in JupyterLab

For interactive exploration:

```bash
kedro jupyter lab
```

This launches JupyterLab with Kedro's context preloaded, giving you direct access to datasets, pipelines, and configuration within the notebook interface.

## Citation

If you use this repository, please cite the following works:

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


## Related Projects


- [panli](https://github.com/cltl/panli) — The PANLI dataset
- [panli-models](https://github.com/cltl/panli-models) — Model evaluation on PANLI
- [crowdtruth](https://github.com/CrowdTruth/CrowdTruth-core) — CrowdTruth methodology and metrics
