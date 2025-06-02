import plotly.express as px

PLOTLY_COLORS = px.colors.qualitative.T10
DIR_IMAGES = "data/04_images"

CATEGORY_ORDERS = {
    "dominant_answer": ["agree", "disagree", "partially_agree", "uncertain"],
    "answer": ["agree", "disagree", "partially_agree", "uncertain"],
    "relation": ["intra-sentence", "inter-sentence"],
    "with_context": [False, True],
    "additional_sources": [False, True],
}
