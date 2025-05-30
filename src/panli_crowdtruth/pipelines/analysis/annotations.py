import numpy as np
import plotly.figure_factory as ff

from .write_images import write_images


def main(judgments, dir_images):
    df = (
        judgments.groupby(["unit", "relation"])["output.answer_value"]
        .value_counts()
        .to_frame("answer_count")
    )
    df = df.pivot_table("answer_count", "unit", "output.answer_value").fillna(0)
    df_corr = df.corr()
    df_lt = df.corr().where(np.tril(np.ones(df.corr().shape)).astype(np.bool))

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

    fig.update_layout(
        yaxis_title="",
        xaxis_title="",
        #     width=500,
        #     height=400,
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
        #     yaxis_autorange='reversed'
    )

    write_images(fig, dir_images, "heatmap_annotations")
