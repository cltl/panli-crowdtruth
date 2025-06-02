from typing import Dict

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from plotly.graph_objects import Figure

from .config_plotly import DIR_IMAGES


def heatmap_correlation_labels(
    df_crowdtruth_judgments: pd.DataFrame, df_crowdtruth_units: pd.DataFrame
) -> Figure:
    """
    Create a heatmap of pairwise Pearson correlation coefficients between answers.
    The heatmap is based on the output.answer_value of the crowdtruth_judgments
    DataFrame.

    Args:
        df_crowdtruth_judgments: DataFrame containing crowdtruth judgments.
            Must contain columns 'unit', 'output.answer_value', and 'relation'.
        df_crowdtruth_units: DataFrame containing crowdtruth units.
            Must contain a 'relation' column.

    Returns:
        ff._figure.Figure: A Plotly figure object containing the heatmap.
    """
    # Merge the crowdtruth judgments with the units to get the relation
    df_crowdtruth_judgments = df_crowdtruth_judgments.merge(
        df_crowdtruth_units[["relation"]].reset_index(), on="unit", how="left"
    )

    # Group by unit and relation, count the occurrences of each answer value
    df = (
        df_crowdtruth_judgments.groupby(["unit", "relation"])["output.answer_value"]
        .value_counts()
        .to_frame("answer_count")
    )
    df = df.pivot_table("answer_count", "unit", "output.answer_value").fillna(0)

    # Get correlation matrix
    df_corr = df.corr()
    df_lt = df.corr().where(np.tril(np.ones(df.corr().shape)).astype(np.bool))

    # Create heatmap
    z = df_corr.values.tolist()
    z_text = np.around(z, decimals=2)  # Only show rounded value (full value on hover)
    labels = df_lt.columns.tolist()

    fig = ff.create_annotated_heatmap(
        z,
        annotation_text=z_text,
        colorscale="orrd",  # matter peach blues brwnyl orrd oranges
        hoverinfo="z",
        showscale=True,
        zmin=-1,
        zmax=1,
        x=labels,
        y=labels,
    )

    # Update layout
    fig.update_layout(
        yaxis_title="",
        xaxis_title="",
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
        ),
        plot_bgcolor="white",
        xaxis_side="bottom",
        xaxis_showgrid=False,
        yaxis_showgrid=False,
    )

    return fig


def analyse_annotations(
    df_crowdtruth_judgments: pd.DataFrame, df_crowdtruth_units: pd.DataFrame
) -> Dict[str, Figure]:
    """
    Analyse annotations by creating a heatmap of pairwise Pearson correlation
    coefficients.

    Args:
        df_crowdtruth_judgments: DataFrame containing crowdtruth judgments.
            Must contain columns 'unit', 'output.answer_value', and 'relation'.
        df_crowdtruth_units: DataFrame containing crowdtruth units.
            Must contain a 'relation' column.

    Returns:
        ff._figure.Figure: A Plotly figure object containing the heatmap.
    """
    figs_annotations = {
        "heatmap_correlation_labels": heatmap_correlation_labels(
            df_crowdtruth_judgments, df_crowdtruth_units
        )
    }

    for key, fig in figs_annotations.items():
        # Save the figure as an image
        fig.write_image(
            f"{DIR_IMAGES}/annotations_{key}.png",
            width=800,
            height=600,
        )

    return figs_annotations
