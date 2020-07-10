from io import StringIO

from .gantt import gantt_embedded
from .utility import write_output

__all__ = ["ldm503"]

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
        output.write("\\subsubsection{Execution Procedure}\n\n")
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

def ldm503(args, mc):
    write_output(args.table_location, generate_table(mc))
    write_output(args.text_location, generate_commentary(mc))
    write_output(args.gantt_location, gantt_embedded(mc))
