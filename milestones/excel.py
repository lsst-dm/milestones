import logging
import re
import sys
from datetime import datetime

import numpy
import xlrd

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
        try:
            return datetime.strptime(value, "%m/%d/%Y")
        except ValueError:
            logger = logging.getLogger(__name__)
            logger.debug(f"Couldn't parse '{value}' as date")
            raise


def extract_wbs(value):
    try:
        return re.match(r"LSST ME .*(0\dC\.\d\d(\.\d\d)?)", value).groups()[0]
    except AttributeError:
        return ""


def extract_fcast(task_sheet, milestones):
    # get forceast dates from sheet
    # go through all milestones and add the f2date
    assert task_sheet.name == TASK_SHEET_NAME
    fetcher = CellFetcher(task_sheet.row(0))
    fdates = {}
    for rownum in range(START_ROW, task_sheet.nrows):
        d = fetcher("end_date", task_sheet.row(rownum))
        code = fetcher("task_code", task_sheet.row(rownum))
        try:
            f2due = extract_date(d)
            fdates[code] = f2due
        except ValueError:
            pass

    print(f"Got {len(fdates)} forecast dates")
    for m in milestones:
        if m.code in fdates:
            m.f2due = fdates[m.code]
        else:  # could be a new milestone not there n months ago
            m.f2due = m.due

    return milestones


def extract_task_details(task_sheet, load_tasks):
    assert task_sheet.name == TASK_SHEET_NAME
    milestones = list()
    fetcher = CellFetcher(task_sheet.row(0))
    for rownum in range(START_ROW, task_sheet.nrows):
        tasktype = fetcher("task_type", task_sheet.row(rownum))
        # File now has milestones and tasks many things only want milestones
        if not (load_tasks or "Milestone" in tasktype):
            continue
        code = fetcher("task_code", task_sheet.row(rownum))
        name = fetcher("task_name", task_sheet.row(rownum))

        # "user_field_859" is just a magic value extracted from the spreadsheet
        level = fetcher("user_field_859", task_sheet.row(rownum))
        level = int(level) if level else None

        # There are three possible end dates:
        #
        #   base_end_date - according to the baseline project
        #   end_date      - the end date in the current project (which floats
        #                   as dependencies get late, etc)
        #   start_date    - the start date in the current project (as above,
        #                   will be the same as the end_date for zero duration
        #                   activities like milestones.

        status = fetcher("status_code", task_sheet.row(rownum))
        act_end_date = fetcher("act_end_date", task_sheet.row(rownum))
        base_end_date = fetcher("base_end_date", task_sheet.row(rownum))
        start_date = fetcher("start_date", task_sheet.row(rownum))
        end_date = fetcher("end_date", task_sheet.row(rownum))

        start = due = fdue = None

        if start_date:
            start = extract_date(start_date)
        if base_end_date:
            due = extract_date(base_end_date)
        if end_date:
            fdue = extract_date(end_date)

        if not due and fdue:
            due = fdue
        if not due:
            if tasktype.startswith("Start"):
                due = start
        if not fdue and due:
            fdue = due
        completed = None
        if status == "Completed":
            if act_end_date:
                completed = extract_date(act_end_date)
            elif base_end_date:
                completed = extract_date(base_end_date)
            elif start_date:
                completed = extract_date(start_date)
            else:
                raise ValueError(f"{code} is completed with no date")

        wbs = extract_wbs(fetcher("wbs_id", task_sheet.row(rownum)))
        celebrate = fetcher(
            "actv_code_celebratory_achievements_id", task_sheet.row(rownum)
        )
        summarychart = fetcher("actv_code_summary_chart_id", task_sheet.row(rownum))

        milestones.append(
            Milestone(
                code,
                tasktype,
                name,
                wbs,
                level,
                due,
                fdue,
                start,
                completed,
                celebrate,
                summarychart,
            )
        )

    return milestones


def set_successors(milestones, relation_sheet):
    assert relation_sheet.name == RELATION_SHEET_NAME
    pred_col = relation_sheet.row_values(0).index("pred_task_id")
    succ_col = relation_sheet.row_values(0).index("task_id")
    preds = numpy.array(relation_sheet.col_values(pred_col))[START_ROW:]
    succs = numpy.array(relation_sheet.col_values(succ_col))[START_ROW:]
    for ms in milestones:
        for i in numpy.where(preds == ms.code)[0]:
            ms.successors.add(succs[i])
        for i in numpy.where(succs == ms.code)[0]:
            ms.predecessors.add(preds[i])


def load_pmcs_excel(path, load_tasks=False):
    workbook = xlrd.open_workbook(path, logfile=sys.stderr)
    milestones = extract_task_details(workbook.sheets()[0], load_tasks)
    set_successors(milestones, workbook.sheets()[1])
    return milestones


def load_f2due_pmcs_excel(fpath, milestones):
    # given milestones, load the sheet from N months prior
    # set fdue2 to the forecast date from the file
    print(f"Loading forecast from {fpath}")
    workbook = xlrd.open_workbook(fpath, logfile=sys.stderr)
    milestones = extract_fcast(workbook.sheets()[0], milestones)
    return milestones
