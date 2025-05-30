from typing import Tuple

import pandas as pd


def balance_number_of_workers(
    df_crowdtruth_workers: pd.DataFrame,
    df_crowdtruth_judgments: pd.DataFrame,
    df_prolific_annotations: pd.DataFrame,
    df_prolific_workers: pd.DataFrame,
    n_workers: int = 10,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Select top N workers per unit. This is done to balance the number of
    participants per unit.


    """

    # Merge judgments and workers
    workers_merge = df_crowdtruth_workers.reset_index()[["worker", "wqs"]]
    merged = df_crowdtruth_judgments.reset_index().merge(
        workers_merge, on="worker", how="left"
    )

    # Find top 10 workers per unit
    to_drop = []
    for _, unit_judgments in merged.groupby("unit"):
        n_judgments = len(unit_judgments)
        if n_judgments > n_workers:
            drop_judgments = (
                unit_judgments.sort_values("wqs", ascending=False)
                .iloc[n_workers:]
                .judgment.tolist()
            )
            to_drop.extend(drop_judgments)

    # Drop from data
    df_annotations_selected = df_prolific_annotations[
        ~df_prolific_annotations.judgment_id.isin(to_drop)
    ]
    df_workers_selected = df_prolific_workers[
        df_prolific_workers.worker_id.isin(df_annotations_selected.worker_id)
    ]

    return df_annotations_selected, df_workers_selected
