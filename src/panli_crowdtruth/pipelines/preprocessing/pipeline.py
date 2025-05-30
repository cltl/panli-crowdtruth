from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    prepare_crowdtruth_judgments,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="prepare_crowdtruth_judgments",
                func=prepare_crowdtruth_judgments,
                inputs={
                    "input_filepath": "params:prolific_input_filepath",
                    "n_classes": "params:n_classes",
                },
                outputs=["preprocessed_data", "config"],
            ),
        ]
    )
