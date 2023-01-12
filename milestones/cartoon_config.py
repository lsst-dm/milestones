#
# Configuration for the cartoon, imported by blockschedule.py
#
__all__ = ["categoryNrow", "categoryGrouping", "categoryColors",
           "specials", "wrappedDescrip", "nRowOfMilestones",
           "milestoneHeight", "milestoneWidth",
           "legend_location", "today_height"]


nRowOfMilestones = 3                    # number of rows of milestones
milestoneHeight = 4                     # height of each row of milestones
milestoneWidth = 20                     # width of labels; used to wrap text
legend_location = (0.83, 0.02)          # plt.legend(loc=legend_location)
today_height = 0.5                      # height of today's label; fraction of y-axis

#
# Number of rows needed for boxes, and rotation (0 or 90 degrees; 90 is the default)
#
categoryNrow = dict(
    AuxTel=(4, 0),
    Calibration=17,
    ComCam=13,
    Commissioning=15,
    Dome=(3, 0),
    LSSTCam=27,
    M1M3=30,
    M2=30,
    Refrigeration_PathFinder=(8, 0),
    TMA_Verification=(2, 0),
)
#
# Tweak specific activities;  (nrow, rotation, advanceRow)
#
specials = {
    "Dome": (None, None, -6),
    "Light Windscreen": (None, 0, 3),
    "Ring Gear Install": (None, None, 3),
    "Calibration Screen": (None, None, 9+2),
}
#
# Group categories onto single lines, and define the order that the categories
# are laid out (top to bottom)
#
categoryGrouping = [
    ("Dome",),
    ("Calibration", "TMA_Verification",),
    ("M1M3", "M2", "Commissioning",),
    ("ComCam",),
    ("Refrigeration_PathFinder",),
    ("LSSTCam",),
    ("AuxTel",),
]
#
# Colours for categories; when a tuple the second colour is the border colour
#
categoryColors = dict(
    AuxTel="goldenrod",
    Calibration="orchid",
    ComCam=("cornflowerblue", "black"),
    Commissioning=("moccasin", "black"),
    Dome=("mistyrose", "brown"),
    LSSTCam=("powderblue", "skyblue"),
    M1M3=("indianred", "brown"),
    M2=("lightgreen", "green"),
    Refrigeration_PathFinder=("lavender", "black"),
    TMA_Verification=("sandybrown", "black"),
)
#
# Override descriptions that the code wraps badly
#
wrappedDescrip = {
    "ComCam Off TMA on Cart": "ComCam Off\nTMA on Cart",
}
