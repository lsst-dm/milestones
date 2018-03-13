import csv
import json

from datetime import datetime

from .utility import open_without_bom

__all__ = ["Milestone", "MilestoneCollection"]

def escape_latex(text):
    return text.strip().replace("#", "\#").replace("&", "\&").replace("Test report: ", "")

class Milestone(object):
    def __init__(self, code, name, due, description="", comment="",
                 aka="", test_spec="", predecessors=None,
                 successors=None, completed=None):
        self.code = code
        self.name = name
        self.description = description
        self.due = due
        self.comment = comment
        self.aka = aka if aka else []
        self.test_spec = test_spec
        self.predecessors = predecessors if predecessors else []
        self.successors = successors if successors else []
        self.completed = completed

    def __repr__(self):
        return "<Milestone: " + self.code + ">"

    def format_template(self, template, **kwargs):
        return template.format(code=escape_latex(self.code),
                               name=escape_latex(self.name),
                               description=escape_latex(self.description),
                               due=escape_latex(self.due.strftime("%Y-%m-%d")),
                               comment=escape_latex(self.comment),
                               aka=escape_latex(", ".join(self.aka)),
                               test_spec=escape_latex(self.test_spec),
                               predecessors=escape_latex(", ".join(self.predecessors)),
                               successors=escape_latex(", ".join(self.successors)),
                               **kwargs)

class MilestoneCollection(object):
    def __init__(self, pmcs, local):
        def extract_date(value):
            try:
                return datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")
            except ValueError:
                return datetime.strptime(value, "%m/%d/%Y")

        self.milestones = set()
        for milestone in pmcs:
            code = milestone['task_code']
            if code == "Activity ID":
                continue
            name = milestone['task_name']
            predecessors = milestone['pred_list'].split(', ')
            successors = milestone['succ_list'].split(', ')
            if milestone['base_end_date']:
                due = extract_date(milestone['base_end_date'])
            else:
                due = extract_date(milestone['start_date'])
            ms = Milestone(code, name, due,
                           predecessors=predecessors, successors=successors)
            if milestone['act_end_date']:
                ms.completed = extract_date(milestone['act_end_date'])
            if code in local:
                for attribute in ["name", "description", "comment", "aka", "test_spec"]:
                    try:
                        setattr(ms, attribute, local[code][attribute])
                    except KeyError:
                        pass
            self.milestones.add(ms)

    def filter(self, prefix=None):
        return set(ms for ms in self.milestones if ms.code.startswith(prefix))

    @staticmethod
    def from_files(pmcs_filename, local_filename):
        with open_without_bom(pmcs_filename) as f:
            dr = csv.DictReader(f)
            pmcs = list(dr)

        with open(local_filename) as f:
            local = json.load(f)

        return MilestoneCollection(pmcs, local)
