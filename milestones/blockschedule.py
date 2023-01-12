# RHL generate the block schedule diagram from the milestones with
# Summary Chart entries.

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

from .cartoon import show_activities, add_legend, Activity, AdvanceRow, Milestone, Nrow, Rotation
from .cartoon_config import \
    categoryNrow, categoryColors, wrappedDescrip, categoryGrouping, specials, \
    nRowOfMilestones, milestoneHeight, milestoneWidth, legend_location, today_height


def blockschedule(args, milestones):
    # Process Summary Chart activities/milestones and celebratory milestones

    activities, celebrations = process_milestones(milestones)

    blocks = create_blocks(activities, celebrations)

    plt.figure(figsize=(10, 8))
    show_activities(blocks, height=1, fontsize=args.fontsize, show_today=True,
                    title=os.path.split(args.pmcs_data)[1], today_height=today_height,
                    show_weeks=args.show_weeks, startDate=args.start_date, endDate=args.end_date)

    add_legend(categoryColors, blocks, categoryGrouping, legend_location=legend_location)

    plt.savefig(args.output)


def create_blocks(activities, celebrations):
    #
    # Convert those activities to a set of block descriptions
    #
    blocks = {}
    row = 1
    for category in activities:
        blocks[category] = []

        nrow = categoryNrow.get(category, 5)
        nrow, rot = (nrow, None) if isinstance(nrow, int) else nrow

        blocks[category] = [Nrow(nrow), Rotation(rot)]

        color = categoryColors.get(category)
        if color is None:
            print(f"No colour is defined for category {category}", file=sys.stderr)
            color = ("white", "red")
        color, border = (color, None) if isinstance(color, str) else color

        row += 1

        for descrip in sorted(activities[category]):
            start = np.min([start for (code, start, due) in activities[category][descrip]])
            due   = np.max([due   for (code, start, due) in activities[category][descrip]])  # noqa: E221,E272

            if descrip in specials:
                nrow, rot, nadvance = specials[descrip]
                if nrow is not None:
                    blocks[category].append(Nrow(nrow))
                if rot is not None:
                    blocks[category].append(Rotation(rot))
                if nadvance is not None:
                    blocks[category].append(AdvanceRow(nadvance))

            if descrip[0] == '"' and descrip[-1] == '"':
                descrip = descrip[1:-1]

            blocks[category].append(Activity(descrip, start, due, color, border,
                                             wrappedDescrip=wrappedDescrip.get(descrip)))

    #
    # Order/group according to categoryGrouping[]
    #
    if categoryGrouping is None:
        grouping = [[cat] for cat in activities]
    else:
        grouping = categoryGrouping

    _blocks = []
    for cats in grouping:
        sub = []
        for cat in cats:
            for a in blocks[cat]:
                sub.append(a)

        _blocks.append(sub)

    blocks = _blocks
    #
    # Handle celebrations milestones now that we've ordered the blocks
    #
    Milestone.height = milestoneHeight
    Milestone.width = milestoneWidth
    Milestone.rotation = 0

    milestones = []
    for c in celebrations:
        name, start = c
        milestones.append(Milestone(name, start))

    milestones = sorted(milestones, key=lambda a: a.t0)
    for i, ml in enumerate(milestones):
        ml.drow = i % nRowOfMilestones

    milestones.append(AdvanceRow((nRowOfMilestones - 1)*milestoneHeight))

    blocks = [milestones] + blocks

    return blocks


def process_milestones(milestones):
    # Process Summary Chart activities/milestones and celebrations milestones

    activities = {}
    celebrations = []

    for ms in milestones:
        summarychart, code, start, due = ms.summarychart, ms.code, ms.start, ms.fdue
        if ms.due is not None and start is not None and due < start and ms.due >= start:
            if True:
                print("Warning: "
                      f"{ms.code} has fdue = {ms.fdue} before start = {ms.start}, "
                      f"but due = {ms.due} is later", file=sys.stderr)
            due = ms.due

        celebrate = False
        if ms.summarychart:
            pass
        elif ms.celebrate:
            celebrate = ms.celebrate.lower()
        else:
            continue
        #
        # handle dates, either of which may have been omitted
        #
        if start is None:
            if due is None:             # HACK
                print(f"{ms} has no date field; skipping", file=sys.stderr)
                continue
            else:
                start = due
        elif due is None:
            due = start
        #
        # Is it a celebrations milestone rather than an activity?
        #
        if celebrate in ("top", "y"):  # it's a celebrations milestone
            if celebrate == "y":
                continue

            celebrations.append((ms.name, due))
            continue

        if True:
            if start > due:
                print(f"Warning: {ms.code:15s}  {ms.summarychart:40s} {start} {due} "
                      f": {ms.start} v. {ms.fdue}")

        if '.' not in summarychart:
            summarychart = f"{summarychart}.{summarychart}"

        category, descrip = summarychart.split(".")
        category = category.replace(' ', '_')

        if "," in descrip:
            descrip = f'"{descrip}"'

        if category not in activities:
            activities[category] = {}

        if descrip not in activities[category]:
            activities[category][descrip] = []

        activities[category][descrip].append((code, start, due))

    return activities, celebrations
