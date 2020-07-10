from csv import DictWriter
from datetime import datetime, timedelta
from io import StringIO
from os import environ

import pandas as pd
import matplotlib.pyplot as plt
import requests

from .gantt import format_gantt, GANTT_MILESTONES
from .utility import write_output

__all__ = ["burndown"]

def burndown(args, mc):
    # We won't consider milestones before which are due and/or completed
    # before the start date. The aim is to avoid picking up a whole bunch of
    # pre-replan milestones.
    start_date, end_date = args.start_date, args.end_date

    milestones = set()
    for my_filter in ("DM-", "DLP-"):
        milestones.update(ms for ms in mc.filter(my_filter)
                          if ms.due > start_date and
                          (not ms.completed or ms.completed > start_date))
    milestones.update(mc.filter("LDM-503"))

    month_starts = []
    for year in (range(start_date.year, end_date.year+1)):
        for month in range(1, 13):
            dt = datetime(year, month, 1)
            if start_date <= dt <= end_date:
                month_starts.append(datetime(year, month, 1))

    model = []
    actual = []
    for date in month_starts:
        model_remain = actual_remain = len(milestones)
        for ms in milestones:
            if ms.due <= date:
                model_remain -= 1
            if ms.completed and ms.completed <= date:
                actual_remain -= 1
        model.append(model_remain)
        try:
            # We'll guess that the last month for which we have data is the
            # last month in whch at least one milestone was completed. This
            # isn't necessarily strictly correct, but it's not bad.
            if actual_remain < actual[-1]:
                last_achieved_month = date
        except IndexError:
            pass
        actual.append(actual_remain)

    plt.plot(month_starts, model, label="Baseline May 2019 ")

    # Dumped from running the code with old PMCS data.
    # Plotted for comparison purposes.
    bl2018 = [201, 196, 196, 196, 194, 194, 194, 186, 186, 185, 177, 175, 175,
              143, 140, 139, 139, 127, 127, 126, 115, 110, 109, 104, 98, 72,
              72, 68, 68, 66, 66, 63, 63, 61, 59, 51, 44, 42, 36, 34, 31, 31,
              31, 31, 31, 30, 27, 27, 22, 14, 14, 14, 14, 14, 14, 13, 12, 11,
              11, 9, 7, 4, 4, 4, 2, 2, 2, 2]

    plt.plot(month_starts, bl2018, label="Baseline June 2018")


    achieved_months = pd.date_range(start_date, last_achieved_month, freq='M')
    plt.plot(achieved_months, actual[:len(achieved_months)], label="Achieved")

    # Removed glide slope to make the plt less noisy.
#    glide_slope = [len(milestones) - i * (len(milestones) / len(month_starts)) for i in range(len(month_starts))]
#    plt.plot(month_starts, glide_slope, label="Glide slope")

    obsolete_ms = [
        "DLP-538", "DLP-541", "DLP-808", "DLP-799", "DLP-458", "DM-NCSA-5", "DM-NCSA-7"
    ]

    flat = [actual[len(achieved_months)] - len(obsolete_ms) for i in range(len(month_starts))]

    # Obsolete illustration, removed.
#    timescale = month_starts[len(achieved_months)-3:len(achieved_months)+2]
#    plt.plot(timescale, flat[:5], label="Corrected")

    plt.xlabel("Date")
    plt.ylabel("Open Milestones")
    plt.legend()
    plt.savefig(args.output)
