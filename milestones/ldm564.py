from io import StringIO

from .gantt import gantt_embedded
from .utility import write_output

__all__ = ["ldm564"]


def generate_releases(mc):
    output = StringIO()
    for ms in sorted(mc.filter("LDM-503"), key=lambda x: (x.due, x.code)):
        output.write(ms.format_template("\\subsection{{{name}: {code}}}\n"))
        output.write("\\textit{{")
        output.write(ms.format_template("Due: {due}; "))
        if ms.completed:
            output.write("completed {}".format(ms.completed.strftime("%Y-%m-%d")))
        else:
            output.write("currently incomplete")
        output.write(".}}\n")
        predecessors = [prems for prems in mc.filter("DM-")
                        if prems.code in ms.predecessors]
        if predecessors:
            output.write("\\begin{itemize}\n")
            for prems in sorted(predecessors, key=lambda x: (x.due, x.code)):
                output.write(prems.format_template(
                    "\item{{{code}: {name} \\textit{{(Due: {due}"))
                if prems.completed:
                    output.write("; completed {}".format(
                                 prems.completed.strftime("%Y-%m-%d")))
                else:
                    output.write("; currently incomplete")
                output.write(")}}\n")
            output.write("\\end{itemize}\n")
        else:
            output.write("""\nNo new functionality is associated with this milestone, which """
                         """represents a refined or improved version of earlier deliveries.\n""")
    return output.getvalue()

def ldm564(args, mc):
    write_output(args.releases_location, generate_releases(mc))
    write_output(args.gantt_location, gantt_embedded(mc))
