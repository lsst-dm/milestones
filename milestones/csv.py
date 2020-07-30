from csv import DictWriter
from datetime import datetime, timedelta
from io import StringIO

from .utility import write_output

__all__ = ["csv"]

def csv(args, milestones):
    start = sorted(milestones, key=lambda x: x.due)[0].due
    end = sorted(milestones, key=lambda x: x.due)[-1].due

    def get_month_start(dt):
        return datetime(dt.year, dt.month, 1)

    def get_next_month(year, month):
        dt = datetime(year, month, 1) + timedelta(days=32)
        return dt.year, dt.month

    def get_month_end(dt):
        next_year, next_month = get_next_month(dt.year, dt.month)
        return (datetime(next_year, next_month, 1) - timedelta(seconds=1))

    milestone_map = {}
    current_date = get_month_start(start)
    while current_date <= get_month_end(end):
        milestone_map[current_date.strftime("%b %Y")] = []
        for milestone in milestones:
            if (milestone.due >= current_date and
                milestone.due <= get_month_end(current_date) and
                milestone.wbs.startswith("02C")):
                milestone_map[current_date.strftime("%b %Y")].append(milestone)

        new_year, new_month = get_next_month(current_date.year, current_date.month)
        current_date = datetime(new_year, new_month, 1)

    fieldnames = milestone_map.keys()

    output = StringIO()
    writer = DictWriter(output, fieldnames=milestone_map.keys())
    writer.writeheader()

    for i in range(max(len(val) for val in milestone_map.values())):
        to_write = {}
        for field in fieldnames:
            try:
                milestone = milestone_map[field][i]

                to_write[field] = "%s (%s%s)" % (
                    milestone.code, milestone.wbs,
                    " DONE" if milestone.completed else ""
                    )
            except:
                pass
        writer.writerow(to_write)
    write_output(args.output, output.getvalue())
