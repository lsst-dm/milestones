__all__ = ["predecessors"]


def predecessors(args, milestones):
    for ms in sorted((ms for ms in milestones if ms.code.startswith("LDM-503")),
                     key=lambda x: (x.due, x.code)):
        print(f"{ms.code} ({ms.name}) :")
        predecessors = [prems for prems in milestones
                        if prems.code in ms.predecessors
                        and prems.code.startswith("DM-")]
        if not predecessors:
            print(f"    (No prdecessors)")

        for prems in sorted(predecessors, key=lambda x: (x.due, x.code)):
            print(f"    {prems.code} ({prems.name})")
