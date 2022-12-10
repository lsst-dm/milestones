# RHL generate the block schedule diagram from the milestones with
# Summary Chart entries.


def blockschedule(args, milestones):
    # Process Summary Chart activities/milestones and celebratory milestones

    print("Summary Chart, Code, Start, Finish, Celebrate")
    for ms in milestones:
        celebrate = False
        if ms.summarychart:
            pass
        elif ms.celebrate:
            celebrate = ms.celebrate
        else:
            continue

        print(f"{ms.summarychart}, {ms.code}, {ms.start}, {ms.due}, {celebrate}")
