__all__ = ["predecessors"]


def predecessors(args, mc):
    for ms in sorted(mc.filter("LDM-503"), key=lambda x: (x.due, x.code)):
        print(f"{ms.code} ({ms.name}) :")
        predecessors = [prems for prems in mc.filter("DM-")
                        if prems.code in ms.predecessors]
        if not predecessors:
            print(f"    (No prdecessors)")

        for prems in sorted(predecessors, key=lambda x: (x.due, x.code)):
            print(f"    {prems.code} ({prems.name})")
