from typing import Dict, Tuple

import crowdtruth
import pandas as pd
from crowdtruth.configuration import DefaultConfig


class BaseConfig(DefaultConfig):
    inputColumns = [
        "batch_id",
        "list_id",
        "pair_id",
        "sent_id",
        "statement_sent_ids",
        "n_sources",
        "sources",
        "sentence_predicate",
        "sentence",
        "sentence_statement",
        "statement",
        "sim",
        "source_index",
        "source_text",
        "true_answer",
    ]
    outputColumns = ["answer_value"]
    customPlatformColumns = [
        "judgment_id",
        "question_id",
        "worker_id",
        "started_time",
        "submitted_time",
    ]
    open_ended_task = False


class ConfigFourLabels(BaseConfig):
    annotation_vector = ["agree", "disagree", "partially_agree", "uncertain"]


class ConfigThreeLabels(BaseConfig):
    annotation_vector = ["entailment", "contradiction", "neutral"]

    def processJudgments(self, judgments):
        for col in self.outputColumns:
            judgments[col] = judgments[col].replace(
                {
                    "agree": "entailment",
                    "disagree": "contradiction",
                    "partially_agree": "neutral",
                    "uncertain": "neutral",
                }
            )
        return judgments


def prepare_crowdtruth_judgments(
    input_filepath: str, n_classes: int
) -> Tuple[Dict[str, pd.DataFrame], DefaultConfig]:
    """Preprocesses the input data before computing CrowdTruth metrics.

    Args:
        input_filepath: Path to input data.
        n_classes: Number of classes (3 or 4) in PANLI dataset.
    """
    # Determine config class
    if n_classes == 3:
        config_class = ConfigThreeLabels()
    elif n_classes == 4:
        config_class = ConfigFourLabels()
    else:
        raise ValueError(f"Unsupported number of classes: {n_classes}")

    # Load data with CrowdTruth
    data, config = crowdtruth.load(file=input_filepath, config=config_class)

    return data, config
