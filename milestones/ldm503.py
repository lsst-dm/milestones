from io import StringIO

from .gantt import gantt_embedded
from .utility import write_output, escape_latex

__all__ = ["ldm503"]

def generate_table(milestones):
    output = StringIO()
    for ms in sorted([ms for ms in milestones if ms.code.startswith("LDM-503")],
                     key=lambda x: (x.due, x.code)):
        output.write(f"{escape_latex(ms.code)} &\n")
        output.write(f"{escape_latex(ms.due.strftime('%Y-%m-%d'))} &\n")
        output.write("NCSA &\n")
        output.write(f"{escape_latex(ms.name)} \\\\\n\n")
    return output.getvalue()

def generate_commentary(milestones):
    output = StringIO()
    for ms in sorted([ms for ms in milestones if ms.code.startswith("LDM-503")],
                     key=lambda x: (x.due, x.code)):
        output.write(f"\\subsection{{{escape_latex(ms.name)} (\\textbf{{{escape_latex(ms.code)}}})}}\n")
        output.write(f"\\label{{{escape_latex(ms.code)}}}\n\n")
        output.write("\\subsubsection{Execution Procedure}\n\n")
        if ms.test_spec:
            output.write(f"This text will be executed following the procedure "
                         f"defined in {escape_latex(ms.test_spec)}.\n\n")
        else:
            output.write("The execution procedure for this test is "
                         "currently unspecified.\n\n")
        output.write("\\subsubsection{Description}\n\n")
        output.write(f"{escape_latex(ms.description)}\n\n")
        if ms.comment:
            output.write("\\subsubsection{Comments}\n\n")
            output.write(f"{escape_latex(ms.comment)}\n\n")
    return output.getvalue()

def ldm503(args, milestones):
    write_output(args.table_location, generate_table(milestones))
    write_output(args.text_location, generate_commentary(milestones))
    write_output(args.gantt_location, gantt_embedded(milestones))
