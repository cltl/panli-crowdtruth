from typing import Dict

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from panli_crowdtruth.pipelines.analysis.config_plotly import DIR_IMAGES, PLOTLY_COLORS


def time_taken_per_task(df: pd.DataFrame) -> px.histogram:
    """
    Generates a histogram showing the distribution of time taken per task by workers.

    Args:
        df: DataFrame containing worker information, including 'time_taken' column.

    Returns:
        px.histogram: Plotly histogram object showing the distribution of time taken
            per task.
    """
    # Filter out negative or zero time taken
    df_time = df[df.entered_code != "Manual Completion"].copy()
    df_time["time_taken_minutes"] = df_time["time_taken"] / 60

    # Create histogram of time taken per task
    fig = px.histogram(
        df_time,
        x="time_taken_minutes",
        color_discrete_sequence=PLOTLY_COLORS,
        marginal="box",
    )

    # Update layout
    fig.update_layout(
        xaxis_title="completion time (in minutes)", yaxis_title="participants (n)"
    )

    return fig


def prolific_scores(df_prolific_workers: pd.DataFrame) -> px.histogram:
    """
    Generates a histogram showing the distribution of Prolific scores of workers.

    Args:
        df_prolific_workers: DataFrame containing worker information,
            including 'prolific_score' column.

    Returns:
        px.histogram: Plotly histogram object showing the distribution of Prolific
            scores.
    """

    df_prolific_workers = df_prolific_workers.sort_values(
        "completed_date_time", ascending=False
    )
    df_prolific_workers = df_prolific_workers.drop_duplicates(subset=["worker_id"])

    # Create histogram of Prolific scores
    fig = px.histogram(
        df_prolific_workers,
        x="prolific_score",
        marginal="box",
        color_discrete_sequence=PLOTLY_COLORS,
    )

    # Update layout
    fig.update_layout(
        xaxis_title="Prolific approval rate", yaxis_title="participants (n)"
    )

    return fig


def worker_quality_score(df_crowdtruth_workers: pd.DataFrame) -> px.histogram:
    """
    Generates a histogram showing the distribution of worker quality scores.

    Args:
        df_prolific_workers: DataFrame containing worker information,
            including 'wqs' column.

    Returns:
        px.histogram: Plotly histogram object showing the distribution of worker
            quality scores.
    """
    # Create histogram of worker quality scores
    fig = px.histogram(
        df_crowdtruth_workers,
        x="wqs",
        marginal="box",
        color_discrete_sequence=PLOTLY_COLORS,
    )

    # Update layout
    fig.update_layout(
        xaxis_range=[-0.01, 1.01],
        xaxis_title="worker quality score",
        yaxis_title="participants (n)",
    )

    return fig


def mean_wqs_per_batch(
    df_crowdtruth_judgments: pd.DataFrame,
    df_crowdtruth_workers: pd.DataFrame,
    df_crowdtruth_units: pd.DataFrame,
) -> px.bar:
    """
    Generates a bar chart showing the mean worker quality score (WQS) per batch.

    Args:
        df_crowdtruth_judgments: DataFrame containing judgments with
            'batch_id' and 'worker'.
        df_crowdtruth_workers: DataFrame containing worker information, including 'wqs'.
        df_crowdtruth_units: DataFrame containing unit information.

    Returns:
        Plotly bar chart object showing the mean WQS per batch.
    """
    # Merge judgments with workers to get WQS
    select_judgments = df_crowdtruth_judgments[["unit", "worker"]]
    select_units = df_crowdtruth_units["input.batch_id"].reset_index()
    select_workers = df_crowdtruth_workers["wqs"]
    df = select_judgments.merge(select_units, on="unit", how="left")
    df = df.merge(select_workers, on="worker", how="left")
    df = (
        df.drop(columns="unit")
        .drop_duplicates()
        .rename(columns={"input.batch_id": "batch_id"})
    )

    # Group by batch and calculate mean WQS
    df_mean_wqs_batch = df.groupby("batch_id")["wqs"].mean().to_frame().reset_index()
    df_mean_wqs_batch["batch_id"] = df_mean_wqs_batch["batch_id"].astype(str)

    # Create bar chart of mean WQS per batch
    fig = px.bar(
        df_mean_wqs_batch,
        x="wqs",
        y="batch_id",
        #     title="Fluent languages (other than English)",
        color_discrete_sequence=PLOTLY_COLORS,
    )

    # Update layout
    fig.update_layout(
        xaxis_title="average worker quality score",
        yaxis_title="batch id",
    )

    # Add vertical line for mean WQS across all batches
    line_mean = df_mean_wqs_batch["wqs"].mean()
    fig.update_layout(
        xaxis_range=[0, 1],
        shapes=[
            dict(
                type="line",
                yref="y",
                y0=-1,
                y1=21,
                xref="x",
                x0=line_mean,
                x1=line_mean,
            )
        ],
    )

    return fig


def analyse_performance(
    df_prolific_workers: pd.DataFrame,
    df_crowdtruth_judgments: pd.DataFrame,
    df_crowdtruth_workers: pd.DataFrame,
    df_crowdtruth_units: pd.DataFrame,
) -> Dict[str, Figure]:
    """
    Analyzes worker demographics and returns a dictionary of Plotly bar plots.

    Args:
        df_prolific_workers: DataFrame containing worker information.

    Returns:
        Dictionary with keys
    """
    # Generate figures for worker performance analysis
    figs_performance = {
        "time_taken_per_task": time_taken_per_task(df_prolific_workers),
        "prolific_scores": prolific_scores(df_prolific_workers),
        "worker_quality_score": worker_quality_score(df_crowdtruth_workers),
        "mean_wqs_per_batch": mean_wqs_per_batch(
            df_crowdtruth_judgments, df_crowdtruth_workers, df_crowdtruth_units
        ),
    }

    # Save figures as images
    for key, fig in figs_performance.items():
        fig.write_image(
            f"{DIR_IMAGES}/workers_performance_{key}.png",
            width=800,
            height=600,
        )

    return figs_performance
