# RHL generate the block schedule diagram from the milestones with
# Summary Chart entries.


def blockschedule(args, milestones):
    # pullout Summary Chart milestones
    milestones = [
        ms
        for ms in milestones
        if ms.summarychart
    ]

    for ms in milestones:
        print(f"{ms.summarychart}, {ms.due}")
