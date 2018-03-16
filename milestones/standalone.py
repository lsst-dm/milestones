from .gantt import format_gantt, GANTT_MILESTONES
from .utility import write_output

__all__ = ["generate"]

GANTT_PREAMBLE = """
\\documentclass{article}
\\usepackage[
    paperwidth=30cm,
    paperheight=19.20cm,  % Manually tweaked to fit chart
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

def generate(args, mc):
    if args.gantt:
        write_output(args.gantt, generate_gantt(mc))
