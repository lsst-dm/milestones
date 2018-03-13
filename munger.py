import argparse
import sys

import munger
import munger.standalone
import munger.ldm503

def parse_args():
    parser = argparse.ArgumentParser(description="Prepare DM milestone summaries.")
    parser.add_argument("--pmcs-data", help="Path to PMCS CSV extract. "
                        "[Default={}]".format(munger.get_latest_pmcs_path()),
                        default=munger.get_latest_pmcs_path())
    parser.add_argument("--local-data", help="Path to local annotations. "
                        "[Default={}]".format(munger.get_local_data_path()),
                        default=munger.get_local_data_path())

    # We'll use a separate sub-parser for each document we're targeting.
    # Ideally, these would be plugins from the document packages themselves,
    # but for simplicity they are here for now.
    subparsers = parser.add_subparsers(title="Output targets.")

    standalone = subparsers.add_parser("standalone", help="Output standalone material.")
    standalone.add_argument("--gantt", help="Output location for Gantt chart.")
    standalone.set_defaults(func=munger.standalone.generate)

    ldm503 = subparsers.add_parser("ldm503", help="Output for LDM-503.")
    ldm503.add_argument("--table", help="Output location for milestone table.")
    ldm503.add_argument("--gantt", help="Output location for Gantt chart.")
    ldm503.add_argument("--commentary", help="Output location for milestone commentary.")
    ldm503.set_defaults(func=munger.ldm503.generate)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    mc = munger.MilestoneCollection.from_files(args.pmcs_data, args.local_data)
    try:
        print(args)
        print(args.func(args, mc))
    except AttributeError:
        print("Please select a supported target.")
        sys.exit(1)

#    print(munger.format_gantt(mc.filter("LDM-503"), preamble=munger.GANTT_PREAMBLE_STANDALONE, postamble=munger.GANTT_POSTAMBLE_STANDALONE))
