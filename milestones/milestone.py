__all__ = ["Milestone"]

def escape_latex(text):
    return text.strip().replace("#", "\#").replace("&", "\&").replace("Test report: ", "")

class Milestone(object):
    def __init__(self, code, name, due, description="", comment="",
                 aka="", test_spec="", short_name=None, predecessors=None,
                 successors=None, completed=None, wbs=None, jira=None,
                 jira_testplan=None):
        self.code = code
        self.name = name
        self._short_name = short_name
        self.description = description
        self.due = due
        self.comment = comment
        self.aka = aka if aka else []
        self.test_spec = test_spec
        self.predecessors = set(predecessors) if predecessors else set()
        self.successors = set(successors) if successors else set()
        self.completed = completed
        self.wbs = wbs
        self.jira = jira
        self.jira_testplan = jira_testplan

    @property
    def short_name(self):
        return self._short_name if self._short_name else self.name

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    def __repr__(self):
        return "<Milestone: " + self.code + ">"

    def format_template(self, template, **kwargs):
        return template.format(code=escape_latex(self.code),
                               name=escape_latex(self.name),
                               short_name=escape_latex(self.short_name),
                               description=escape_latex(self.description),
                               due=escape_latex(self.due.strftime("%Y-%m-%d")),
                               comment=escape_latex(self.comment),
                               aka=escape_latex(", ".join(self.aka)),
                               test_spec=escape_latex(self.test_spec),
                               predecessors=escape_latex(", ".join(self.predecessors)),
                               successors=escape_latex(", ".join(self.successors)),
                               **kwargs)
