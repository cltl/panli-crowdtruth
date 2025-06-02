from kedro.pipeline import Pipeline, node, pipeline

from .workers_demographics import analyse_demographics
from .workers_performance import analyse_performance


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="analyse_demographics",
                func=analyse_demographics,
                inputs={"df_prolific_workers": "prolific_workers_final"},
                outputs="images_demographics",
            ),
            node(
                name="analyse_performance",
                func=analyse_performance,
                inputs={
                    "df_prolific_workers": "prolific_workers_final",
                    "df_crowdtruth_judgments": "crowdtruth_judgments",
                    "df_crowdtruth_workers": "crowdtruth_workers",
                    "df_crowdtruth_units": "crowdtruth_units",
                },
                outputs="images_performance",
            ),
        ]
    )
