from datetime import datetime
from io import StringIO

__all__ = ["format_gantt"]

def format_gantt(milestones, preamble, postamble, start=datetime(2017, 7, 1)):
    def get_month_number(start, date):
        # First month is month 1; all other months sequentially.
        return 1 + (date.year * 12 + date.month) - (start.year * 12 + start.month)
    def get_milestone_name(code):
        return code.lower().replace("-", "").replace("&", "")

    output = StringIO()
    output.write(preamble)

    for ms in sorted(milestones, key=lambda x: x.due):
        ms_uniq_id = get_milestone_name(ms.code)
        output.write(ms.format_template("\\ganttmilestone[name={ms_uniq_id},progress label text={name}\\phantom{{#1}},progress=100]{{code}}{{month_no}} \\ganttnewline\n",
                                        ms_uniq_id=ms_uniq_id, month_no=get_month_number(start, ms.due)))
    for ms in sorted(milestones, key=lambda x: x.due):
        for succ in ms.successors:
            if succ in [milestone.code for milestone in milestones]:
                output.write("\\ganttlink{{{}}}{{{}}}\n".format(
                    get_milestone_name(ms.code), get_milestone_name(succ)))

    output.write(postamble)
    return output.getvalue()
