########################
DM Milestone Information
########################

This repository contains:

- Excel sheets describing milestones extracted from Primavera;
- Local annotations, which are used to augment or override the information in Excel sheets;
- Code for manipulating and analyzing the milestone data.

Milestone Semantics
===================

This package provides a ``Milestone`` class, instances of which represent each milestone.
Each instance of ``Milestone`` provides at least the following information:

``code``

   The “activity ID” or “task code” from PMCS, e.g. “LDM-503-01”, “DM-NCSA-23”, “CAMM6995”, etc.

``name``

   A short summary of the milestone, e.g. “System First Light”, “Start of Full Science Operations”.

``wbs``

  The WBS element which contains the milestone.
  This starts at the *second* level of WBS (e.g. “02C”), and may proceed arbitrarily deep (e.g. “02C.04.03”).

``due``

  The due date for this milestone, as an instance of ``datetime.datetime``.

``completed``

  The date on which the milestone was completed, as an instance of ``datetime.datetime``.
  If the milestone is not complete, this will be ``None``.

``predecessors``

  The set of all milestone codes which are immediate predecessors of this milestone.
  This is *not* transitive: if ”B” is listed as a predecessor of “A”, and “C” as a predecessor of ”B”, then “C” will not appear in the predecessor list for “A”.
  This set may be empty.

``successors``

  The set of all milestone codes which are immediate successors of this milestone.
  This is *not* transitive: if ”B” is listed as a successor of “A”, and “C” as a successor of ”B”, then “C” will not appear in the successor list for “A”.
  This set may be empty.

``aka``

  The set of alternative codes by which this milestone has been referred to in the documentation.
  This set may be empty.

``description``

  An extended description of the milestone.
  May be ``None``.

``comment``

  Any additional commentary attached to this milestone, such as implementation notes.
  May be ``None``.

``short_name``

  A shortened form of the milestone name, for use when space is constrained (e.g. in figures).
  Defaults to ``name`` if not explicitly set.

``test_spec``

  The test specification document handle corresponding to this milestone.
  May be ``None``.

``jira_testplan``

  The Jira issue ID corresponding to delivery of the test plan for this milestone.
  May be ``None``.

``jira``

  The Jira issue ID corresponding to completion of this milestone.
  May be ``None``.

Data Sources
============

The ``data`` directory contains:

- One Excel sheet per calendar month, named following the pattern ``pmcs/YYYYMM-ME.xls``.
  These files are extracted from Primavera as described below.
- Local annotations stored in YAML format in the file ``local.yaml``.

The Excel sheets are used to populate the ``code``, ``name``, ``wbs``, ``due``, ``completed``, ``predecessors`` and ``successors``  fields for each milestone.
If one of these fields is specified in ``local.yaml``, then the value derived from PMCS is discarded, and the local value is used instead.
A warning is printed in this case.

The other fields are populated based on the contents of ``local.yaml``, without reference to Primavera.

Extracting information from Primavera
-------------------------------------

The Excel sheet is generated from within Primavera as follows:

#. Load the project to be exported.
   Note that we always use the “forecast” project, not the “baseline”.
   Look for a project named similarly to “LSST ME 20-06” (*not* “LSST BL 20-06”).
#. Select File→Export.
#. Select “Spreadsheet - (XLS)” and hit “Next”.
#. Select “Activities” and “Activity Relationships” and hit “Next”.
#. Select the open project, and hit “Next”.
#. Select template “All Milestones and Tasks” and hit “Next” (its near the very end of the list).
#. Review the name of the file to be exported, and hit “Next”.
#. Hit “Finish”.
#. Commit the file to the ``data/pmcs`` directory of this repository.

Command-Line Usage
==================

Ensure the prerequisites listed in ``requirements.txt`` are installed.
For example::

  $ pip install -r requirements.txt

Then execute ``python milestones.py --help`` for a listing of available functionality::

  $ python milestones.py --help
  usage: milestones.py [-h] [--pmcs-data PMCS_DATA] [--local-data LOCAL_DATA] [--verbose] {gantt,burndown,csv,jira,delayed,remaining,predecessors,graph} ...

  Prepare DM milestone summaries.

  optional arguments:
    -h, --help            show this help message and exit
    --pmcs-data PMCS_DATA
                          Path to PMCS Excel extract; default=data/pmcs/YYYYMM-ME.xls
    --local-data LOCAL_DATA
                          Path to local annotations; default=data/local.yaml.
    --verbose, -v

  Output targets:
    {gantt,burndown,csv,jira,delayed,predecessors,graph}
      gantt               Generate Gantt chart.
      burndown            Generate milestone burndown chart.
      csv                 Generate a CSV version of the milestone schedule.
      jira                Sync milestone details to Jira.
      remaining           Print a list of remaining milestones.
      delayed             Print a list of delayed milestones.
      predecessors        List each milestone with its predecessors
      graph               Generate Graphviz dot showing milestone relationships.

Note that by default the Excel spreadsheet corresponding to the most recent month is used, but this can be changed using the ``--pmcs-data`` command line option.

Each of the various “output targets” listed provides a different output format.
For example, to produce a “burndown chart” comparing the number of milestones completed with time against the baseline plan, execute::

  $ python milestones.py burndown

Each target has its own ``--help`` option which describes any target-specific options::

  $ python milestones.py burndown --help
  usage: milestones.py burndown [-h] [--start-date START_DATE] [--end-date END_DATE] [--output OUTPUT]

  optional arguments:
    -h, --help            show this help message and exit
    --start-date START_DATE
                          Start date for the burndown chart (YYYY-MM-DD); default=2016-10-30.
    --end-date END_DATE   Start date for the burndown chart (YYYY-MM-DD); default=2022-06-30.
    --output OUTPUT       Filename for output; default={filename}.
    --prefix PREFIX       List of prefixes for burndown milestones.

Hence to produce the SITCOM type burn down we use::

  $  python milestones.py burndown --prefix "SIT COM SUM" --output SIT-COM-SUMburndown.png


GitHub Artifacts
================

On push to this repository, some of the artifacts produced by the ``milestone.py`` script are automatically compiled and made available for download.
These are available from the `Generate Artifacts workflow <https://github.com/lsst-dm/milestones/actions?query=workflow%3A%22Generate+artifacts%22>`_; choose the latest run on the branch you are interested in.

All of the documents with PRs made by this action now have Auto-Merge enabled hence they all update when a change is pushed to this milestones repo. 
