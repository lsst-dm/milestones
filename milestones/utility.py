import glob
import os
import re
import sys
import time
import yaml
import logging
import subprocess
from datetime import datetime

from .excel import load_pmcs_excel

__all__ = [
    "add_latex_citations",
    "add_rst_citations",
    "escape_latex",
    "format_latex",
    "get_pmcs_path_months",
    "get_latest_pmcs_path",
    "get_local_data_path",
    "load_milestones",
    "write_output",
    "get_version_info",
]

DOC_HANDLES = [
    "DMTN",
    "DMTR",
    "LDF",
    "LDM",
    "LDO",
    "LEP",
    "LOO",
    "LSE",
    "LSO",
    "LSP",
    "OPSTN",
    "PSTN",
    "SMTN",
    "SQR",
    "TEST",
    "RTN",
]


# Input filename format:
#
# YYYYMM-<datatype>.xls
#
# Where YYYY is the year, MM is the month and <datatype> is either "BL" (for
# baseline) or "ME" (for forecast).


def get_pmcs_path_months(cpath=None, months=3):
    """Get the list of pmcs files - find the one passed and take the one months prior.
    """
    path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..",
                                         "data", "pmcs"))
    all_files = sorted(glob.glob(os.path.join(path, "??????-ME.xls")))
    for ind, f in enumerate(all_files):
        if f.__contains__(cpath) and ind >= months:
            return all_files[ind - months]


def get_latest_pmcs_path(path=None):
    """By default, fetch the latest forecast.
    """
    if not path:
        path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "data", "pmcs")
        )
    return sorted(glob.glob(os.path.join(path, "??????-ME.xls")))[-1]


def get_local_data_path(path=os.path.dirname(__file__)):
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "local.yaml")
    )


def write_output(filename, content, comment_prefix="%"):
    print(f"Writing output to {filename}")
    with open(filename, "w") as f:
        f.write(
            f"{comment_prefix} Auto-generated by {sys.argv[0]} "
            f"on {time.strftime('%c')} - DO NOT EDIT\n\n"
        )
        f.write(content)


def escape_latex(text):
    return (
        text.strip()
        .replace("#", r"\#")
        .replace("&", r"\&")
        .replace("Test report: ", "")
    )


def add_citations(text, cite_handles, replacement_pattern):
    # Automatically add citations to anything that looks like a document
    # (Handle-NNN), unless it looks like a milestone (LDM-503-nn).
    return re.sub(
        f"(({'|'.join(cite_handles)})-\\d{{3}})(?!(?<=LDM-\\d{{3}})-\\w)",
        replacement_pattern,
        text,
    )


def add_latex_citations(text, cite_handles):
    if text:
        return add_citations(text, cite_handles, r"\\citeds{\1}")


def format_latex(text, cite_handles=DOC_HANDLES):
    if text:
        return escape_latex(add_latex_citations(text, DOC_HANDLES))
    else:
        print("No text in format_latex")
        return ""


def add_rst_citations(text, cite_handles=DOC_HANDLES):
    if text:
        return add_citations(text, cite_handles, r"\1 :cite:`\1`")


def load_milestones(pmcs_filename, local_data_filename):
    logger = logging.getLogger(__name__)

    logger.info(f"Loading PMCS data from: {pmcs_filename}")
    logger.info(f"Loading local annotations from: {local_data_filename}")
    milestones = load_pmcs_excel(pmcs_filename)

    with open(local_data_filename) as f:
        local = yaml.safe_load(f)
    for ms in milestones:
        if ms.code in local:
            # These are core PMCS attributes; we should warn if we
            # over-write them.
            for attribute in ["name", "wbs", "level", "predecessors", "successors"]:
                if attribute in local[ms.code]:
                    logger.info(
                        f"Overriding PMCS {attribute} on {ms.code} "
                        f"Overriding PMCS {attribute} on {ms.code} "
                        f"(was “{getattr(ms, attribute)}”; "
                        f"now “{local[ms.code][attribute]}”)"
                    )
                    setattr(ms, attribute, local[ms.code][attribute])

            for attribute in ["due", "completed"]:
                if attribute in local[ms.code]:
                    logger.warning(
                        f"Overriding PMCS {attribute} on {ms.code} "
                        f"(was {getattr(ms, attribute)}; "
                        f"now {local[ms.code][attribute]})"
                    )
                    if local[ms.code][attribute] == "":
                        setattr(ms, attribute, None)
                    else:
                        setattr(
                            ms,
                            attribute,
                            datetime.strptime(local[ms.code][attribute], "%Y-%m-%d"),
                        )

            for attribute in [
                "aka",
                "description",
                "comment",
                "short_name",
                "test_spec",
                "jira",
                "jira_testplan",
            ]:
                if attribute in local[ms.code]:
                    logger.info(f"Setting {attribute} on {ms.code}")
                    setattr(ms, attribute, local[ms.code][attribute])

    return milestones


def get_version_info(pmcs_path=None):
    if pmcs_path is None:
        pmcs_path = get_latest_pmcs_path()
    git_dir = os.path.dirname(pmcs_path)
    if git_dir == '':
        git_dir = '.'
    sha, date = (
        subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:'%H %ad'", "--date=unix"], cwd=git_dir
        )
        .decode("utf-8")
        .strip("'")
        .split()
    )
    split = os.path.basename(pmcs_path).split("-")
    p6_date = datetime.strptime(split[0], "%Y%m")

    return sha, datetime.utcfromtimestamp(int(date)), p6_date
