import argparse
import sys

import milestones
import milestones.standalone
import milestones.ldm503
import milestones.ldm564

def parse_args():
    parser = argparse.ArgumentParser(description="Prepare DM milestone summaries.")
    parser.add_argument("--pmcs-data", help="Path to PMCS Excel extract. "
                        "[Default={}]".format(milestones.get_latest_pmcs_path()),
                        default=milestones.get_latest_pmcs_path())
    parser.add_argument("--local-data", help="Path to local annotations. "
                        "[Default={}]".format(milestones.get_local_data_path()),
                        default=milestones.get_local_data_path())

    # We'll use a separate sub-parser for each document we're targeting.
    # Ideally, these would be plugins from the document packages themselves,
    # but for simplicity they are here for now.
    subparsers = parser.add_subparsers(title="Output targets.")

    standalone = subparsers.add_parser("standalone", help="Output standalone material.")
    standalone.add_argument("--gantt", help="Output location for Gantt chart.")
    standalone.add_argument("--burndown", help="Output location for burndown plot.")
    standalone.add_argument("--future", help="Output location for milestone forecast.")
    standalone.add_argument("--jira", action="store_true", help="Set due dates in Jira.")
    standalone.set_defaults(func=milestones.standalone.generate)

    ldm503 = subparsers.add_parser("ldm503", help="Output for LDM-503.")
    ldm503.add_argument("--table", help="Output location for milestone table.")
    ldm503.add_argument("--gantt", help="Output location for Gantt chart.")
    ldm503.add_argument("--commentary", help="Output location for milestone commentary.")
    ldm503.set_defaults(func=milestones.ldm503.generate)

    ldm564 = subparsers.add_parser("ldm564", help="Output for LDM-564.")
    ldm564.add_argument("--releases", help="Output location for summary of releases.")
    ldm564.add_argument("--gantt", help="Output location for Gantt chart.")
    ldm564.add_argument("--map", help="Dump milestone map to stdout.")
    ldm564.set_defaults(func=milestones.ldm564.generate)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    mc = milestones.MilestoneCollection.from_files(args.pmcs_data, args.local_data)
    try:
        args.func(args, mc)
    except AttributeError:
        print("Please select a supported target.")
        sys.exit(1)
