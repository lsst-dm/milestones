from datetime import datetime
from io import StringIO

__all__ = ["GANTT_MILESTONES", "format_gantt"]

# Milestones with these prefixes are included when generating Gantt charts.
# Note that some are not DM milestones, but are included for context.
GANTT_MILESTONES = [
    "LDM-503",
    "LSST-1200",
    "T&SC-1100-0900",
    "COMC-1264",
    "CAMM6995",
    "LSST-1220",
    "T&SC-1150-0600",
    "LSST-1510",
    "LSST-1513",
    "COMC-1664",
    "LSST-1520",
    "LSST-1540",
    "LSST-1560",
    "LSST-1620"
]

GANTT_PREAMBLE_EMBEDDED = """
\\begin{ganttchart}[
    expand chart=\\textwidth,
    title label font=\\sffamily\\bfseries,
    milestone label font=\\scriptsize,
    progress label text={#1},
    milestone progress label node/.append style={right=0.9cm},
    y unit chart=0.5cm,
    y unit title=0.8cm
]{1}{115}
  \\gantttitle{}{6} \\gantttitle{2018}{12} \\gantttitle{2019}{12}
  \\gantttitle{2020}{12} \\gantttitle{2021}{12} \\gantttitle{2022}{12}
  \\gantttitle{Operations}{49} \\
  \\ganttnewline\n
"""

GANTT_POSTAMBLE_EMBEDDED = """
\\end{ganttchart}
"""

def generate_gantt_embedded(mc):
    milestones = set()
    for ms in GANTT_MILESTONES:
        milestones = milestones.union(mc.filter(ms))
    return format_gantt(sorted(milestones, key=lambda x: (x.due, x.code)),
                        GANTT_PREAMBLE_EMBEDDED, GANTT_POSTAMBLE_EMBEDDED)

def format_gantt(milestones, preamble, postamble, start=datetime(2017, 7, 1)):
    def get_month_number(start, date):
        # First month is month 1; all other months sequentially.
        return 1 + (date.year * 12 + date.month) - (start.year * 12 + start.month)
    def get_milestone_name(code):
        return code.lower().replace("-", "").replace("&", "")

    output = StringIO()
    output.write(preamble)

    for ms in sorted(milestones, key=lambda x: x.due):
        ms_uniq_id = get_milestone_name(ms.code)
        output.write(ms.format_template("\\ganttmilestone[name={ms_uniq_id},progress label text={short_name}\\phantom{{#1}},progress=100]{{{code}}}{{{month_no}}} \\ganttnewline\n",
                                        ms_uniq_id=ms_uniq_id, month_no=get_month_number(start, ms.due)))
    for ms in sorted(milestones, key=lambda x: x.due):
        for succ in ms.successors:
            if succ in [milestone.code for milestone in milestones]:
                output.write("\\ganttlink{{{}}}{{{}}}\n".format(
                    get_milestone_name(ms.code), get_milestone_name(succ)))

    output.write(postamble)
    return output.getvalue()
