__all__ = ["delayed"]


def delayed(args, mc):
    obsolete_ms = [
        "DLP-538", "DLP-541", "DLP-458", "DM-NCSA-5", "DM-NCSA-7"
    ]

    for ms in mc.for_wbs(args.wbs):
        if ms.code not in obsolete_ms and ms.due < args.as_of and not ms.completed:
            print(ms.wbs, ms.code, ms.name, ms.due)
