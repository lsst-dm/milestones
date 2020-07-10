__all__ = ["predecessors"]


def predecessors(args, mc):
    for ms in sorted(mc.filter("LDM-503"), key=lambda x: (x.due, x.code)):
        predecessors = [prems for prems in mc.filter("DM-")
                        if prems.code in ms.predecessors]
        for prems in sorted(predecessors, key=lambda x: (x.due, x.code)):
            print(ms.code + " : " + prems.code)
