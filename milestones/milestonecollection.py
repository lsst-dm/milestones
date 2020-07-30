import yaml
import sys
import logging

from datetime import datetime

from .excel import load_pmcs_excel

__all__ = ["MilestoneCollection"]

class MilestoneCollection(object):
    def __init__(self, milestones):
        self.milestones = milestones

    def filter(self, prefix=None):
        return [ms for ms in self.milestones if ms.code.startswith(prefix)]

    def for_wbs(self, wbs=None):
        return [ms for ms in self.milestones if ms.wbs.startswith(wbs)]

    @staticmethod
    def from_files(pmcs_filename, local_filename):
        logger = logging.getLogger(__name__)

        logger.info(f"Loading PMCS data from: {pmcs_filename}")
        logger.info(f"Loading local annotations from: {local_filename}")
        milestones = load_pmcs_excel(pmcs_filename)

        with open(local_filename) as f:
            local = yaml.safe_load(f)
        for ms in milestones:
            if ms.code in local:
                # These are core PMCS attributes; we should warn if we
                # over-write them.
                for attribute in ["name", "wbs"]:
                    if attribute in local[ms.code]:
                        logger.warning(f"WARNING: overriding PMCS {attribute} on {ms.code}")
                        setattr(ms, attribute, local[ms.code][attribute])

                for attribute in ["due", "completed"]:
                    if attribute in local[ms.code]:
                        logger.warning(f"WARNING: overriding PMCS {attribute} on {ms.code}")
                        if local[ms.code][attribute] == "":
                            setattr(ms, attribute, None)
                        else:
                            setattr(ms, attribute, datetime.strptime(local[ms.code][attribute], "%Y-%m-%d"))

                for attribute in ["aka", "description", "comment", "short_name",
                                  "test_spec", "jira", "jira_testplan"]:
                    if attribute in local[ms.code]:
                        logger.info(f"WARNING: setting {attribute} on {ms.code}")
                        setattr(ms, attribute, local[ms.code][attribute])

        return MilestoneCollection(milestones)
