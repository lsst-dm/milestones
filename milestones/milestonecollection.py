import json

from datetime import datetime

from .excel import load_pmcs_excel

__all__ = ["MilestoneCollection"]

class MilestoneCollection(object):
    def __init__(self, milestones):
        self.milestones = milestones

    def filter(self, prefix=None):
        return set(ms for ms in self.milestones if ms.code.startswith(prefix))

    @staticmethod
    def from_files(pmcs_filename, local_filename):
        milestones = load_pmcs_excel(pmcs_filename)

        with open(local_filename) as f:
            local = json.load(f)
        for ms in milestones:
            if ms.code in local:
                for attribute in ["name", "description", "comment", "aka",
                                  "test_spec", "short_name"]:
                    try:
                        setattr(ms, attribute, local[ms.code][attribute])
                    except KeyError:
                        pass
        return MilestoneCollection(milestones)
