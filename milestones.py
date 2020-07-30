from datetime import datetime

import argparse
import logging
import sys

import milestones

def parse_args():
    default_wbs = "02C"

    parser = argparse.ArgumentParser(description="Prepare DM milestone summaries.")
    parser.add_argument("--pmcs-data", help="Path to PMCS Excel extract. "
                        "[Default={}]".format(milestones.get_latest_pmcs_path()),
                        default=milestones.get_latest_pmcs_path())
    parser.add_argument("--local-data", help="Path to local annotations. "
                        "[Default={}]".format(milestones.get_local_data_path()),
                        default=milestones.get_local_data_path())
    parser.add_argument('--verbose', '-v', action='count', default=0)

    subparsers = parser.add_subparsers(title="Output targets.")

    gantt = subparsers.add_parser("gantt", help="Generate Gantt chart.")
    gantt.add_argument("--embedded", help="Format for embedding in another document", action="store_true")
    gantt.add_argument("--output", help="Filename for output", default="gantt.tex")
    gantt.set_defaults(func=milestones.gantt)

    burndown = subparsers.add_parser("burndown", help="Generate milestone burndown chart.")
    filename, burndown_start, burndown_end = "burndown.png", "2016-10-30", "2022-06-30"
    burndown.add_argument("--start-date", type=datetime.fromisoformat, default=burndown_start,
                          help=f"Start date for the burndown chart (YYYY-MM-DD); default={burndown_start}.")
    burndown.add_argument("--end-date", type=datetime.fromisoformat, default=burndown_end,
                          help=f"Start date for the burndown chart (YYYY-MM-DD); default={burndown_end}.")
    burndown.add_argument("--output", help="Filename for output; default={filename}.", default=filename)
    burndown.set_defaults(func=milestones.burndown)

    csv = subparsers.add_parser("csv", help="Generate a CSV version of the milestone schedule.")
    filename = "milestones.csv"
    csv.add_argument("--output", help=f"Filename for output; default={filename}.",
                     default=filename)
    csv.set_defaults(func=milestones.csv)

    jira = subparsers.add_parser("jira", help="Sync milestone details to Jira.")
    jira.set_defaults(func=milestones.jira)

    delayed = subparsers.add_parser("delayed", help="Print a list of delayed milestones.")
    as_of = datetime.now().isoformat()
    delayed.add_argument("--wbs", default=default_wbs,
                       help=f"Include only milestones for this WBS; default={default_wbs}")
    delayed.add_argument("--as-of", type=datetime.fromisoformat, default=as_of,
                         help=f"Print incomplete milestones due by this date; default={as_of}")
    delayed.set_defaults(func=milestones.delayed)

    predecessors = subparsers.add_parser("predecessors", help="List each milestone with its predecessors")
    predecessors.set_defaults(func=milestones.predecessors)

    ldm564 = subparsers.add_parser("ldm564", help="Generate inserts for LDM-564.")
    releases_location, gantt_location = "featurelist.tex", "gantt.tex"
    ldm564.add_argument("--releases-location", default=releases_location,
                        help=f"Ouput location for release feature list; default={releases_location}.")
    ldm564.add_argument("--gantt-location", default=gantt_location,
                        help=f"Ouput location for milestone table; default={gantt_location}.")
    ldm564.set_defaults(func=milestones.ldm564)

    graph = subparsers.add_parser("graph", help="Generate Graphviz dot showing milestone relationships.")
    graph.add_argument("--output", help="Filename for output", default="graph.dot")
    graph.add_argument("--wbs", default=default_wbs,
                       help=f"Include only milestones for this WBS; default={default_wbs}")
    graph.set_defaults(func=milestones.graph)

    args = parser.parse_args()

    log_levels = [logging.WARN, logging.INFO, logging.DEBUG, logging.NOTSET]
    logging.basicConfig(level=log_levels[args.verbose])

    if not hasattr(args, "func"):
        parser.print_usage()
        sys.exit(1)
    return args

if __name__ == "__main__":
    args = parse_args()
    milestones = milestones.load_milestones(args.pmcs_data, args.local_data)
    args.func(args, milestones)
