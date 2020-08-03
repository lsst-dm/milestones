from datetime import datetime
from io import StringIO

from .utility import write_output, escape_latex

__all__ = ["gantt", "gantt_embedded"]

# Milestones with these prefixes are included when generating Gantt charts.
# Note that some are not DM milestones, but are included for context.
GANTT_MILESTONES = [
    "LDM-503",
    "LSST-1200",
    "T&SC-1100-0900",
    #    "COMC-1264",
    #    "CAMM6995",  Dropped following LCR-1288.
    "LSST-1220",
    #    "T&SC-1150-0600",
    "LSST-1510",
    "LSST-1513",
    #    "COMC-1664",
    "LSST-1520",
    "LSST-1540",
    "LSST-1560",
    "LSST-1620",
]

GANTT_PREAMBLE_EMBEDDED = """
\\begin{ganttchart}[
    expand chart=\\textwidth,
    title label font=\\sffamily\\bfseries,
    milestone label font=\\scriptsize,
    progress label text={#1},
    milestone progress label node/.append style={right=1.4cm},
    y unit chart=0.4cm,
    y unit title=0.7cm
]{1}{125}
  \\gantttitle{}{6} \\gantttitle{2018}{12} \\gantttitle{2019}{12}
  \\gantttitle{2020}{12} \\gantttitle{2021}{12} \\gantttitle{2022}{12}
  \\gantttitle{2023}{12} \\gantttitle{Operations}{47} \\
  \\ganttnewline\n
"""

GANTT_POSTAMBLE_EMBEDDED = """
\\end{ganttchart}
"""

GANTT_PREAMBLE_STANDALONE = """
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
]{1}{102}
  \\gantttitle{}{6} \\gantttitle{2018}{12} \\gantttitle{2019}{12}
  \\gantttitle{2020}{12} \\gantttitle{2021}{12} \\gantttitle{2022}{12}
  \\gantttitle{2023}{12} \\gantttitle{Operations}{24} \\
  \\ganttnewline\n
"""

GANTT_POSTAMBLE_STANDALONE = """
\\end{ganttchart}
\\end{center}
\\end{document}
"""


def format_gantt(milestones, preamble, postamble, start=datetime(2017, 7, 1)):
    def get_month_number(start, date):
        # First month is month 1; all other months sequentially.
        return 1 + (date.year * 12 + date.month) - (start.year * 12 + start.month)

    def get_milestone_name(code):
        return code.lower().replace("-", "").replace("&", "")

    output = StringIO()
    output.write(preamble)

    for ms in sorted(milestones, key=lambda x: x.due):
        output_string = (
            f"\\ganttmilestone[name={get_milestone_name(ms.code)},"
            f"progress label text={ms.short_name}"
            f"\\phantom{{#1}},progress=100]{{{ms.code}}}"
            f"{{{get_month_number(start, ms.due)}}} \\ganttnewline\n"
        )
        output.write(escape_latex(output_string))

    for ms in sorted(milestones, key=lambda x: x.due):
        for succ in ms.successors:
            if succ in [milestone.code for milestone in milestones]:
                output.write(
                    "\\ganttlink{{{}}}{{{}}}\n".format(
                        get_milestone_name(ms.code), get_milestone_name(succ)
                    )
                )

    output.write(postamble)
    return output.getvalue()


def gantt_standalone(milestones):
    milestones = [
        ms
        for ms in milestones
        for gantt in GANTT_MILESTONES
        if ms.code.startswith(gantt)
    ]
    return format_gantt(
        sorted(milestones, key=lambda x: (x.due, x.code)),
        GANTT_PREAMBLE_STANDALONE,
        GANTT_POSTAMBLE_STANDALONE,
    )


def gantt_embedded(milestones):
    milestones = [
        ms
        for ms in milestones
        for gantt in GANTT_MILESTONES
        if ms.code.startswith(gantt)
    ]
    return format_gantt(
        sorted(milestones, key=lambda x: (x.due, x.code)),
        GANTT_PREAMBLE_EMBEDDED,
        GANTT_POSTAMBLE_EMBEDDED,
    )


def gantt(args, milestones):
    if args.embedded:
        tex_source = gantt_embedded(milestones)
    else:
        tex_source = gantt_standalone(milestones)
    write_output(args.output, tex_source)
