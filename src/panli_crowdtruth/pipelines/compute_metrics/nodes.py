from typing import Dict

import crowdtruth
import pandas as pd
from crowdtruth.configuration import DefaultConfig


def fix_annotations(results: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Fixes the answer_value in annotations based on judgments (workaround
    for bug in CrowdTruth).

    Args:
        results: Results dictionary from CrowdTruth.

    Returns:
        Fixed results dictionary from CrowdTruth.
    """
    results["annotations"]["output.answer_value"] = 0

    for idx in results["judgments"].index:
        for k, v in results["judgments"]["output.answer_value"][idx].items():
            if v > 0:
                results["annotations"].loc[k, "output.answer_value"] += 1

    results["annotations"] = results["annotations"].sort_values(
        by=["aqs"], ascending=False
    )
    return results


def compute_crowdtruth_metrics(
    data: Dict[str, pd.DataFrame], config: DefaultConfig
) -> Dict[str, pd.DataFrame]:
    """
    Computes the CrowdTruth metrics.

    Args:
        data: Preprocessed input data.
        config: Configuration for CrowdTruth.

    Returns:
        Units, workers, annotations, judgments, jobs
    """

    # Compute CrowdTruth metrics
    results = crowdtruth.run(data, config)

    # Fixes in annotations (workaround for bug in CrowdTruth)
    results = fix_annotations(results)

    return (
        results["units"],
        results["workers"],
        results["annotations"],
        results["judgments"],
        results["jobs"],
    )
