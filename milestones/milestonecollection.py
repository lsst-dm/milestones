import yaml
import sys

from datetime import datetime

from .excel import load_pmcs_excel

__all__ = ["MilestoneCollection"]

class MilestoneCollection(object):
    def __init__(self, milestones):
        self.milestones = milestones

    def filter(self, prefix=None):
        return set(ms for ms in self.milestones if ms.code.startswith(prefix))

    def for_wbs(self, wbs=None):
        return set(ms for ms in self.milestones if ms.wbs.startswith(wbs))

    @staticmethod
    def from_files(pmcs_filename, local_filename):
        print("Loading PMCS data from: {}".format(pmcs_filename))
        print("Loading local annotations from: {}".format(local_filename))
        milestones = load_pmcs_excel(pmcs_filename)

        with open(local_filename) as f:
            local = yaml.safe_load(f)
        for ms in milestones:
            if ms.code in local:
                for attribute in ["name", "description", "comment", "aka",
                                  "test_spec", "short_name"]:
                    if (hasattr(ms, attribute) and
                        ms.code in local and
                        attribute in local[ms.code]):
                        print(f"NOTE: overriding {attribute} on {ms.code}", file=sys.stderr)
                        setattr(ms, attribute, local[ms.code][attribute])
                try:
                    old_completion = ms.completed
                    if local[ms.code]["completed"] == "":
                        # Not completed afterall!
                        ms.completed = None
                    else:
                        setattr(ms, "completed",
                                datetime.strptime(local[ms.code]["completed"],
                                                  "%Y-%m-%d"))
                    print("NOTE: overriding completion date on %s (was %s, now %s)" %
                          (ms.code, old_completion, local[ms.code]['completed'] or "incomplete"))
                except KeyError:
                    pass
                if "jira" in local[ms.code]:
                    ms.jira = local[ms.code]["jira"]
                if "jira_testplan" in local[ms.code]:
                    ms.jira_testplan = local[ms.code]["jira_testplan"]
        return MilestoneCollection(milestones)
