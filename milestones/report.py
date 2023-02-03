from datetime import datetime

import matplotlib.pyplot as plt
from .utility import get_pmcs_path_months
from .excel import load_pmcs_excel

__all__ = ["report"]


def report(args, milestones):
    # Build a report with filtered milestones including last months due date
    # and n months prior due date
    # Format as per request
    # Milestone_Name	Expected_Date	Prior_Expected_Date	Delta_Days1	2xPrior_Expected_Date	Delta_Days1	Prior_Delta_Days1
    start_date = args.start_date

    prefixes = args.prefix.split()

    print(f"Report for milestones starting with {prefixes} using "
          f"{args.months} prior forcast")

    # The milestones will have loaded the 2 month already we need to get the 1 month
    fpath = get_pmcs_path_months(args.pmcs_data, 1)
    milestonesLastMonth = load_pmcs_excel(fpath, False)
    milestones = [
        ms
        for ms in milestones
        for prefix in prefixes
        if ms.code.startswith(prefix)
        and (ms.due and ms.due > start_date)
        and (not ms.completed or ms.completed > start_date)
    ]

    codes = [ms.code for ms in milestones]
    lmmap  = {}
    for mslm in milestonesLastMonth:
        if mslm.code in codes:
            lmmap[mslm.code]=mslm.fdue


    print("Code, Forecast end, Last Month, delta1 ,  2 Month, delta2")
    for ms in milestones:
        lmdue = lmmap[ms.code]
        if lmdue is None: # may be new with no prior
            lmdue = ms.fdue
        print(f"{ms.code},{ms.fdue.date()},{lmdue.date()},{(ms.fdue-lmdue).days}," 
              f"{ms.f2due.date()},{(ms.fdue-ms.f2due).days}")

