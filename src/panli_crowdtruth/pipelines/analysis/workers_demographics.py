from typing import Dict

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from panli_crowdtruth.pipelines.analysis.config_plotly import DIR_IMAGES, PLOTLY_COLORS


def replace_by_other(row, column_name="fluent_language", threshold=4):
    # Replace language with "Other" if the number of workers is below the threshold
    if row["n_workers"] < threshold:
        return "Other"
    else:
        return row[column_name]


def plot_employment_status(
    df_prolific_workers: pd.DataFrame,
) -> px.pie:
    """
    Generates a pie chart visualizing the distribution of employment status in the
    provided DataFrame. This function standardizes and formats employment status
    labels for improved display, counts the occurrences of each employment status,
    and creates a Plotly pie chart showing the proportion of each status.

    Args:
        df_prolific_workers: DataFrame containing an "Employment Status" column
            with employment status labels.

    Returns:
        px.pie: A Plotly pie chart figure object representing the employment
            status distribution.
    """
    # Dictionary to standardize and format employment status labels for better display
    to_replace = {
        "Not in paid work (e.g. homemaker', 'retired or disabled)": (
            "Not in paid work (e.g.<br>" "homemaker, retired<br>" "or disabled)"
        ),
        "Not in paid work (e.g. homemaker, retired or disabled)": (
            "Not in paid work (e.g.<br>" "homemaker, retired<br>" "or disabled)"
        ),
        "Due to start a new job within the next month": (
            "Due to start a new job<br>" "within the next month"
        ),
        "Unemployed (and job seeking)": ("Unemployed<br>" "(and job seeking)"),
    }

    # Make a copy to avoid modifying the original DataFrame
    df_employment = df_prolific_workers.copy()
    # Replace employment status values using the mapping above
    df_employment["Employment Status"] = df_employment["Employment Status"].replace(
        to_replace
    )
    # Count occurrences of each employment status
    df_employment = df_employment["Employment Status"].value_counts().to_frame("count")

    # Create a pie chart of employment status distribution
    fig = px.pie(
        df_employment,
        values="count",
        names=df_employment.index,
        color_discrete_sequence=PLOTLY_COLORS,
    )

    return fig


def plot_nationalities(
    df_prolific_workers: pd.DataFrame,
) -> px.pie:
    """
    Generates a pie chart showing the distribution of participants' nationalities.
    Nationalities with fewer than 20 workers are grouped into an "Other" category.

    Args:
        df_prolific_workers: DataFrame containing worker information

    Returns:
        px.pie: A Plotly pie chart figure object representing the distribution of
            participants' nationalities.
    """
    # Group by 'Nationality' and count unique workers per nationality
    df_nationalities = (
        df_prolific_workers.groupby("Nationality")["worker_id"]
        .nunique()
        .to_frame("n_workers")
        .reset_index()
    )

    # Replace nationalities with fewer than 20 workers with "Other"
    df_nationalities["Nationality"] = df_nationalities.apply(
        replace_by_other,
        args=(
            "Nationality",
            20,
        ),
        axis=1,
    )

    # Create pie chart of nationalities
    fig = px.pie(
        df_nationalities,
        values="n_workers",
        names="Nationality",
        color_discrete_sequence=PLOTLY_COLORS,
    )
    return fig


def plot_age(df_prolific_workers: pd.DataFrame) -> px.histogram:
    """
    Generates a histogram of the ages of participants, excluding outliers (ages >= 100).

    Args:
        df_prolific_workers: input dataframe containing worker information,
            including an 'age' column

    Returns:
        px.histogram: Plotly histogram object showing the distribution of ages.
    """
    # Filter out outlier ages (age >= 100)
    df_age = df_prolific_workers[df_prolific_workers.age < 100]

    # Create a histogram of ages with a marginal box plot
    fig = px.histogram(
        df_age,
        x="age",
        marginal="box",  # show a box plot on top of the histogram
        color_discrete_sequence=PLOTLY_COLORS,
    )

    # Update layout: set y-axis title and bar group gap
    fig.update_layout(
        yaxis_title="participants (n)",
        bargroupgap=0.1,  # gap between bars of the same location coordinates
    )

    return fig


def plot_fluent_languages(df_prolific_workers: pd.DataFrame) -> px.bar:
    """
    Generates a bar plot showing the number of unique workers per fluent language,
    excluding English, and groups languages with fewer than a specified threshold
    of workers into an "Other" category.

    Args:
        df_prolific_workers: input dataframe containing worker information, including a
            column 'Fluent languages'

    Returns:
        px.bar: Plotly bar plot object showing the number of workers per fluent
            language.
    """

    # Split the 'Fluent languages' column into lists (if not already)
    df_prolific_workers["Fluent languages"] = df_prolific_workers[
        "Fluent languages"
    ].apply(lambda x: x.split(", ") if isinstance(x, str) else x)
    # Explode the lists so each language gets its own row
    df_fluent = df_prolific_workers.explode("Fluent languages").rename(
        columns={"Fluent languages": "fluent_language"}
    )
    # Count unique workers per language
    df_fluent_workers = (
        df_fluent.groupby("fluent_language")["worker_id"]
        .nunique()
        .to_frame("n_workers")
        .reset_index()
    )
    # Exclude English from the results
    df_fluent_workers = df_fluent_workers[
        df_fluent_workers.fluent_language != "English"
    ]
    # Replace languages with fewer than 5 workers with "Other"
    df_fluent_workers["fluent_language"] = df_fluent_workers.apply(
        replace_by_other, args=("fluent_language", 5), axis=1
    )
    # Group again to sum up "Other" and sort by number of workers
    df_fluent_workers = (
        df_fluent_workers.groupby("fluent_language")["n_workers"]
        .sum()
        .to_frame()
        .reset_index()
        .sort_values("n_workers", ascending=False)
    )

    # Create bar plot
    fig = px.bar(
        df_fluent_workers,
        x="fluent_language",
        y="n_workers",
        color_discrete_sequence=PLOTLY_COLORS,
    )

    # Set axis titles
    fig.update_layout(
        xaxis_title="fluent language",
        yaxis_title="participants (n)",
    )

    return fig


def analyse_demographics(df_prolific_workers: pd.DataFrame) -> Dict[str, Figure]:
    """
    Generates demographic visualizations for the provided DataFrame of Prolific workers.

    Args:
        df_prolific_workers: DataFrame containing worker information.

    Returns:
        Dict[str, px.Figure]: A dictionary containing Plotly figures for various
            demographic visualizations, including employment status, nationalities,
            age distribution, and fluent languages.
    """

    # Generate demographic visualizations
    figs_demographics = {
        "fig_employment_status": plot_employment_status(df_prolific_workers),
        "fig_nationalities": plot_nationalities(df_prolific_workers),
        "fig_age": plot_age(df_prolific_workers),
        "fig_fluent_languages": plot_fluent_languages(df_prolific_workers),
    }

    # Save figures as images
    for key, fig in figs_demographics.items():
        fig.write_image(
            f"{DIR_IMAGES}/workers_demographics_{key}.png",
            width=800,
            height=600,
        )

    return figs_demographics
