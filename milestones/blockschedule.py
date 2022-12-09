from io import StringIO
from .utility import get_version_info, write_output, load_milestones




def blockschedule(args, milestones):
    # pullout Summary Chart milestones
    milestones = [
        ms
        for ms in milestones
        if ms.summarychart
    ]

    for ms in milestones:
        print (f"{ms.summarychart}, {ms.due}")
