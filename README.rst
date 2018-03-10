########################
LSST DM Milestone Munger
########################

Given inputs from PMCS and elsewhere, transform them into LaTeX snippets or
other formats suitable for inclusion in DM documentation.

Sources of milestone information
================================

- Exports from Primavera/PMCS;

  - Note that from PMCS we can dump from either the “baseline” or “forecast”
    projects.
  - Baseline provides the latest thinking about the schedule, but is devoid of
    completion status.
  - Forecast is updated later, but contains completion dates.

- Dump of the old Google ``master milestone list``;
- Annotations stored in this package.

Output formats
==============

- Gantt chart-like figure, to be included in the ``lsst-dm/images`` repository
  and embedded in LDM-503 and perhaps elsewhere.
- LDM-503 schedule table.
- LDM-503 milestone summary section.
- LDM-564 release list.

Formatting note
===============

All text fields are assumed to contain text which might be displayed by LaTeX.

Milestone terminology
=====================

Code:

   The “activity ID” or “task code” from PMCS, e.g. “LDM-503-01”, “DM-NCSA-23”,
   “CAMM6995”, etc. We use this for cross-referencing data sources.

   Note that we normalize the LDM-503-n milestones to have two digit numbers
   (ie, “LDM-503-01”, not “LDM-503-1”). This follows the convention used in
   PMCS. (For whatever reason, other milestones have not been normalized in
   the same way — PMCS uses e.g. “DM-AP-1”).

Name:

   A short summary of the milestone, e.g. “System First Light”, “Start of Full
   Science Operations”.

   In most cases, this corresponds to the “activity name” in PMCS. However, on
   occasion, this has been used as a reference to some other lookup table
   (e.g. “DRP-MS-INT-1”). The lookup table is (currently) stored on GDocs; we
   should automatically replace these with helpful names based on that.

Description:

   A lengthier overview of the milestone.

   For LDM-503-n (level 2) milestones, this was provided in the original
   LDM-503 text and should be recorded in this repository.

   For other milestones (DM level 3 & 4, other subsystems), it may not be
   available (the “description” field in the GDocs sheet was used to populate
   the “name” in PMCS; more detailed descriptions were not required). If
   available, it will also be recorded in this repository.

   May be blank.

Comment:

   Any additional information provided for this milestone. Expected to contain
   things like implementation notes for LDM-503.

   Will be sourced from this repository.

   May be blank.

AKA:

  “Also Known As”. Any other IDs by which this milestone might be identified
  (e.g. “DRP-MS-INT-1”).

Test Spec:

   A reference to the *document handle*, *version*, *section* and *name* of the
   test specification which is used to test this milestone, if applicable.

   The master copy of this information lives in this repository.

Predecessors:

   A list of the codes of milestones which must be completed before this one.

   Sourced from PMCS. Should always be an iterable, but may be empty.

Successors:

   A list of milestone codes for which this milestone is a prerequisite.

   Sourced from PMCS. Should always be an iterable, but may be empty.

Due date:

   The date by which the milestone is scheduled for completion.

Completion date:

   The date by which the milestone was recorded as completed.

   ``None`` if the milestone remains incomplete.
