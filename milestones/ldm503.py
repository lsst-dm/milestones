from io import StringIO

from .gantt import generate_gantt_embedded
from .utility import write_output

__all__ = ["generate"]

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
        write_output(args.gantt, generate_gantt_embedded(mc))
    if args.table:
        write_output(args.table, generate_table(mc))
    if args.commentary:
        write_output(args.commentary, generate_commentary(mc))
