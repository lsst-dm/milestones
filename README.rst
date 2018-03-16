########################
LSST DM Milestone Munger
########################

Given inputs from PMCS and elsewhere, transform them into LaTeX snippets or
other formats suitable for inclusion in DM documentation.

Usage
=====

Execute ``milestones.py``. For example::

  $ python milestones.py --help
  usage: milestones.py [-h] [--pmcs-data PMCS_DATA] [--local-data LOCAL_DATA]
                       {standalone,ldm503,ldm564} ...

  Prepare DM milestone summaries.

  optional arguments:
    -h, --help            show this help message and exit
    --pmcs-data PMCS_DATA
                          Path to PMCS Excel extract. [Default=...]
    --local-data LOCAL_DATA
                          Path to local annotations. [Default=...]

  Output targets.:
    {standalone,ldm503,ldm564}
      standalone          Output standalone material.
      ldm503              Output for LDM-503.
      ldm564              Output for LDM-564.

Each target (``standalone``, ``ldm503``, etc) may take further command
line options to specify its output.

Data
====

Milestone summaries are generated based on two sources of input data:

- An Excel sheet, extracted from PMCS (Primavera);
- A JSON file, ``data/local.json``, containing additional information
  contained in this package.

The Excel sheet is generated from within Primavera as follows:

- Load the project to be exported;
- Select File→Export;
- Select “Spreadsheet - (XLS)” and hit “Next”;
- Select “Activities” and “Activity Relationships” and hit “Next”;
- Select the open project, and hit “Next”;
- Select template “DM All Milestones” and hit “Next”;
- Review the name of the file to be exported, and hit “Next”;
- Hit “Finish”;
- Commit the file to the ``data/pmcs`` directory of this repository.

The PMCS export files should be named according to the pattern
``YYYYMM-<type>.xls``, where ``YYYY`` is the (calendar) year, ``MM`` the
month, and ``<type>`` is either ``ME`` (representing the forecast project for
a particular month ending) or ``BL`` (for the baseline project for a
particular month). For example, ``201802-ME.xls`` is the forecast for
month-ending February 2018.

Note that LSST convention is that the forecast projects contain information
about the completion status of activities, so they are almost always more
useful than the baseline projects.

The ``local.json`` annotations may be edited as needed and the results
committed to this repository.

Milestone semantics
===================

Milestones — or rather, instances of the ``Milestone`` class provided in
this package — have a number of associated attributes. These are:

``code``

   The “activity ID” or “task code” from PMCS, e.g. “LDM-503-01”, “DM-NCSA-23”,
   “CAMM6995”, etc. We use this for cross-referencing data sources.

   Note that we normalize the LDM-503-n milestones to have two digit numbers
   (ie, “LDM-503-01”, not “LDM-503-1”). This follows the convention used in
   PMCS. (For whatever reason, other milestones have not been normalized in
   the same way — PMCS uses e.g. “DM-AP-1”).


``name``

   A short summary of the milestone, e.g. “System First Light”, “Start of Full
   Science Operations”.

   In most cases, this corresponds to the “activity name” in PMCS. However, on
   occasion, this has been used as a reference to some other lookup table
   (e.g. “DRP-MS-INT-1”). In these cases, we set the milestone name to some
   more descriptive value (stored in the ``local.json`` in this package), and
   the Milestone's ``aka`` attribute (see below) to a list of alternative IDs.

``description``

   A lengthier overview of the milestone. May be blank.

   Descriptions are provided in the ``local.json`` file in this packge.

``comment``

   Any additional information provided for this milestone. Expected to contain
   things like implementation notes for LDM-503. May be blank.

   Will be sourced from ``local.json``.

``aka``

  “Also Known As”. Any other IDs by which this milestone might be identified
  (e.g. “DRP-MS-INT-1”).

  Will be sourced from ``local.json``. Should always be an iterable, but may
  be empty.

``test_spec``

   A reference to the *document handle*, *version*, *section* and *name* of the
   test specification which is used to test this milestone, if applicable.

   The master copy of this information lives in this repository.

``predecessors``

   A list of the codes of milestones which must be completed before this one.

   Sourced from PMCS. Should always be an iterable, but may be empty.

``successors``

   A list of milestone codes for which this milestone is a prerequisite.

   Sourced from PMCS. Should always be an iterable, but may be empty.

``due``

   The date by which the milestone is scheduled for completion.

   Sourced from PMCS.

``completed``

   The date on which the milestone was recorded as completed, or ``None`` if
   the milestone remains incomplete.

   Sourced from PMCS.

``short_name``

   A shortened form of the milestone name, which may be useful e.g. when using
   it to label figures. If not set, it defaults to being equal to ``name``.

   Source from ``local.json``.
