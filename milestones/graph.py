import html
import textwrap

from datetime import datetime
from io import StringIO

from .utility import write_output

__all__ = ["graph"]


def format_milestone(ms, my_wbs):
    attr_list = [
        "<br/>".join(
            textwrap.wrap(f"label=<{html.escape(ms.code)}: {html.escape(ms.name)}>", 25)
        )
    ]
    if ms.completed:
        attr_list.append("style=filled")
        attr_list.append("fillcolor=powderblue")
    elif ms.due < datetime.now():
        attr_list.append("style=filled")
        attr_list.append("fillcolor=orange")
    if not ms.wbs.startswith(my_wbs):
        attr_list.append("shape=rect")
    return f"  \"{ms.code}\" [{','.join(attr_list)}];\n"


def graph(args, milestones):
    dot_source = StringIO()
    dot_source.write("strict digraph {\n")
    seen = []
    for ms in milestones:
        if not ms.wbs.startswith(args.wbs):
            continue

        if ms.code not in seen:
            dot_source.write(format_milestone(ms, args.wbs))
            seen.append(ms.code)

        for candidate in milestones:
            if candidate.code in ms.predecessors or candidate.code in ms.successors:
                if candidate.code not in seen:
                    dot_source.write(format_milestone(candidate, args.wbs))
                    seen.append(candidate.code)
                if candidate.code in ms.predecessors:
                    dot_source.write(f'  "{candidate.code}" -> "{ms.code}";\n')
                if candidate.code in ms.successors:
                    dot_source.write(f'  "{ms.code}" -> "{candidate.code}";\n')
    dot_source.write("}")
    write_output(args.output, dot_source.getvalue(), comment_prefix="//")
