from kedro.pipeline import Pipeline, node, pipeline

from .compute_metrics import compute_crowdtruth_metrics


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="compute_crowdtruth_metrics",
                func=compute_crowdtruth_metrics,
                inputs={
                    "input_filepath": "params:prolific_input_filepath",
                    "n_classes": "params:n_classes",
                },
                outputs=[
                    "crowdtruth_units",
                    "crowdtruth_workers",
                    "crowdtruth_annotations",
                    "crowdtruth_judgments",
                    "crowdtruth_jobs",
                ],
            ),
        ]
    )
