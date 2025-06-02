from typing import Dict

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from panli_crowdtruth.pipelines.analysis.config_plotly import (
    CATEGORY_ORDERS,
    DIR_IMAGES,
    PLOTLY_COLORS,
)


def histogram_overall_uqs(df_crowdtruth_units: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the overall unit quality score (UQS) for each unit in the DataFrame.

    Args:
        df_crowdtruth_units: DataFrame containing crowdtruth units.
            Must contain a 'uqs' column.

    Returns:
        pd.DataFrame: A DataFrame with the overall UQS for each unit.
    """
    # Calculate the mean of the unit quality scores
    fig = px.histogram(
        df_crowdtruth_units,
        x="uqs",
        marginal="box",
        color_discrete_sequence=PLOTLY_COLORS,
    )

    # update layout
    fig.update_layout(
        xaxis_title="uqs",
        yaxis_title="units (n)",
        autosize=False,
        width=600,
        height=400,
        margin=dict(
            l=2,
            r=2,
            b=1,
        ),
    )

    return fig


def violin_uqs_per_type(df_crowdtruth_units: pd.DataFrame) -> px.violin:
    """
    Create a violin plot to visualize the distribution of unit quality scores (UQS)
    per type (inta-sentence & inter-sentence) in the DataFrame.

    Args:
        df_crowdtruth_units: DataFrame containing crowdtruth units.
            Must contain 'uqs' and 'type' columns.

    Returns:
        px.violin: A Plotly violin plot showing the distribution of UQS per type.
    """
    # Create a violin plot to visualize the distribution of UQS per type
    fig = px.violin(
        df_crowdtruth_units,
        color="relation",
        x="uqs",
        category_orders=CATEGORY_ORDERS,
        color_discrete_sequence=px.colors.qualitative.T10,
        labels={"relation": ""},
        orientation="h",
        box=True,
    )

    # Update layout
    fig.update_layout(
        autosize=False,
        width=600,
        height=400,
        margin=dict(
            l=2,
            r=2,
            b=1,
            #         t=1,
        ),
        legend=dict(
            title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
    )

    # Update annotations to show only the type name
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    return fig


def boxplot_uqs_per_type_and_source(
    df_crowdtruth_units: pd.DataFrame,
) -> Figure:
    """
    Create a box plot to visualize the unit quality scores (UQS) faceted by type
    and source in the DataFrame.

    Args:
        df_crowdtruth_units: DataFrame containing crowdtruth units.
            Must contain 'uqs', 'relation', and 'source' columns.

    Returns:
        px.box: A Plotly box plot showing UQS faceted by type and source.
    """
    units = df_crowdtruth_units.copy()

    # Replace 'source' values with more descriptive names
    units["additional_sources"] = units["additional_sources"].replace(
        {True: "with additional sources", False: "without additional sources"}
    )
    # FIXME: somehow True/False still appear in plot

    # Create a box plot to visualize the unit quality scores (UQS) faceted by
    # type and source
    fig = px.box(
        units,
        x="dominant_answer",
        y="uqs",
        color="source_type",
        color_discrete_sequence=px.colors.qualitative.T10,
        category_orders=CATEGORY_ORDERS,
        orientation="v",
        labels={"dominant_answer": ""},
        facet_col="relation",
        facet_row="additional_sources",
    )

    # Update layout
    fig.update_layout(
        xaxis_title="",
        autosize=False,
        width=1000,
        height=600,
        legend=dict(
            title="",
        ),
        margin=dict(
            l=1,
            r=1,
            b=1,
        ),
    )

    # Update annotations to show only the type name
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    return fig


def scatter_correlation_uqs_similarity(df_crowdtruth_units: pd.DataFrame) -> px.scatter:
    """
    Create a scatter plot to visualize the correlation between unit quality scores (UQS)
    and similarity scores fpr inter-sentence relations in the DataFrame.

    Args:
        df_crowdtruth_units: DataFrame containing crowdtruth units.
            Must contain 'uqs' and 'similarity' columns.

    Returns:
        px.scatter: A Plotly scatter plot showing the correlation between UQS
            and similarity.
    """
    # Filter the DataFrame for inter-sentence relations
    units_inter = df_crowdtruth_units[df_crowdtruth_units.relation == "inter-sentence"]

    # Create a scatter plot to visualize the correlation between UQS and similarity
    fig = px.scatter(
        units_inter,
        x="input.sim",
        y="uqs",
        labels={"input.sim": "similarity", "dominant_aqs": "aqs"},
        color_discrete_sequence=px.colors.qualitative.T10,
        trendline="ols",
        trendline_color_override="#E45756",
        opacity=0.65,
        category_orders=CATEGORY_ORDERS,
        facet_row="dominant_answer",
    )

    # Update annotations to show only the type name
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    # Update layout
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        margin=dict(
            l=1,
            r=1,
            b=1,
        ),
    )

    return fig


def preprocess_units(df_crowdtruth_units: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame of crowdtruth units to add additional columns
    for analysis, such as 'with_context', 'source_type', and 'relation'.

    Args:
        df_crowdtruth_units: DataFrame containing crowdtruth units.

    Returns:
        pd.DataFrame: The preprocessed DataFrame with additional columns.
    """

    def _author_vs_additional_sources(row):
        if row["input.source_index"] == 0:
            return "author"
        else:
            return "additional_source"

    def _context(row):
        if row["relation"] == "inter-sentence":
            return True
        if row["input.true_answer"] == "agree":
            return False
        return True

    def _relation_sentence_statement(row):
        if row["input.sent_id"] in row["input.statement_sent_ids"]:
            return "intra-sentence"
        return "inter-sentence"

    units = df_crowdtruth_units.copy()

    # add column 'dominant_answer'
    units["dominant_answer"] = units["unit_annotation_score"].apply(
        lambda x: x.most_common()[0][0]
    )
    units["second_answer"] = units["unit_annotation_score"].apply(
        lambda x: x.most_common()[1][0]
    )
    units["dominant_aqs"] = units["unit_annotation_score"].apply(
        lambda x: x.most_common()[0][1]
    )

    # fillna for true_answer
    units["input.true_answer"] = units["input.true_answer"].fillna("unknown")
    units["context"] = units["input.true_answer"].replace(
        {"agree": True, "unknown": False}
    )

    # presence of additional sources
    units["additional_sources"] = units["input.n_sources"].apply(lambda x: x > 0)

    # Preprocess the DataFrame to add a 'with_context' column
    units["with_context"] = units.apply(_context, axis=1)

    # Preprocess the DataFrame to add a 'source_type' column
    units["source_type"] = units.apply(_author_vs_additional_sources, axis=1)

    # Preprocess the DataFrame to add a 'relation' column
    units["relation"] = units.apply(_relation_sentence_statement, axis=1)

    return units


def analyse_units(df_crowdtruth_units: pd.DataFrame) -> Dict[str, Figure]:
    """
    Generates visualizations for the provided DataFrame of crowdtruth units.

    Args:
        df_crowdtruth_units: DataFrame containing crowdtruth units.

    Returns:
        Dict[str, px.Figure]: A dictionary containing Plotly figures for various
            unit visualizations, including overall unit quality score (UQS).
    """
    # Preprocess the DataFrame to add additional columns for analysis
    df_crowdtruth_units = preprocess_units(df_crowdtruth_units)

    # Create figures for unit analysis
    figs_units = {
        "overall_uqs": histogram_overall_uqs(df_crowdtruth_units),
        "uqs_per_type": violin_uqs_per_type(df_crowdtruth_units),
        "uqs_per_type_and_source": boxplot_uqs_per_type_and_source(df_crowdtruth_units),
        "correlation_uqs_similarity": scatter_correlation_uqs_similarity(
            df_crowdtruth_units
        ),
    }

    # Save figures as images
    for key, fig in figs_units.items():
        fig.write_image(
            f"{DIR_IMAGES}/units_{key}.png",
            width=800,
            height=600,
        )

    return figs_units
