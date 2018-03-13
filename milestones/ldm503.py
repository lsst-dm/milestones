from io import StringIO

from . import GANTT_MILESTONES
from .gantt import format_gantt
from .utility import write_output

__all__ = ["generate"]

GANTT_PREAMBLE = """
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

GANTT_POSTAMBLE = """
\\end{ganttchart}
"""

def generate_gantt(mc):
    milestones = set()
    for ms in GANTT_MILESTONES:
        milestones = milestones.union(mc.filter(ms))
    return format_gantt(sorted(milestones, key=lambda x: (x.due, x.code)),
                        GANTT_PREAMBLE, GANTT_POSTAMBLE)

def generate_table(mc):
    output = StringIO()
    for ms in sorted(mc.filter("LDM-503"), key=lambda x: (x.due, x.code)):
        output.write(ms.format_template("{code} &\n"))
        output.write(ms.format_template("{due} &\n"))
        output.write("NCSA &\n")
        output.write(ms.format_template("{name} \\\\\n\n"))
    return output.getvalue()

def generate_commentary(mc):
    output = StringIO()
    for ms in sorted(mc.filter("LDM-503"), key=lambda x: (x.due, x.code)):
        output.write(ms.format_template("\\subsection{{{name} "
                                        "(\\textbf{{{code}}})}}\n"))
        output.write(ms.format_template("\\label{{{code}}}\n\n"))
        output.write("\\subsubsection{Specification}\n\n")
        if ms.test_spec:
            output.write(ms.format_template("This test will be executed "
                                            "following the procedure defined "
                                            "in {test_spec}.\n\n"))
        else:
            output.write("The execution procedure for this test is "
                         "currently unspecified.\n\n")
        output.write("\\subsubsection{Description}\n\n")
        output.write(ms.format_template("{description}\n\n"))
        if ms.comment:
            output.write("\\subsubsection{Comments}\n\n")
            output.write(ms.format_template("{comment}\n\n"))
    return output.getvalue()

def generate(args, mc):
    if args.gantt:
        write_output(args.gantt, generate_gantt(mc))
    if args.table:
        write_output(args.table, generate_table(mc))
    if args.commentary:
        write_output(args.commentary, generate_commentary(mc))
