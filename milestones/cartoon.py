import csv
from datetime import datetime, timedelta
import re
import sys
import textwrap

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

__all__ = ["show_activities", "add_legend", "print_details",
           "Activity", "Milestone", "AdvanceRow", "Nrow", "Rotation",
]


class Activity:
    border = None
    color = None
    nrow = 1                         # number of rows in an Activity
    markerWidth = 0
    fontsize = 8
    height = 0.3
    row = 0
    rotation = None

    time = None

    def __init__(self, descrip, t0, duration, color=None, border=None, markerWidth=0, rotation=0,
                 drow=0, nrow=0, wrappedDescrip=None):
        """An activity to be carried out
        descrip: string description; will be wrapped based on a guess on available width
        t0: starting date as string (e.g. 1958-02-05)
        duration: duration in days, or ending date in same format as t0
        color: color to use, or None to use current default
        border: border color to use, or None to use current default
        markerwidth: XX, or None to use current default
        rotation: rotate text by this many degrees
        drow: offset Activity by drow when drawing
          (see also AdvanceRow in show_activities())
        wrappedDescrip:  hand-line-wrapped version of descrip; usually None, which uses textwrap.fill
        """
        self.descrip = descrip
        self.wrappedDescrip = wrappedDescrip   # hand-line-wrapped version of descrip; usually None

        if t0:
            if not isinstance(t0, datetime):
                t0 = datetime.fromisoformat(t0)

            self.t0 = t0
        else:
            self.t0 = Activity.time

        try:
            try:
                duration = float(duration)
            except (TypeError, ValueError):
                pass
            if not isinstance(duration, timedelta):
                duration = timedelta(duration)
            self.duration = duration
        except TypeError:
            if not isinstance(duration, datetime):
                duration = datetime.fromisoformat(duration)

            self.duration = duration - self.t0

        Activity.time = self.t0 + self.duration

        self.drow = drow
        self._nrow = nrow if nrow > 0 else None
        self._color = color if color else None
        self._border = border if border else None
        self._markerWidth = markerWidth if markerWidth else None
        self._rotation = rotation if rotation else None

    def __repr__(self):
        return f"Activity({self.descrip}, {self.t0}, {self.duration.days}, {self._color}, {self._border})"

    def __str__(self):
        descrip = self.descrip
        if ',' in descrip and descrip[0] != '"':
            descrip = f'"{descrip}"'

        return f"Activity, {descrip}, {self.t0}, {self.t0 + self.duration}, {self._color}, {self._border}"

    def getData(self):
        return [self.descrip, self.t0.strftime('%Y-%m-%d'), (self.t0 + self.duration).strftime('%Y-%m-%d'),
                self._color, self._border, self._markerWidth, self.drow,
               ]

    def getNrow(self):
        return self.nrow if self._nrow is None else self._nrow

    def draw(self, totalDuration=0, startDate="1958-02-05", endDate="2099-12-31", **kwargs):
        kwargs = kwargs.copy()
        if "nrowTot" in kwargs:
            nrowTot = kwargs["nrowTot"]
            del kwargs["nrowTot"]
        else:
            nrowTot = 1

        if "alpha" not in kwargs:
            kwargs["alpha"] = 0.9
        if "color" not in kwargs:
            kwargs["color"] = self.color if self._color is None else self._color
        nrow = self.getNrow()

        rotation = (90 if nrow > 1 else 0) if self.rotation is None else self.rotation

        if isinstance(endDate, str):
            endDate = datetime.fromisoformat(endDate)

        t0 = self.t0 + timedelta(hours=12)
        t1 = t0 + self.duration

        if t1 < startDate:
            return 0
        elif t0 < startDate:
            t0 = startDate

        if t0 > endDate:
            return 0
        elif t1 > endDate:
            t1 = endDate

        y0 = self.height*(1.1*(self.row - self.drow))
        x = t0 + (t1 - t0)*np.array([0, 1, 1, 0, 0])
        y = y0 + (1 + 1.1*(nrow - 1))*self.height*np.array([0, 0, 1, 1, 0])
        plt.fill(x, y, '-', label=self.descrip, **kwargs)

        if not (self.border is None and self._border is None):
            kwargs["color"] = self.border if self._border is None else self._border

        plt.plot(x, y, '-', **kwargs)

        textwidth = 0
        fontsize = self.fontsize if self.fontsize else 10
        if rotation == 90:
            width_pts = plt.gcf().get_size_inches()[1]*72

            fiddleFactor = 1.5*width_pts/nrowTot
            textwidth = int(fiddleFactor*nrow/self.fontsize) + 1
        else:
            if totalDuration == 0:
                fiddleFactor = 3
            else:
                width_pts = plt.gcf().get_size_inches()[0]*72
                fiddleFactor = width_pts/totalDuration.days

            textwidth = int(fiddleFactor*self.duration.days/self.fontsize) + 1

        if self.wrappedDescrip is None:
            text = textwrap.fill(self.descrip, width=textwidth, break_long_words=False)
        else:
            text = self.wrappedDescrip

        if textwidth <= 0:
            textwidth = 10
        plt.text(t0 + 0.5*(t1 - t0), 0.5*(y[1] + y[2]), text,
                 rotation=rotation,
                 horizontalalignment='center', verticalalignment='center',
                 fontsize=self.fontsize)

        return nrow


class Milestone(Activity):
    axvline = False                     # draw a vertical line through Milestones
    markerWidth = 2
    nrow = 1
    rotation = 0                        # text rotation
    color = None
    border = None

    def __init__(self, descrip, t0, color=None, border=None, align="right", valign="top",
                 markerWidth=None, drow=0):
        super().__init__(descrip, t0, 0.0, color=color, border=border, drow=drow, markerWidth=markerWidth)
        self.align = align
        self.valign = valign

    def __repr__(self):
        return f"Milestone({self.descrip})"

    def __str__(self):
        return f"Milestone, {self.descrip}, {self.t0}, {self._color}, {self._border}, " \
            f"{self.align}, {self.valign}, {self._markerWidth}, {self.drow}, {self.height}"

    def getData(self):
        return [self.descrip, self.t0.strftime('%Y-%m-%d'),
                self._color, self._border, self.align, self.valign, self._markerWidth, self.drow]

    def __getNrow(self):
        return self.height

    def draw(self, totalDuration=0, startDate="1958-02-05", endDate="2099-12-31", **kwargs):
        kwargs = kwargs.copy()
        del kwargs["nrowTot"]
        if "color" not in kwargs:
            kwargs["facecolor"] = self.color if self._color is None else self._color

        if not (self.border is None and self._border is None):
            kwargs["edgecolor"] = self.border if self._border is None else self._border
        else:
            kwargs["edgecolor"] = kwargs.get("facecolor")

        if kwargs["edgecolor"]:
            import matplotlib
            kwargs["edgecolor"] = matplotlib.colors.to_rgba(kwargs["edgecolor"], kwargs.get("alpha", 1))

        kwargs["linewidth"] = 2

        if "alpha" not in kwargs:
            kwargs["alpha"] = 0.5

        if isinstance(startDate, str):
            startDate = datetime.fromisoformat(startDate)
        if isinstance(endDate, str):
            endDate = datetime.fromisoformat(endDate)

        t0 = self.t0 + timedelta(hours=12)
        if t0 + self.duration < startDate:
            return 0
        elif t0 < startDate:
            t0 = startDate

        if t0 > endDate:
            return 0

        y0 = self.height*(1.1*(self.row - self.drow))

        markerWidth = timedelta(self.markerWidth if self._markerWidth is None else self._markerWidth)
        x = t0 + 0.9*markerWidth*np.array([0, 1, 0, -1, 0])
        y = y0 + 0.9*self.height*np.array([0, 0.5, 1, 0.5, 0])
        plt.fill(x, y, '-', **kwargs)

        if Milestone.axvline:
            plt.axvline(t0, ls='-', alpha=0.1, zorder=-1)

        horizontalalignment = "left" if self.align == "right" else "right"  # matplotlib is confusing
        plt.text(t0 + markerWidth/2*(1 if self.align == "right" else -1),
                 y0 + (0.9 if self.valign == "top" else 0.1)*self.height, self.descrip,
                 rotation=self.rotation,
                 horizontalalignment=horizontalalignment, verticalalignment='center',
                 fontsize=self.fontsize, zorder=10)

        return 1


class Manipulation:
    """Modify the state of the system, rather than describing an activity or milestone"""
    pass

class AdvanceRow(Manipulation):
    """A class used to advance the row counter"""

    def __init__(self, drow):
        self.drow = drow

    if False:
        def getNrow(self):
            return self.drow

    def __repr__(self):
        return f"AdvanceRow({self.drow})"

    def __str__(self):
        return f"AdvanceRow, {self.drow}"

    def getData(self):
        return [self.drow]


class Nrow(Manipulation):
    """A class used to set the height of the activities"""

    def __init__(self, nrow):
        self.nrow = nrow

    def __repr__(self):
        return f"Nrow({self.nrow})"

    def __str__(self):
        return f"Nrow, {self.nrow}"

    def getNrow(self):
        return self.nrow

    def set_default_Nrow(self):
        Activity.nrow = self.nrow

    def getData(self):
        return [self.nrow]


class Rotation(Manipulation):
    """A class used to set the text rotation"""

    def __init__(self, rotation):
        self.rotation = rotation   # angle in degrees

    def __repr__(self):
        return f"Rotation({self.rotation})"

    def __str__(self):
        return f"Rotation, {self.rotation}"

    def getData(self):
        return [self.rotation]

    def set_default_Rotation(self):
        Activity.rotation = self.rotation


def calculate_height(activities):
    rot = 90
    heights = [0]
    baseline = 0

    for a in activities:
        if isinstance(a, Rotation):
            rot = a.rotation
        elif isinstance(a, (Activity, Milestone, Nrow)):
            nrow = a.getNrow()
            heights.append(baseline + (nrow if rot in (None, 90) else 1))
        elif isinstance(a, AdvanceRow):
            baseline -= a.drow

    return max(heights)


def show_activities(activities, height=0.1, fontsize=7,
                    rowSpacing=0.5, show_today=True, show_time_axis=True,
                    title="", show_milestone_vlines=True,
                    startDate=None, endDate=None, show_weeks=True):
    """Plot a set of activities

    activities: list of list of Activities
    height:  height of each activity bar
    fontsize: fontsize for labels (passed to plt.text)
    show_today: indicate today by a dashed vertical line

    In general each inner list of activities is drawn on its own row but you can
    modify this by using pseudo-activity `AdvanceRow`.  Also
    available is `Color` to set the default colour (and optionally border)
    N.b. `Color(c)` resets the border, `Activity(..., color=c)` does not

    E.g.
        activities = [
            [
                Color("white", border='red'),
                Activity("A", "2021-02-28", 35),
                Activity("B", "2021-04-10", "2021-05-10")
            ], [
                Color("blue"),
                Activity("C", "2021-01-01", 30),
                Activity("D", "2021-01-20", "2021-04-01", drow=1),
                AdvanceRow(1),
            ], [
                Activity("E", "2021-01-05", "2021-01-31", color="green"),
            ],
        ]
"""

    if not startDate:
        startDate = "1958-02-05"
    if not endDate:
        endDate = "2099-12-31"

    Activity.height = height
    Activity.fontsize = fontsize
    Milestone.axvline = show_milestone_vlines

    if re.search("^[-+]?\d+$", startDate):  # a date relative to now, in days
        nday = int(startDate)
        startDate = datetime.now() + timedelta(days=nday)
    elif isinstance(startDate, str):
        startDate = datetime.fromisoformat(startDate)

    if re.search("^[-+]?\d+$", endDate):    # a date relative to now, in days
        nday = int(endDate)
        endDate = datetime.now() + timedelta(days=nday)
    elif isinstance(endDate, str):
        endDate = datetime.fromisoformat(endDate)

    dateMin = None
    dateMax = None
    for aa in activities:
        for a in aa:
            if isinstance(a, Manipulation):
                continue

            t0 = a.t0
            t1 = a.t0 + a.duration

            if t1 < startDate:
                continue
            if t0 < startDate:
                t0 = startDate

            if t0 > endDate:
                continue
            if t1 > endDate:
                t1 = endDate

            if dateMin is None or t0 < dateMin:
                dateMin = t0
            if dateMax is None or t1 > dateMax:
                dateMax = t1

    if dateMax is None:
        totalDuration = 0
    else:
        totalDuration = dateMax - dateMin  # used in line-wrapping the labels
    #
    # Count the number of rows of activities in the figure
    #
    nrowTot = 0
    for aa in activities:
        nrowTot0 = nrowTot
        nrowTot += calculate_height(aa)

    Activity.row = 0
    for aa in activities:
        Activity.nrow = 0
        Activity.row -= calculate_height(aa) + rowSpacing

        for a in aa:
            if isinstance(a, Manipulation):
                if isinstance(a, AdvanceRow):
                    Activity.row -= a.drow
                elif isinstance(a, Rotation):
                    a.set_default_Rotation()
                elif isinstance(a, Nrow):
                    a.set_default_Nrow()
                else:
                    raise NotImplemented(a)

                continue

            a.draw(totalDuration=totalDuration, nrowTot=nrowTot,
                   startDate=startDate, endDate=endDate)

    if show_today and datetime.now() > startDate:
        plt.axvline(datetime.now(), ls='--', color='black', alpha=0.5, zorder=-1)
    plt.grid(axis='x')

    if not show_time_axis:
        plt.xticks(ticks=[], labels=[])
    if True:                            # turn off y-axis labels
        plt.yticks(ticks=[], labels=[])

    ax = plt.gca()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %H:%M:%S.02 ')

    ax.tick_params('x', top=True, labeltop=True)

    plt.gcf().autofmt_xdate(ha='center')   # rotate and make space; center works at top and bottom

    if show_weeks:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))

        startDate, endDate = [datetime.utcfromtimestamp(x) for x in ax.set_xlim()]

        daylen = timedelta(days=1)
        for i in range(((endDate + 2*daylen) - (startDate - 2*daylen)).days):
            d = startDate + i*daylen
            if d.weekday() in [5, 6]:
                pos = mdates.date2num(d)
                ax.axvspan(pos - 0, pos + 1, color='lightgray', zorder=-10)

    if title:
        plt.title(title)

    plt.tight_layout()


def add_legend(categoryColors, activities=None, categoryGrouping=None, legend_location=None):
    """Add a legend to a show_activities() plot
    categoryColors: dict mapping categories to colours
    activities: list of activities shown; if None assume that all categories are present
    categoryGrouping: list of lists giving the order of categories; if None, alphabetical
    legend_location: location of legend; `loc` parameter to plt.legend
    """
    # Lookup which colours are actually used
    if activities is None:
        usedColors = None               # assume all are used
    else:
        usedColors = set([a._color for a in sum(activities, []) if
                          isinstance(a, Activity) and not isinstance(a, Milestone)])

    if categoryGrouping is None:
        categoryGrouping = [sorted(categoryColors)]

    # Construct a legend in the order of categoryGrouping
    handles = []
    for cc in categoryGrouping:
        for c in cc:
            color = categoryColors.get(c)
            if isinstance(color, str):
                border = None
            else:
                color, border = color

            if usedColors is None or color in usedColors:
                handles.append(patches.Polygon([(0,0), (10,0), (0,-10)],
                                               facecolor=color, edgecolor=border,
                                               label=f"{c.replace('_', ' ')}"))
    # and add it to the figure
    plt.legend(handles=handles, loc=legend_location)

    plt.tight_layout()


def p6dateStrToIso(dateStr):
    """Convert a date string such as "5-Feb-58" to ISO standard "2058-02-05"

    Not Y2K compliant!
    """
    if re.search(r"^\d{4}-\d{2}-\d{2}", dateStr):
        return dateStr

    dateStr = re.sub("(\s+A|\*)$", "", dateStr) # "Actual"; Kevin Long says to ignore it

    day, monName, year2 = dateStr.split('-')
    day = int(day)
    year2 = int(year2)

    mon = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)[monName]

    return f"20{year2}-{mon:02}-{day:02}"


def read_activities_from_P6(fileName, milestonesFileName=None, categoryGrouping=None, specials={},
                            nRowOfMilestones=5, milestoneHeight=4, ignoreZeroLengthActivities=False,
                            categoryColors={}, categoryNrow={}, wrappedDescrip={}):
    """Read Kevin Long's csv dump from P6

The file's in the format:
...

Summary Chart,Activity ID,Start,Finish,Total Float,Original Duration
M1M3.Install M1M3 with Surrogate,Summit-K1310,17-Jan-23,30-Jan-23,0,10
...
M1M3.Install M1M3 with Surrogate,SUMMIT-1923,7-Feb-23,13-Feb-23,0,5
M1M3.FunctionalTesting with Surrogate,SUMMIT-1927,7-Mar-23,13-Mar-23,0,5
...
M1M3.FunctionalTesting with Surrogate,SUMMIT-1929,14-Mar-23,15-Mar-23,0,2
M1M3.Dynamic Testing with Surrogate,SUMMIT-1928,23-Mar-23,19-Apr-23,0,20
...
M1M3.M1M3 on TMA + Thermal control t,SUMMIT-1909,5-Mar-24,15-Mar-24,0,9
M2.M2 functional testing  on TMA,SUMMIT-1916,24-Jul-23,4-Aug-23,0,10
...
M2.M2 on TMA + reintallation,SUMMIT-3081,10-Jul-23,21-Jul-23,0,10
Refrigeration PathFinder.prep & test  on TMA,SUMMIT-3013,,22-Mar-23,352,0
...
    """

    activities = {}
    celebratory = []
    with open(fileName, newline='\n') as fd:
        csvin = csv.reader(fd, skipinitialspace=True)

        for lineNo, line in enumerate(csvin, 1):
            if False:
                print(lineNo, line)

            if lineNo == 1:
                continue

            summary_chart, aid, start, finish, celebrate = line
            #
            # handle dates
            start = None if (start == 'None' or start is None) else start
            finish = None if (finish == 'None' or finish is None) else finish

            if ignoreZeroLengthActivities:
                if start is None or finish is None:
                    continue

            if start is None:
                if finish is None:             # HACK
                    print(f"Skipping {lineNo}: {line}")
                    continue
                else:
                    start = finish
            elif finish is None:
                finish = start
    
            start = datetime.fromisoformat(p6dateStrToIso(start))
            finish = datetime.fromisoformat(p6dateStrToIso(finish))
            #
            # Is it a celebratory milestone rather than an activity?
            #
            if celebrate.lower() in ("top", "y"):  # it's a celebratory milestone
                if celebrate.lower() == "y":
                    continue

                celebratory.append((aid, finish))
                continue

            if '.' not in summary_chart:
                summary_chart = f"{summary_chart}.{summary_chart}"

            category, descrip = summary_chart.split(".")
            category = category.replace(' ', '_')

            if "," in descrip:
                descrip = f'"{descrip}"'

            if category not in activities:
                activities[category] = {}

            if descrip not in activities[category]:
                activities[category][descrip] = []

            activities[category][descrip].append((aid, start, finish))

    summaries = {}
    row = 1
    for category in activities:
        summaries[category] = []

        nrow = categoryNrow.get(category, 5)
        nrow, rot = (nrow, None) if isinstance(nrow, int) else nrow

        summaries[category] = [Nrow(nrow), Rotation(rot)]

        color = categoryColors.get(category)
        if color is None:
            print(f"No colour is defined for category {category}", file=sys.stderr)
            color = ("white", "red")
        color, border = (color, None) if isinstance(color, str) else color

        row += 1

        for descrip in sorted(activities[category]):
            aids =          [aid    for (aid, start, finish) in activities[category][descrip]]
            start =  np.min([start  for (aid, start, finish) in activities[category][descrip]])
            finish = np.max([finish for (aid, start, finish) in activities[category][descrip]])

            if descrip in specials:
                nrow, rot, advanceRow = specials[descrip]
                if nrow is not None:
                    summaries[category].append(Nrow(nrow))
                if rot is not None:
                    summaries[category].append(Rotation(rot))
                if advanceRow is not None:
                    summaries[category].append(AdvanceRow(advanceRow))

            if descrip[0] == '"' and descrip[-1] == '"':
                descrip = descrip[1:-1]

            summaries[category].append(Activity(descrip, start, finish, color, border,
                                                wrappedDescrip=wrappedDescrip.get(descrip)))

    #
    # Order/group according to grouping[]
    if categoryGrouping is not None:
        _summaries = []
        for cats in categoryGrouping:
            sub = []
            for cat in cats:
                for a in summaries[cat]:
                    sub.append(a)

            _summaries.append(sub)

        summaries = _summaries

    if False:
        if milestonesFileName is not None:
            milestones = read_celeb_milestones(milestonesFileName,
                                               nRowOfMilestones=nRowOfMilestones, milestoneHeight=milestoneHeight)
            summaries = [milestones] + summaries
    else:
        Milestone.height = milestoneHeight
        Milestone.rotation = 0

        milestones = []
        for c in celebratory:
            name, start = c
            milestones.append(Milestone(name, start))

        milestones = sorted(milestones, key=lambda a: a.t0)
        for i, ml in enumerate(milestones):
            ml.drow = i%nRowOfMilestones

        milestones.append(AdvanceRow((nRowOfMilestones - 1)*milestoneHeight))

        summaries = [milestones] + summaries

    return summaries, activities


def print_details(inputs, systems=None, fd=None, indent="   "):
    """Print the details of cartoon boxes

    E.g.
       activities, inputs = read_activities_from_P6(...)
       print_details(inputs, fd=None, systems=["Calibration"])
    """
    if fd is None:
        fd = sys.stdout

    if systems is not None and isinstance(systems, (list, tuple)):
        systems = set(systems)

    for system, aa in inputs.items():
        system = system.replace('_', ' ')

        if systems is not None and system not in systems:
            continue
        print(system, file=fd)
        for descrip, cpts in aa.items():
            print(f"{indent}{descrip}", file=fd)
            for (aid, start, finish) in sorted(cpts, key=lambda x: x[2]):
                print(f"{2*indent}{aid:20} {str(start).split(' ')[0]} -- {str(finish).split(' ')[0]}", file=fd)

