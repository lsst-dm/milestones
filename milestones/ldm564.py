from io import StringIO

from . import GANTT_MILESTONES
from .gantt import generate_gantt_embedded
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
                    "\item{{{code}: {name} \\textit{{(Due: {due}"))
                if prems.completed:
                    output.write("; completed {}".format(
                                 prems.completed.strftime("%Y-%m-%d")))
                else:
                    output.write("; currently incomplete")
                output.write(")}}\n")
            output.write("\\end{itemize}\n")
    return output.getvalue()

def milestone_map(mc):
#    for ms in sorted(mc.filter("LDM-503"), key=lambda x: (x.due, x.code)):
#        predecessors = [prems for prems in mc.filter("DM-")
#                        if prems.code in ms.predecessors]
#        for prems in sorted(predecessors, key=lambda x: (x.due, x.code)):
#            print(ms.code + " : " + prems.code)
    preds = set()
    import pandas as pd
    from datetime import datetime
    cutoff = datetime(2017,11,2)
    for ms in mc.filter("DM-"):
        if ms.due < cutoff or (ms.completed and ms.completed < cutoff):
            next
        else:
            preds.add(ms)
    for ms in mc.filter("DLP-"):
        if ms.due < cutoff or (ms.completed and ms.completed < cutoff):
            next
        else:
            preds.add(ms)
    for ms in mc.filter("LDM-503"):
        preds.add(ms)

#        preds.update(prems for prems in mc.filter("DM-")
#                     if prems.code in ms.predecessors and prems.due > datetime(2017, 11, 2))
#        preds.add(ms)
    month_ends = pd.date_range('2017-10-01','2022-06-01' , freq='1M')
#    for ms in preds:
#        if ms.completed and ms.completed < datetime(2017,11,30):
#            ms.completed = datetime(2017,11,30)
    model = []
    actual = []
    for me in month_ends:
        model_remain = actual_remain = len(preds)
        for ms in preds:
            if ms.due <= me:
                model_remain -= 1
            if ms.completed and ms.completed <= me:
#                print(me, ms)
                actual_remain -= 1
#            if ms.completed and ms.completed <= me:
#                print("Done", ms)
#                actual_done -= 1
#        print(me, model_remain, actual_remain)#, actual_done)
        model.append(model_remain)
        actual.append(actual_remain)

    import matplotlib.pyplot as plt
    plt.plot(month_ends, model, label="Schedule")
    plt.plot(month_ends[:7], actual[:7], label="Achieved")
    plt.xlabel("Date")
    plt.ylabel("Open Milestones")
    plt.legend()
    plt.show()


#    print(sorted(preds, key=lambda x: (x.due, x.code)))
#    for ms in sorted(preds, key=lambda x: (x.due, x.code)):
#        print(ms, ms.due, ms.completed)

def generate(args, mc):
    if args.gantt:
        write_output(args.gantt, generate_gantt_embedded(mc))
    if args.releases:
        write_output(args.releases, generate_releases(mc))
    if args.map:
        milestone_map(mc)
