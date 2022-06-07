from io import StringIO
from .utility import get_version_info, write_output
from contextlib import contextmanager
import textwrap


from abc import ABC, abstractmethod

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
        return line_start + indented_result[len(line_start):]


@add_context("bullet", BulletListItem)
class BulletList(TextAccumulator):
    def get_result(self):
        return super().get_result()


# Can't reference BulletList before it is defined
BulletListItem = add_context("bullet_list", BulletList)(BulletListItem)


@add_context("paragraph", Paragraph)
@add_context("bullet_list", BulletList)
class Section(TextAccumulator):
    def __init__(self, level, title, anchor=None):
        super().__init__()
        self._level = level
        if anchor:
            self._buffer.write(f".. _{anchor}:\n\n")
        self._buffer.write(
            underline(title, HEADING_CHARS[self._level]) + "\n\n")

    def get_result(self):
        return super().get_result()


# Can't reference Section before it is defined.
Section = add_context("section", Section, needs_level=True)(Section)


@add_context("paragraph", Paragraph)
@add_context("section", Section, needs_level=True)
@add_context("bullet_list", BulletList)
class ReSTDocument(TextAccumulator):
    def __init__(self, title=None, subtitle=None, options=None):
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


def generate_doc(args, milestones):
    # pullout celebratory milestones - only Top or Y are the values
    inc = args.inc

    milestones = [
        ms
        for ms in milestones
        if ms.celebrate
    ].sort()

    doc = ReSTDocument(options={"tocdepth": 0})
    with doc.section("Provenance") as my_section:
        with my_section.paragraph() as p:
            sha, timestamp, p6_date = get_version_info()
            p.write_line(
                f"This document was generated based on the contents of "
                f"the `lsst-dm/milestones <https://github.com/lsst-dm/milestones>`_ "
                f"repository, version "
                f"`{sha[:8]} <https://github.com/lsst-dm/milestones/commit/{sha}>`_, "
                f"dated {timestamp.strftime('%Y-%m-%d')}."
            )
            p.write_line(
                f"This corresponds to the status recorded in the project "
                f"controls system for {p6_date.strftime('%B %Y')}."
            )

    with doc.section("Top milestones") as my_section:
        top_milestones = [
            ms
            for ms in milestones
            if ms.celebrate == "Top"
        ]
        with my_section.bullet_list() as my_list:
            for ms in sorted(top_milestones, key=lambda ms: ms.wbs + ms.code):
                with my_list.bullet() as b:
                    with b.paragraph() as p:
                        p.write_line(
                            f"`{ms.code}`_: {ms.name} "
                            f"[Due {ms.due.strftime('%Y-%m-%d')}]"
                        )

    if (inc == "Y"):
        with doc.section("Supporting milestones") as my_section:
            o_milestones = [
                ms
                for ms in milestones
                if ms.celebrate == "Y"
            ]
            with my_section.bullet_list() as my_list:
                for ms in sorted(o_milestones,
                                 key=lambda ms: ms.wbs + ms.code):
                    with my_list.bullet() as b:
                        with b.paragraph() as p:
                            p.write_line(
                                f"`{ms.code}`_: {ms.name} "
                                f"[Due {ms.due.strftime('%Y-%m-%d')}]"
                            )

    return doc.get_result()


def celeb(args, milestones):
    # pullout celebratory milestones - only Top or Y are the values
    write_output("index.rst", generate_doc(args, milestones),
                 comment_prefix="..")
