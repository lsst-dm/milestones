from csv import DictWriter
from datetime import datetime, timedelta
from io import StringIO
from os import environ

import pandas as pd
import matplotlib.pyplot as plt
import requests

from .gantt import format_gantt, GANTT_MILESTONES
from .utility import write_output

__all__ = ["generate"]

GANTT_PREAMBLE = """
\\documentclass{article}
\\usepackage[
    paperwidth=30cm,
    paperheight=22.50cm,  % Manually tweaked to fit chart
    left=0mm,
    top=0mm,
    bottom=0mm,
    right=0mm,
    noheadfoot,
    marginparwidth=0pt,
    includemp=false
]{geometry}
\\usepackage{pgfgantt}
\\begin{document}
\\begin{center}
\\begin{ganttchart}[
%    vgrid,  % disabled for aesthetic reasons
%    hgrid,  % disabled for aesthetic reasons
    expand chart=0.98\\textwidth,
    title label font=\\sffamily\\bfseries,
    milestone label font=\\sffamily\\bfseries,
    progress label text={#1},
    milestone progress label node/.append style={right=2.2cm},
    milestone progress label font=\\sffamily,
    y unit chart=0.55cm,
    y unit title=0.8cm
]{1}{90}
  \\gantttitle{}{6} \\gantttitle{2018}{12} \\gantttitle{2019}{12}
  \\gantttitle{2020}{12} \\gantttitle{2021}{12} \\gantttitle{2022}{12}
  \\gantttitle{Operations}{24} \\
  \\ganttnewline\n
"""

GANTT_POSTAMBLE = """
\\end{ganttchart}
\\end{center}
\\end{document}
"""

def generate_gantt(mc):
    milestones = set()
    for ms in GANTT_MILESTONES:
        milestones = milestones.union(mc.filter(ms))
    return format_gantt(sorted(milestones, key=lambda x: (x.due, x.code)),
                        GANTT_PREAMBLE, GANTT_POSTAMBLE)

def dump_burndown(output, mc, start_date=None):
    # We won't consider milestones before which are due and/or completed
    # before the start date. The aim is to avoid picking up a whole bunch of
    # pre-replan milestones.
    if not start_date:
        start_date = datetime(2016, 10, 30)
    # Last date we'll consider.
    end_date = datetime(2022, 6, 30)

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
    plt.savefig(output)

def future(milestones):
    wbs = {milestone.wbs for milestone in milestones}
    start = sorted(milestones, key=lambda x: x.due)[0].due
    end = sorted(milestones, key=lambda x: x.due)[-1].due

    def get_month_start(dt):
        return datetime(dt.year, dt.month, 1)

    def get_next_month(year, month):
        dt = datetime(year, month, 1) + timedelta(days=32)
        return dt.year, dt.month

    def get_month_end(dt):
        next_year, next_month = get_next_month(dt.year, dt.month)
        return (datetime(next_year, next_month, 1) - timedelta(seconds=1))

    milestone_map = {}
    current_date = get_month_start(start)
    while current_date <= get_month_end(end):
        milestone_map[current_date.strftime("%b %Y")] = []
        for milestone in milestones:
            if (milestone.due >= current_date and
                milestone.due <= get_month_end(current_date) and
                milestone.wbs.startswith("02C")):
                milestone_map[current_date.strftime("%b %Y")].append(milestone)

        new_year, new_month = get_next_month(current_date.year, current_date.month)
        current_date = datetime(new_year, new_month, 1)

    fieldnames = milestone_map.keys()

    output = StringIO()
    writer = DictWriter(output, fieldnames=milestone_map.keys())
    writer.writeheader()

    for i in range(max(len(val) for val in milestone_map.values())):
        to_write = {}
        for field in fieldnames:
            try:
                milestone = milestone_map[field][i]

                to_write[field] = "%s (%s%s)" % (
                    milestone.code, milestone.wbs,
                    " DONE" if milestone.completed else ""
                    )
            except:
                pass
        writer.writerow(to_write)
    return output.getvalue()

def set_jira_due_dates(mc):
    def set_jira_due_date(issue_id, due_date):
        API_ENDPOINT = "https://jira.lsstcorp.org/rest/api/latest/"
        user, pw = environ["JIRA_USER"], environ["JIRA_PW"]
        formatted_date = due_date.strftime("%Y-%m-%d")
        data = {"fields": {"duedate": formatted_date}}
        print("Setting due date on", issue_id, "to", formatted_date)
        r = requests.put(API_ENDPOINT + "issue/" + issue_id,
                         auth=(user, pw), json=data)

    for ms in mc.milestones:
        if ms.jira and ms.due:
            set_jira_due_date(ms.jira, ms.due)
        elif ms.code.startswith("LDM-503"):
            if not ms.jira:
                print("WARNING: %s is not in Jira" % (ms.code,))
            if not ms.due:
                print("WARNING: %s has no due date" % (ms.code,))
        if ms.jira_testplan and ms.due:
            set_jira_due_date(ms.jira_testplan,
                              ms.due - timedelta(days=45))

def generate(args, mc):
    if args.gantt:
        write_output(args.gantt, generate_gantt(mc))
    if args.burndown:
        dump_burndown(args.burndown, mc)
    if args.future:
        write_output(args.future, future(mc.milestones))
    if args.jira:
        set_jira_due_dates(mc)
