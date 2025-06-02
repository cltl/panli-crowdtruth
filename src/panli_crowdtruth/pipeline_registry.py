"""Project pipelines."""

from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from .pipelines.analysis import pipeline as analysis
from .pipelines.compute_crowdtruth_metrics import pipeline as compute_crowdtruth_metrics
from .pipelines.selection import pipeline as selection

# def register_pipelines() -> Dict[str, Pipeline]:
#     """Register the project's pipelines.

#     Returns:
#         A mapping from pipeline names to ``Pipeline`` objects.
#     """
#     pipelines = find_pipelines()
#     pipelines["__default__"] = sum(pipelines.values())
#     return pipelines


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    # Load all pipelines from the project
    pipelines = find_pipelines()

    # Create individual pipelines
    compute_crowdtruth_metrics_pipeline = compute_crowdtruth_metrics.create_pipeline()
    selection_pipeline = selection.create_pipeline()
    analysis_pipeline = analysis.create_pipeline()

    # Define the full pipeline by combining the individual pipelines
    full_pipeline = Pipeline(
        nodes=[
            compute_crowdtruth_metrics_pipeline,
            selection_pipeline,
            analysis_pipeline,
        ]
    )

    # Add the pipelines to the registry
    pipelines.update(
        {
            "__default__": full_pipeline,
            "auto": sum(pipelines.values()),
            "compute_crowdtruth_metrics": compute_crowdtruth_metrics_pipeline,
            "selection": selection_pipeline,
            "analysis": analysis_pipeline,
        }
    )

    return pipelines
