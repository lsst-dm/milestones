from datetime import datetime

import matplotlib.pyplot as plt

__all__ = ["burndown"]


def burndown(args, milestones):
    # We won't consider milestones before which are due and/or completed
    # before the start date. The aim is to avoid picking up a whole bunch of
    # pre-replan milestones.
    start_date, end_date = args.start_date, args.end_date

    milestones = [
        ms
        for ms in milestones
        for prefix in ["DM-", "DLP-", "LDM-503-"]
        if ms.code.startswith(prefix)
        and ms.due > start_date
        and (not ms.completed or ms.completed > start_date)
    ]

    month_starts = []
    for year in range(start_date.year, end_date.year + 1):
        for month in range(1, 13):
            dt = datetime(year, month, 1)
            if start_date <= dt <= end_date:
                month_starts.append(datetime(year, month, 1))

    model = []
    actual = []
    for date in month_starts:
        model_remain = actual_remain = len(milestones)
        for ms in milestones:
            if ms.due <= date:
                model_remain -= 1
            if ms.completed and ms.completed <= date:
                actual_remain -= 1

        model.append(model_remain)
        actual.append(actual_remain)

    last_achieved_month = None
    for ms in milestones:
        if ms.completed and (
            not last_achieved_month or last_achieved_month < ms.completed
        ):
            last_achieved_month = ms.completed

    plt.plot(month_starts, model, label="Baseline")

    achieved_months = [mnth for mnth in month_starts if mnth <= last_achieved_month]
    # Need to acount for year wrap
    if achieved_months[-1].month == 12:
        achieved_months.append(
            datetime(
                achieved_months[-1].year + 1,
                1,
                achieved_months[-1].day,
                )
        )
    else:
        achieved_months.append(
            datetime(
                achieved_months[-1].year,
                achieved_months[-1].month + 1,
                achieved_months[-1].day,
            )
        )
    plt.plot(achieved_months, actual[: len(achieved_months)], label="Achieved")

    plt.xlabel("Date")
    plt.ylabel("Open Milestones")
    plt.legend()
    plt.savefig(args.output)
