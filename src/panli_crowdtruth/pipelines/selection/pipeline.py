from kedro.pipeline import Pipeline, node, pipeline

from .nodes import balance_number_of_workers


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="balance_number_of_workers",
                func=balance_number_of_workers,
                inputs={
                    "df_crowdtruth_workers": "crowdtruth_workers",
                    "df_crowdtruth_judgments": "crowdtruth_judgments",
                    "df_prolific_annotations": "prolific_annotations_all",
                    "df_prolific_workers": "prolific_workers_all",
                },
                outputs=["prolific_annotations_selected", "prolific_workers_selected"],
            ),
        ]
    )
