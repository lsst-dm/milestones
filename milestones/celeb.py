import calendar
import re
import textwrap
from abc import ABC, abstractmethod
from contextlib import contextmanager
from io import StringIO

from .utility import (
    get_pmcs_path_months,
    get_version_info,
    load_milestones,
    write_output,
)

HEADING_CHARS = '#=-^"'


class TextAccumulator(ABC):
    def __init__(self):
        self._buffer = StringIO()

    @abstractmethod
    def get_result(self):
        return self._buffer.getvalue()


class Paragraph(TextAccumulator):
    def write_line(self, line):
        self._buffer.write(line + "\n")

    def get_result(self):
        return super().get_result() + "\n"


def underline(text, character, overline=False):
    line = character * len(text) + "\n"
    return f"{line if overline else ''}{text}\n{line}".strip()


def add_context(context_name, context_manager, *, needs_level=False):
    def wrapper(cls):
        @contextmanager
        def new_method(self, *args, **kwargs):
            if needs_level:
                level = self._level + 1 if hasattr(self, "_level") else 1
                manager = context_manager(level, *args, **kwargs)
            else:
                manager = context_manager(*args, **kwargs)
            yield manager
            self._buffer.write(manager.get_result())

        setattr(cls, context_name, new_method)
        return cls

    return wrapper


@add_context("paragraph", Paragraph)
class BulletListItem(TextAccumulator):
    def get_result(self):
        line_start = "-"
        indented_result = textwrap.indent(
            self._buffer.getvalue(), " " * (len(line_start) + 1)
        )
        return line_start + indented_result[len(line_start) :]


@add_context("bullet", BulletListItem)
class BulletList(TextAccumulator):
    def get_result(self):
        return super().get_result()


# Can't reference BulletList before it is defined
BulletListItem = add_context("bullet_list", BulletList)(BulletListItem)


class TableRow(TextAccumulator):
    def write_col(self, line):
        self._buffer.write(f"- {line}\n")

    def get_result(self):
        line_start = "   *"
        indented_result = textwrap.indent(
            self._buffer.getvalue(), " " * (len(line_start) + 1)
        )
        return line_start + indented_result[len(line_start) :]


@add_context("row", TableRow)
class Table(TextAccumulator):
    def get_result(self):
        head = ".. list-table::\n   :header-rows: 1"
        return f"{head}\n\n{super().get_result()}\n\n"


# Can't reference Table before it is defined
TableRow = add_context("table", Table)(TableRow)


@add_context("paragraph", Paragraph)
@add_context("bullet_list", BulletList)
@add_context("table", Table)
class Section(TextAccumulator):
    def __init__(self, level, title, anchor=None):
        super().__init__()
        self._level = level
        if anchor:
            self._buffer.write(f".. _{anchor}:\n\n")
        self._buffer.write(underline(title, HEADING_CHARS[self._level]) + "\n\n")

    def get_result(self):
        return super().get_result()


# Can't reference Section before it is defined.
Section = add_context("section", Section, needs_level=True)(Section)


@add_context("paragraph", Paragraph)
@add_context("section", Section, needs_level=True)
@add_context("bullet_list", BulletList)
@add_context("table", Table)
class ReSTDocument(TextAccumulator):
    def __init__(self, title="Celebratory Milestones", subtitle=None, options=None):
        super().__init__()
        if title:
            self._buffer.write(underline(title, HEADING_CHARS[0], True) + "\n")
        if subtitle:
            self._buffer.write(underline(subtitle, HEADING_CHARS[1], True) + "\n")

        options = options or {}
        for name, value in options.items():
            self._buffer.write(f":{name}:")
            if value:
                self._buffer.write(f" {value}")
            self._buffer.write("\n")

        if title or subtitle or options:
            self._buffer.write("\n")

    def get_result(self):
        return super().get_result()


def write_html(top_milestones, pmcs_data, comp_milestones, compline):
    # simple html page for inclusion by communications
    # uses fdue - forecast date
    file_name = "top_milestones.html"
    ofile = open(file_name, "w")

    print(
        "<!DOCTYPE html>"
        "<!-- Simple page with the top milestones on it -->\n"
        '<html lang="en"> <head> <meta charset="utf-8">\n'
        '<link type="text/css" rel="stylesheet" href="https://fonts.googleapis.'
        'com/css?family=Raleway:300,500,700&amp;subset=latin" media="all" />\n'
        '<style type="text/css" media="all">\n'
        '@import url("https://www.lsst.org/sites/all/themes/edu/css/style.css");'
        '@import url("https://www.lsst.org/sites/default/files/'
        'fontyourface/font.css");\n'
        '@import url("https://www.lsst.org/sites/default/files/'
        'css_injector/css_injector_4.css");\n'
        "body { background: none; } \n"
        "th { font-weight: bold; } \n"
        "td { line-height: 1.05em; padding 2px; font-family: Raleway, sans;"
        " font-weight: 500;  }\n"
        "p { line-height: 2.05em; font-size: x-small; font-weight: bold; }\n"
        "</style>\n"
        "</head> <body>\n"
        '<table id="top_miles">'
        "<tr><th>Due</th><th>"
        "Name</th><th>",
        "Previously</th></tr>",
        file=ofile,
    )

    for m in top_milestones:
        date = m.fdue.strftime("%d-%b-%Y")
        completed = completed_or_previosdue(m, comp_milestones)
        print(
            f"<tr><td>{date}</td> " f"<td>{m.name}</td><td>{completed}</td>" "</tr>",
            file=ofile,
        )

    sha, timestamp, p6_date = get_version_info(pmcs_data)
    print(
        f"</table>"
        f"<p>Using {p6_date.strftime('%B %Y')} project controls data. {compline}</p>"
        f"</body>",
        file=ofile,
    )


def find_comp(comps, code):
    comp = None
    for m in comps:
        if m.code == code:
            comp = m
    return comp


def write_row(b, code, name, due, comp):
    b.write_col(code)
    b.write_col(name)
    b.write_col(due)
    b.write_col(comp)


def completed_or_previosdue(ms, comp_milestones):
    completed = ""
    if ms.completed:
        completed = "**Completed**"
    else:
        if comp_milestones:
            cm = find_comp(comp_milestones, ms.code)
            if cm:
                date = cm.fdue.strftime("%d-%b-%Y")
                completed = f"{date}"
    return completed


def write_table(my_section, milestones, comp_milestones):
    # uses fdue - forecast date
    with my_section.table() as my_table:
        with my_table.row() as my_row:
            write_row(my_row, "Code", "Name", "Due", "Previously")
        for ms in milestones:
            with my_table.row() as my_row:
                completed = ""
                if ms.completed:
                    completed = "**Completed**"
                else:
                    if comp_milestones:
                        cm = find_comp(comp_milestones, ms.code)
                        if cm:
                            completed = f"{cm.fdue.strftime('%Y-%m-%d')}"

                write_row(
                    my_row, ms.code, ms.name, ms.fdue.strftime("%Y-%m-%d"), completed
                )


def write_list(my_section, milestones, comp_milestones):
    # uses fdue - forecast date
    with my_section.bullet_list() as my_list:
        for ms in milestones:
            with my_list.bullet() as b:
                with b.paragraph() as p:
                    completed = ""
                    if ms.completed:
                        completed = (
                            f" **Completed " f"{ms.completed.strftime('%Y-%m-%d')}**"
                        )
                    if comp_milestones:
                        cm = find_comp(comp_milestones, ms.code)
                        cdate = "None"
                        if cm:
                            cdate = f"{cm.fdue.strftime('%Y-%m-%d')}"
                        p.write_line(
                            f"{cdate}-> **{ms.fdue.strftime('%Y-%m-%d')}** : "
                            f"{ms.name} ({ms.code}) {completed}"
                        )
                    else:
                        p.write_line(
                            f"**{ms.fdue.strftime('%Y-%m-%d')}** : "
                            f"{ms.name} ({ms.code}) {completed}"
                        )


def generate_doc(args, milestones):
    # pullout celebratory milestones - only Top or Y are the values
    comp_milestones = None
    months = args.months
    comp_ym = []
    if args.pmcs_comp is not None:
        if months > 0:
            print(
                f"Ignoring months argument ({months}) since "
                f"pmcs_comp is set ({args.pmcs_comp})"
            )
        comp_milestones = load_milestones(args.pmcs_comp, args.local_data)
        comp_ym = re.findall(r"\(d{4}d{2}-", args.pmcs_comp)
    else:
        if months > 0:
            comp_milestones = load_milestones(
                get_pmcs_path_months(args.pmcs_data, months), args.local_data
            )

    milestones = [ms for ms in milestones if ms.milestone_tracking == "Y"]

    milestones = sorted(milestones, key=lambda ms: ms.fdue)

    doc = ReSTDocument()
    with doc.section("Provenance") as my_section:
        with my_section.paragraph() as p:
            sha, timestamp, p6_date = get_version_info(args.pmcs_data)
            p.write_line(
                f"This document was generated based on the contents of "
                f"the `lsst-dm/milestones <https://github.com/lsst-dm/milestones>`_ "
                f"repository, version "
                f"`{sha[:8]} <https://github.com/lsst-dm/milestones/commit/{sha}>`_, "
                f"dated {timestamp.strftime('%Y-%m-%d')}."
            )
            compline = ""
            if comp_milestones:
                if months > 0:
                    yr = p6_date.strftime("%Y")
                    mo = int(p6_date.strftime("%m")) - months
                    if mo < 1:
                        mo = 12 + mo
                        yr = int(yr) - 1
                    if mo > 12:
                        mo = mo - 12
                        yr = int(yr) + 1
                    comp_ym = [yr, calendar.month_name[mo]]
                    compline = f" This compares to {comp_ym[1]} {comp_ym[0]}."
            p.write_line(
                f"This corresponds to the status recorded in the project "
                f"controls system for {p6_date.strftime('%B %Y')}. {compline}"
            )

    with doc.section("Key milestones") as my_section:
        top_milestones = [ms for ms in milestones if ms.milestone_tracking == "Y"]
        write_html(top_milestones, args.pmcs_data, comp_milestones, compline)
        if args.table:
            write_table(my_section, top_milestones, comp_milestones)
        else:
            write_list(my_section, top_milestones, comp_milestones)
        with my_section.paragraph() as p:
            p.write_line(
                "A public HTML version for embedding is "
                "`here <./top_milestones.html>`_."
            )

    return doc.get_result()


def celeb(args, milestones):
    # pullout celebratory milestones - only Top or Y are the values
    write_output("index.rst", generate_doc(args, milestones), comment_prefix="..")
