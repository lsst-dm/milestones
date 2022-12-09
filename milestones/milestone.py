from dataclasses import dataclass, field
from datetime import datetime
from typing import Set, Optional

__all__ = ["Milestone"]


@dataclass
class Milestone(object):
    # These should come from Excel/PMCS
    # Sound a warning if we override locally

    code: str
    name: str
    wbs: str
    level: Optional[int]
    due: datetime
    fdue: datetime
    completed: Optional[datetime] = None
    celebrate: Optional[str] = ""
    summarychart: Optional[str] = ""

    predecessors: Set[str] = field(default_factory=set)
    successors: Set[str] = field(default_factory=set)

    # These may be set locally without triggering a warning
    aka: Set[str] = field(default_factory=set)
    description: Optional[str] = None
    comment: Optional[str] = None
    _short_name: Optional[str] = None

    test_spec: Optional[str] = None
    jira: Optional[str] = None
    jira_testplan: Optional[str] = None

    f2due: Optional[datetime] = None

    @property
    def short_name(self):
        return self._short_name if self._short_name else self.name

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    def __repr__(self):
        return "<Milestone: " + self.code + ">"
