import numpy
import sys
import xlrd
from datetime import datetime

from .milestone import Milestone

__all__ = ["load_pmcs_excel"]

TASK_SHEET_NAME = "TASK"
RELATION_SHEET_NAME = "TASKPRED"

# Skip the first two rows, which always contain header information.
START_ROW = 2

class CellFetcher(object):
    def __init__(self, hdr):
        self._hdr = [cell.value for cell in hdr]

    def __call__(self, field_name, row):
        position = self._hdr.index(field_name)
        return row[position].value

def extract_date(value):
    try:
        return datetime.strptime(value, "%m/%d/%Y %I:%M:%S %p")
    except ValueError:
        return datetime.strptime(value, "%m/%d/%Y")

def extract_task_details(task_sheet):
    assert(task_sheet.name == TASK_SHEET_NAME)
    milestones = set()
    fetcher = CellFetcher(task_sheet.row(0))
    for rownum in range(START_ROW, task_sheet.nrows):
        code = fetcher("task_code", task_sheet.row(rownum))
        name = fetcher("task_name", task_sheet.row(rownum))

        # There are three possible end dates:
        #
        #   base_end_date - according to the baseline project
        #   end_date      - the end date in the current project (which floats
        #                   as dependencies get late, etc)
        #   start_date    - the start date in the current project (as above,
        #                   will be the same as the end_date for zero duration activities like
        #                   milestones.
        #
        # We use the first available.
        for date_field in ("base_end_date", "end_date", "start_date"):
            d = fetcher(date_field, task_sheet.row(rownum))
            try:
                due = extract_date(d)
            except ValueError:
                pass
            else:
                break

        ms = Milestone(code, name, due)
        act_end_date = fetcher("act_end_date", task_sheet.row(rownum))
        if act_end_date:
            ms.completed = extract_date(act_end_date)
        milestones.add(ms)
    return milestones

def set_successors(milestones, relation_sheet):
    assert(relation_sheet.name == RELATION_SHEET_NAME)
    pred_col = relation_sheet.row_values(0).index("pred_task_id")
    succ_col = relation_sheet.row_values(0).index("task_id")
    preds = numpy.array(relation_sheet.col_values(pred_col))[START_ROW:]
    succs = numpy.array(relation_sheet.col_values(succ_col))[START_ROW:]
    for ms in milestones:
        for i in numpy.where(preds == ms.code)[0]:
            ms.successors.add(succs[i])
        for i in numpy.where(succs == ms.code)[0]:
            ms.predecessors.add(preds[i])

def load_pmcs_excel(path):
    workbook = xlrd.open_workbook(path, logfile=sys.stderr)
    milestones = extract_task_details(workbook.sheets()[0])
    set_successors(milestones, workbook.sheets()[1])
    return milestones
