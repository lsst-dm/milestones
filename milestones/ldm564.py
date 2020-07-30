from io import StringIO

from .gantt import gantt_embedded
from .utility import write_output, escape_latex

__all__ = ["ldm564"]


def generate_releases(mc):
    output = StringIO()
    for ms in sorted([ms for ms in mc.milestones if ms.code.startswith("LDM-503")],
                     key=lambda x: (x.due, x.code)):
        output.write(f"\\subsection{{{escape_latex(ms.name)}: {escape_latex(ms.code)}}}\n")
        output.write("\\textit{")
        output.write(f"Due: {escape_latex(ms.due.strftime('%Y-%m-%d'))}; ")

        if ms.completed:
            output.write(f"completed {escape_latex(ms.completed.strftime('%Y-%m-%d'))}")
        else:
            output.write("currently incomplete")
        output.write(".}\n")

        predecessors = [prems for prems in mc.milestones
                        if prems.code.startswith("DM-")
                        and prems.code in ms.predecessors]

        if predecessors:
            output.write("\\begin{itemize}\n")
            for prems in sorted(predecessors, key=lambda x: (x.due, x.code)):
                output.write(f"\item{{{escape_latex(prems.code)}: {escape_latex(prems.name)} "
                             f"\\textit{{(Due: {escape_latex(prems.due.strftime('%Y-%m-%d'))}; ")

                if prems.completed:
                    output.write(f"completed {escape_latex(prems.completed.strftime('%Y-%m-%d'))}")
                else:
                    output.write("currently incomplete")

                output.write(")}}\n")
            output.write("\\end{itemize}\n")
        else:
            output.write("""\nNo new functionality is associated with this milestone, which """
                         """represents a refined or improved version of earlier deliveries.\n""")
    return output.getvalue()

def ldm564(args, mc):
    write_output(args.releases_location, generate_releases(mc))
    write_output(args.gantt_location, gantt_embedded(mc))
