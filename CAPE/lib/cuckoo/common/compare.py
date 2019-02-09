# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import collections

from lib.cuckoo.common.constants import CUCKOO_ROOT
from modules.processing.behavior import ParseProcessLog

ANALYSIS_ROOT = os.path.join(CUCKOO_ROOT, "storage", "analyses")

def behavior_categories_percent(calls):
    catcounts = collections.defaultdict(lambda: 0)

    for call in calls:
        catcounts[call.get("category", "none")] += 1

    return dict(catcounts)

def combine_behavior_percentages(stats):
    # get all categories present
    cats = set()
    for v in stats.values():
        for v2 in v.values():
            cats |= set(v2.keys())

    sums = {}
    for tid in stats:
        sums[tid] = {}
        for cat in cats:
            sums[tid][cat] = sum(j.get(cat, 0) for j in stats[tid].values())

    totals = dict((k, sum(v.values())) for k, v in sums.items())

    percentages = {}
    for tid in stats:
        percentages[tid] = {}
        for cat in cats:
            percentages[tid][cat] = round(sums[tid][cat] * 1.0 / totals[tid] * 100, 2)

    return percentages

def iter_task_process_logfiles(tid):
    tpath = os.path.join(ANALYSIS_ROOT, str(tid), "logs")

    for fname in os.listdir(tpath):
        fpath = os.path.join(tpath, fname)
        pid = int(fname.split(".")[0])
        yield (pid, fpath)

def helper_percentages_storage(tid1, tid2):
    counts = {}

    for tid in [tid1, tid2]:
        counts[tid] = {}

        for pid, fpath in iter_task_process_logfiles(tid):
            ppl = ParseProcessLog(fpath)
            category_counts = behavior_categories_percent(ppl.calls)

            counts[tid][pid] = category_counts

    return combine_behavior_percentages(counts)

def helper_percentages_mongo(results_db, tid1, tid2, ignore_categories=["misc"]):
    counts = {}

    for tid in[tid1, tid2]:
        counts[tid] = {}

        pids_calls = results_db.analysis.find_one(
            {
                "info.id": int(tid),
            },
            {
                "behavior.processes.process_id": 1,
                "behavior.processes.calls": 1
            }
        )

        if not pids_calls:
            continue

        for pdoc in pids_calls["behavior"]["processes"]:
            pid = pdoc["process_id"]
            counts[tid][pid] = {}

            for coid in pdoc["calls"]:
                chunk = results_db.calls.find_one({"_id": coid}, {"calls.category": 1})
                category_counts = behavior_categories_percent(chunk["calls"])
                for cat, count in category_counts.items():
                    if cat in ignore_categories: continue
                    counts[tid][pid][cat] = counts[tid][pid].get(cat, 0) + count

    return combine_behavior_percentages(counts)

def helper_summary_mongo(results_db, tid1, tid2):
    summaries = dict()
    left_sum, right_sum = None, None
    left_sum = results_db.analysis.find_one({"info.id": int(tid1)},{"behavior.summary": 1})
    right_sum = results_db.analysis.find_one({"info.id": int(tid2)},{"behavior.summary": 1})
    if left_sum and right_sum:
        summaries = get_similar_summary(left_sum, right_sum)

    return summaries

def helper_percentages_elastic(es_obj, tid1, tid2, idx, ignore_categories=["misc"]):
    counts = {}

    for tid in [tid1, tid2]:
        counts[tid] = {}
        results = es_obj.search(
                          index=idx,
                          doc_type="analysis",
                          q="info.id: \"%s\"" % tid,
                      )["hits"]["hits"]
        if results:
            pids_calls = results[-1]["_source"]
        else:
            pids_calls = None

        if not pids_calls:
            continue

        for pdoc in pids_calls["behavior"]["processes"]:
            pid = pdoc["process_id"]
            counts[tid][pid] = {}

            for coid in pdoc["calls"]:
                chunk = es_obj.search(
                                index=idx,
                                doc_type="calls",
                                q="_id: \"%s\"" % coid,
                            )["hits"]["hits"][-1]["_source"]
                category_counts = behavior_categories_percent(chunk["calls"])
                for cat, count in category_counts.items():
                    if cat in ignore_categories: continue
                    counts[tid][pid][cat] = counts[tid][pid].get(cat, 0) + count

    return combine_behavior_percentages(counts)

def helper_summary_elastic(es_obj, tid1, tid2, idx):
    summaries = dict()
    left_sum, right_sum = None, None
    buf = es_obj.search(
                  index=idx,
                  doc_type="analysis",
                  q="info.id: \"%s\"" % tid1,
                 )["hits"]["hits"]
    if buf:
        left_sum = buf[-1]["_source"]

    buf = es_obj.search(
                  index=idx,
                  doc_type="analysis",
                  q="info.id: \"%s\"" % tid2,
                 )["hits"]["hits"]
    if buf:
        right_sum = buf[-1]["_source"]

    if left_sum and right_sum:
        summaries = get_similar_summary(left_sum, right_sum)

    return summaries

def get_similar_summary(left_sum, right_sum):
    ret = dict()
    for summary in left_sum["behavior"]["summary"]:
        for item in left_sum["behavior"]["summary"][summary]:
            if item in right_sum["behavior"]["summary"][summary]:
                if summary not in ret.keys():
                    ret[summary] = list()
                ret[summary].append(item)

    return ret
