from io import StringIO

from . import GANTT_MILESTONES
from .gantt import format_gantt
from .utility import write_output

__all__ = ["generate"]

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
                    "\item{{{code}: {name} (\\textit{{Due: {due}}})}}\n"))
            output.write("\\end{itemize}\n")
    return output.getvalue()

def generate(args, mc):
    if args.releases:
        write_output(args.releases, generate_releases(mc))
