import argparse
import logging
import sys

from datetime import datetime

import milestones
from milestones.excel import load_f2due_pmcs_excel
from milestones.utility import get_pmcs_path_months


def parse_args():
    default_wbs = "02C"

    parser = argparse.ArgumentParser(description="Prepare DM milestone summaries.")
    parser.add_argument(
        "--pmcs-data",
        help=f"Path to PMCS Excel extract; default={milestones.get_latest_pmcs_path()}",
        default=milestones.get_latest_pmcs_path(),
    )
    parser.add_argument(
        "--local-data",
        help=f"Path to local annotations; default={milestones.get_local_data_path()}.",
        default=milestones.get_local_data_path(),
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)

    subparsers = parser.add_subparsers(title="Output targets")

    # Celeb uses fdue forecast date
    celeb = subparsers.add_parser("celeb", help="Generate celebratory milestones.")
    celeb.add_argument("--output", help="Filename for output", default="milestones.rst")
    celeb.add_argument("--pmcs-comp", help="Filename for PMCS compare")
    celeb.add_argument("--inc", help="Top or Y", default="Top")
    celeb.set_defaults(func=milestones.celeb)

    gantt = subparsers.add_parser("gantt", help="Generate Gantt chart.")
    gantt.add_argument(
        "--embedded",
        help="Format for embedding in another document",
        action="store_true",
    )
    gantt.add_argument("--output", help="Filename for output", default="gantt.tex")
    gantt.set_defaults(func=milestones.gantt)

    burndown = subparsers.add_parser(
        "burndown", help="Generate milestone burndown chart."
    )
    filename, burndown_start, burndown_end = "burndown.png", "2016-10-30", "2024-06-30"
    burndown.add_argument(
        "--start-date",
        type=datetime.fromisoformat,
        default=burndown_start,
        help=(
            f"Start date for the burndown chart (YYYY-MM-DD); "
            f"default={burndown_start}."
        ),
    )
    burndown.add_argument(
        "--end-date",
        type=datetime.fromisoformat,
        default=burndown_end,
        help=f"Start date for the burndown chart (YYYY-MM-DD); default={burndown_end}.",
    )
    burndown.add_argument(
        "--output", help="Filename for output; default={filename}.", default=filename
    )
    burndown.set_defaults(func=milestones.burndown)
    burndown.add_argument(
        "--prefix", help="List of prefixes for burndown milestones.",
        default="DM- DLP- LDM-503-"
    )
    burndown.add_argument(
        "--months", help="Specify number of months prior to use as forecast",
        type=int, default=0
    )

    csv = subparsers.add_parser(
        "csv", help="Generate a CSV version of the milestone schedule."
    )
    filename = "milestones.csv"
    csv.add_argument(
        "--output", help=f"Filename for output; default={filename}.", default=filename
    )
    csv.set_defaults(func=milestones.csv)

    jira = subparsers.add_parser("jira", help="Sync milestone details to Jira.")
    jira.set_defaults(func=milestones.cjira)

    remaining = subparsers.add_parser(
        "remaining", help="Print a list of remaining milestones."
    )
    as_of = datetime.now().isoformat()
    remaining.add_argument(
        "--wbs",
        default=default_wbs,
        help=f"Include only milestones for this WBS; default={default_wbs}",
    )
    remaining.set_defaults(func=milestones.remaining)

    delayed = subparsers.add_parser(
        "delayed", help="Print a list of delayed milestones."
    )
    as_of = datetime.now().isoformat()
    delayed.add_argument(
        "--wbs",
        default=default_wbs,
        help=f"Include only milestones for this WBS; default={default_wbs}",
    )
    delayed.add_argument(
        "--as-of",
        type=datetime.fromisoformat,
        default=as_of,
        help=f"Print incomplete milestones due by this date; default={as_of}",
    )
    delayed.set_defaults(func=milestones.delayed)

    predecessors = subparsers.add_parser(
        "predecessors", help="List each milestone with its predecessors"
    )
    predecessors.set_defaults(func=milestones.predecessors)

    graph = subparsers.add_parser(
        "graph", help="Generate Graphviz dot showing milestone relationships."
    )
    graph.add_argument("--output", help="Filename for output", default="graph.dot")
    graph.add_argument(
        "--wbs",
        default=default_wbs,
        help=f"Include only milestones for this WBS; default={default_wbs}",
    )
    graph.set_defaults(func=milestones.graph)

    #  RHL blockchart
    blockschedule = subparsers.add_parser(
        "blockschedule", help="Generate the summry block schedule."
    )
    blockschedule.add_argument("--output", help="Filename for output",
                               default="blockschedule.pdf")
    blockschedule.set_defaults(func=milestones.blockschedule)

    args = parser.parse_args()

    log_levels = [logging.WARN, logging.INFO, logging.DEBUG, logging.NOTSET]
    logging.basicConfig(level=log_levels[args.verbose])

    if not hasattr(args, "func"):
        parser.print_usage()
        sys.exit(1)
    return args


if __name__ == "__main__":
    args = parse_args()
    print("Working with "+args.pmcs_data)
    load_tasks = (args.func == milestones.blockschedule)
    milestones = milestones.load_milestones(args.pmcs_data, args.local_data,
                                            load_tasks)
    if "months" in args and args.months > 0:
        fpath = get_pmcs_path_months(args.pmcs_data, args.months)
        load_f2due_pmcs_excel(fpath, milestones)

    args.func(args, milestones)
