from typing import List
from analyser.report import Report
from collections import defaultdict, Counter


def calculate_hashtags_stats(reports: List[Report]) -> dict:
    stats_by_hashtags = defaultdict(list)
    for report in reports:
        stats_by_hashtags[report.approved].extend(report.normalised_hashtags)
    acc_stats = {True: Counter(stats_by_hashtags[True]),
                 False: Counter(stats_by_hashtags[False]),
                 None: Counter(stats_by_hashtags[None])}
    return acc_stats
