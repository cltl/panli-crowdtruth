from kedro.pipeline import Pipeline, node, pipeline

from .nodes import compute_crowdtruth_metrics


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="compute_crowdtruth_metrics",
                func=compute_crowdtruth_metrics,
                inputs={
                    "data": "preprocessed_data",
                    "config": "config",
                },
                outputs=["units", "workers", "annotations", "judgments", "jobs"],
            ),
        ]
    )
