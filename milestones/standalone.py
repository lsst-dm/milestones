from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from .gantt import format_gantt, GANTT_MILESTONES
from .utility import write_output

__all__ = ["generate"]

GANTT_PREAMBLE = """
\\documentclass{article}
\\usepackage[
    paperwidth=30cm,
    paperheight=22.00cm,  % Manually tweaked to fit chart
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
        start_date = datetime(2017, 10, 31)
    # Last date we'll consider.
    end_date = datetime(2022, 5, 31)

    milestones = set()
    for my_filter in ("DM-", "DLP-"):
        milestones.update(ms for ms in mc.filter(my_filter)
                          if ms.due > start_date and
                          (not ms.completed or ms.completed > start_date))
    milestones.update(mc.filter("LDM-503"))

    month_ends = pd.date_range(start_date, end_date, freq='M')
    model = []
    actual = []
    for me in month_ends:
        model_remain = actual_remain = len(milestones)
        for ms in milestones:
            if ms.due <= me:
                model_remain -= 1
            if ms.completed and ms.completed <= me:
                actual_remain -= 1
        model.append(model_remain)
        try:
            # We'll guess that the last month for which we have data is the
            # last month in whch at least one milestone was completed. This
            # isn't necessarily strictly correct, but it's not bad.
            if actual_remain < actual[-1]:
                last_achieved_month = me
        except IndexError:
            pass
        actual.append(actual_remain)

    plt.plot(month_ends, model, label="Schedule")

    achieved_months = pd.date_range(start_date, last_achieved_month, freq='M')
    plt.plot(achieved_months, actual[:len(achieved_months)], label="Achieved")
    plt.xlabel("Date")
    plt.ylabel("Open Milestones")
    plt.legend()
    plt.savefig(output)

def generate(args, mc):
    if args.gantt:
        write_output(args.gantt, generate_gantt(mc))
    if args.burndown:
        dump_burndown(args.burndown, mc)
