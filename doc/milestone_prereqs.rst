LDM-503-01: Science Platform w/ WISE data in PDAC
=================================================

- DM-SUIT-3 Time series analysis tool for WISE data
- DM-SQRE-1 Project internal Jupyter notebook service
- DM-DAX-1 WISE data ingest to PDAC
- DM-SUIT-1 Search and display WISE sources (objects) in PDAC
- DM-SUIT-2 Search WISE coaded data single exposure images in PDAC (the images are from IRSA at IPAC, not NCSA)
- DM-SUIT-4 Multiple data traces in chart space

LDM-503-02: HSC reprocessing
============================

- DM-DRP-1 HSC merger complete: all functionality deployed for the most recent HSC data release processing is now available within the LSST stack.
- DM-NCSA-1 Provide regular reprocessing service for HSC data
- DM-NCSA-2 Provide access to results of regular reprocessing (NB the form this takes depends upon available DAX functionality)
- DM-AP-1 Basic single frame measurement pipeline.
- DM-DRP-2 Basic visualization and quality assessment tools operational on HSC-scale data volumes.
- DM-NCSA-3 Provide database for metadata, provenance, location and demonstrate ingest at small scale

LDM-503-03: Alert Generation
============================

- DM-AP-1 Basic single frame measurement pipeline.
- DM-AP-2 Alard & Lupton-style image differencing.
- DM-AP-3 Point source & dipole measurement on difference images.
- DM-AP-4 DIASource association
- DM-AP-5 DIAObject generation
- DM-DAX-6 Prototype level 1 database

LDM-503-04: AuxTel DAQ integration
==================================

- DM-NCSA-4 Minimal support for the small operational schema including file metadata and provenance for every file, and record of in
- DM-DAX-7 Butler interface to retrieve images from data backbone

LDM-503-04b: AuxTel DAQ interface verification
==============================================

- DM-NCSA-27 Deliver header service code
- DM-NCSA-6 Ability to transfer files originating from Tucson to NCSA and ingest files at NCSA, including metadata and provenance
- DM-NCSA-5 Level 1 archiving system able to acquire pixel data from the Aux Tel DAQ, header metadata via OCS, assemble FITS image,
- DM-NCSA-7 Capability to paint displays for Tucson and NCSA
- LDM-503-04 Test report: Aux Tel DAQ integration functionality test

LDM-503-05: Alert distribution validation
=========================================

- LDM-503-03 Test report: Alert generation validation
- (Query) F18S F18 Start
- (Query) DM-NCSA-8 Test instance of feeds to LSST mini broker in online (live stream) and offline (replaying from files) modes
- (Query) DM-NCSA-9 Test instance of alert distribution hosting service and L1 database in Development & Integration Enclave

LDM-503-09a: Pipelines Release Fall 2018
========================================

- DM-AP-2 Alard & Lupton-style image differencing.
- DM-AP-3 Point source & dipole measurement on difference images.
- DM-DRP-16 Global photometric fitting (e.g. Burke et al. Forward Global Calibration Method).
- DM-DRP-32 Object classification system available.
- DM-DRP-11 Pipelines code provides supports for database ingestion of results.
- DM-AP-7 Basic instrument signature removal (ISR) capability.
- DM-DRP-3 PSF-homogenized coadd construction.
- DM-DRP-38 Camera package supporting the Commissioning Camera.
- DM-DRP-5 Camera package supporting the LSST Camera.
- DM-DRP-7 Coordinate transformation tool provided for use with the Collimated Beam Projector.
- DM-AP-9 JOINTCAL1: Jointcal at a functional level
- DM-DRP-17 Simultaneous photometric and astrometric fitting to multiple exposures.
- DM-AP-6 Alert format defined & queue system available.
- (Query) DM-DAX-8 Supertask-based system capable of efficient processing across a full focal plane.

  - We are not holding this release based on SuperTask (or PipelineTask) functionality, so this has to be gone.

LDM-503-06: DM ComCam interface verification readiness (LDM-503-06)
===================================================================

- (Query) This is apparently blocked on DAQ availability. What milestone describes that? It's evidently not LSST-1200.
- LSST-1200 Interface Verification: Single Visit
- DM-NCSA-10 Sustained archiving service that is OCS commandable
- DM-NCSA-11 Verified acquisition of raw and crosstalk-corrected exposures at raft scale, incl. correct metadata

LDM-503-07: Camera Data Processing
==================================

- DM-DRP-4 Calibration product generation in support of basic ISR.
- LDM-503-01 Test report: Science Platform with WISE data in PDAC
- LDM-503-02 Test report: HSC reprocessing
- (Query) LDM-503-06 Test report: DM ComCam interface verification readiness

  - LDM-503-07 has already been completed with LDM-503-06 having been done, so
    this makes no sense.

LDM-503-09: Ops Rehearsal for Commissioning #1
==============================================

- (Query) DM-DAX-2 Query service supporting IVOA TAP protocol, w/ support for asynchronous queries
- (Query) DM-DAX-4 Metadata service supporting IVOA SIAv2 protocol
- (Query) DM-DAX-3 Image cutout service supporting IVOA SODA protocol
- (Query) DM-DAX-5 Database ingest in support of HSC reprocessing (ie, large catalog ingest)
- (Query) DM-SUIT-5 Search and display processed HSC data
- (Query) LDM-503-05 Test report: Alert distribution validation
- LDM-503-08b Small Scale CCOB Data Access
- (Query) DM-DAX-9 Provenance system, details TBD.

  - I can see we'd want some provenance for the Ops rehearsal, but I *don't* think we want to tie it to the details of Butler implementation.

- LDM-503-09a Test report: Pipelines Release Fall 2018
- DM-NCSA-17 QA on WCS, PSF, etc returned to Observatory using JupyterLab
- DM-NCSA-16 Perform ISR processing on ComCam-scale data.
- DM-SQRE-2 Commissioning notebooks running on the commissioning cluster
- DM-NCSA-19 8x7 incident response system
- LDM-503-07 Test report: Camera data processing

LDM-503-10b: Large Scale CCOB Data Access
=========================================

- CAMM8040 COMP: DAQ V4
- EIA-200 Main Camera 24-Hour Cycle
- (Query) Is it correct that this milestone has NO internal-to-DM
  prerequisites? It just happens when CAMM8040 and EIA-200 are done?

LDM-503-11b: Pipelines Release Fall 2019
========================================

- DM-DRP-14 Insertion of simulated sources into the data stream to check pipeline performance.
- DM-DRP-18 Initial multi-band deblending algorithm available.
- DM-DRP-8 Calibration product generation for the Auxiliary Telescope.
- DM-DRP-9 Data reduction pipeline for the Auxiliary Telescope.
- DM-DRP-10 Calibration products include an optical ghost model.
- DM-DRP-19 QA metrics are generated during pipeline execution.
- DM-DRP-33 Generation of coadded images suitable for use in EPO activities.
- DM-DRP-12 Background estimation over the full visit.
- DM-DRP-13 PSF estimation over the full visit.
- DM-DRP-15 All varieties of coadd required for object detection and characterization are now produced during normal pipeline operation (although not necessarily at the ultimately required level of fidelity).
- DM-DRP-29 Moving point source model fitting now available.
- DM-DRP-37 Artifact rejection and background matching during coadd construction.
- DM-AP-8 Advanced ISR, including ghost and linear feature masking, correction for the Brighter-Fatter effect and compensation for pixel response non-uniformity.
- DM-DRP-23 Atmospheric characterization based on data from the Auxiliary Telescope now available.
- DM-DRP-20 Refined set of LSST calibration products.
- DM-DRP-21 Integrated image characterization pipeline for Data Release Production.
- DM-AP-10 Advanced single frame measurement pipeline for Alert Production.
- (Query) LDM-503-10b Large Scale CCOB Data Access

  - Obviously, this release should not depend on LDM-503-10b.

LDM-503-11a: ComCam Ops Readiness
=================================

- (Query) DM-SUIT-10 SUIT deployment procedure

  - We should assume that all SUIT milestones are at risk and they shouldn't block anything.

- LDM-503-11b Test report: Pipelines Release Fall 2019
- DM-NCSA-20 ComCam Archiving Service
- DM-NCSA-21 L1 Offline Processing Service, Raft Scale, ComCam
- DM-NCSA-22 Information in consolidated database available to QA portal

LDM-503-08 Spectrograph Data Acquisiion
=======================================

- (Query) DM-DRP-6 Camera package supporting the Auxiliary Telescope.

  - This is Pipelines integration; presumably not necessary for this milestone.

- (Query) DM-NET-3 Initial Network Ready (Summit)

  - Is this acquiring spectrograph data from the lab or the mountain?

- (Query) DM-NET-6 Summit LAN installed
- (Query) DM-NET-2 Mountain - Base Network Functional 2 x 100 Gbps
- LDM-503-04b Test report: Aux Tel DAQ interface Integration Verification and Spectrograph Operations Rehearsal
- CAMM8300 COMP: Full production grade ADAQ system for DM at NCSA
- DM-NCSA-15 Batch Processing Service for offline spectrograph data processing
- (Query) DM-SUIT-9 Spectral data display

  - All SUIT miletones at risk.
  - Not obvious that visualization is necessary to complete LDM-503-08.

- (Query) DM-NCSA-12 EFD ETL Service

  - Is this necessary to complete LDM-503-08?
  - How does it relate to ongoing work in SQuaRE?

- DM-NCSA-13 Header Writing Service for Spectrograph use case
- (Query) DM-NCSA-14 Data Backbone endpoints in Chile for ingestion and access, distribution over WAN, ingest at NCSA into custodial file sto

LDM-503-10: DAQ validation
==========================

- (Query) the list below implies there is no additional on-DM deliverable for this milestone. Right?
- LDM-503-04 Test report: Aux Tel DAQ integration functionality test
- LDM-503-06 Test report: DM ComCam interface verification readiness
- EIA-130 Installation of Large-scale DAQ Client Cluster at NCSA
- LDM-503-08 Test report: Spectrograph data acquisition

LDM-503-11: Ops Rehearsal for Commissioning #2
==============================================

- (Query) DM-DAX-10 Middleware support for multifit

  - Clearly this is not a prereq for an Ops rehearsal.

- (Query) DM-NET-4 Base LAN installed

  - Would we block the rehearsal on this?

- LDM-503-09 Test report: Ops rehearsal for commissioning #1
- LDM-503-11b Test report: Pipelines Release Fall 2019
- LDM-503-08 Test report: Spectrograph data acquisition
- LDM-503-10 Test report: DAQ validation

LDM-503-12: Ops rehearsal for commissioning #3
==============================================

- (Query) DM-SQRE-3 Hardened Jupyter deployment on Commissioning Cluster

  - Should be defined in terms of LSP milestones, I guess.

- LDM-503-11a ComCam Ops Readiness
- LDM-503-11 Ops rehearsal for commissioning #2

LDM-503-12a: LSSTCam Ops Readiness
==================================

- (Query) CAMM8090 COMP: Camera Pre-Ship Review at SLAC

  - LDM-503-12a is a *DM* milestone: we should be able to declare DM's readiness for LSSTCam regardless of Camera Team milestones.
  - Note that we did not rely on external milestones for LDM-503-11a (ComCam readiness); this should be analogous.

- (Query) COMC-0030 Start Early Integration and Test

  - Ditto.

LDM-503-13: Ops rehearsal for data release processing #1
========================================================

- (Query) DM-SUIT-15 Alert subscription

  - SUIT milestones are at risk.
  - Alert subscription is not necessary for data release processing.

- (Query) DM-STAFF Staffing Checkpoint

  - Not relevant to DRP.

- LDM-503-12 Ops rehearsal for commissioning #3
- DM-NCSA-23 Operational processes for preparing for & producing a data release defined and tested
- LDM-503-13a Test report: Pipelines Release Fall 2020

LDM-503-13a: Pipelines Release Fall 2020
========================================

- DM-AP-11 Difference imaging includes noise decorrelation and correction for differential chromatic refraction.
- DM-DRP-22 Template generation integrated with Data Release Production pipelines.
- DM-DRP-26 Overlap resolution at tract & patch boundaries.
- DM-DRP-24 Physically motivated PSF model, including separate characterization of contributions from the atmosphere and the telescope system.
- DM-DRP-27 Object generation: association and assembly of (DIA, coadd, etc) sources to form objects.
- DM-DRP-30 Forced photometry is now performed on individual processed visit images during data releases.
- DM-DRP-28 Difference images are now a first-class data product during data release processing.
- DM-DRP-25 Prototype multi-epoch fitting system available.
- DM-DRP-34 Selection maps are generated during data releases.
- DM-AP-14 Alert filtering system available.
- DM-AP-12 Difference imaging is now agnostic to the PSF of the template image.
- DM-AP-13 Trailed source measurement on difference images.

LDM-503-14: DM Readiness for Science Verification
=================================================

- DM-SUIT-16 Commissioning DAC
- LDM-503-12 Ops rehearsal for commissioning #3
- DM-SQRE-4 Notebook service ready for verification & validation
- LDM-503-13 Ops rehearsal for data release processing #1 (ComCam data)
- LDM-503-13a Test report: Pipelines Release Fall 2020

LDM-503-15a: Pipelines Release Fall 2021
========================================

- DM-AP-15 Alert distribution system fully integrated.
- DM-AP-17 Moving object processing system (MOPS) available.
- DM-AP-16 Full integration of the Alert Production system within the operational environment.

LDM-503-15: Ops rehearsal for data release processing #2
=========================================================

- (Query) DM-SQRE-5 Notebook service ready for general science users

  - Not relevant to DRP.

- LDM-503-13 Ops rehearsal for data release processing #1 (ComCam data)
- DM-NCSA-25 Demonstrate operational coordination with and processing at satellite CC-IN2P3 satellite computing facility
- DM-NCSA-24 Production batch service for data release processing

LDM-503-16: Ops rehearsal for data release processing #3
========================================================

- LDM-503-15 Ops rehearsal for data release processing #2
- DM-NCSA-26 Demonstrate full delivery of Data Facility ConOps

LDM-503-17a: Final Pipelines Delivery
=====================================

- LDM-503-15a Test report: Pipelines Release Fall 2021

LDM-503-17: Final Operations Rehearsal
======================================

- LDM-503-16 Ops rehearsal for data release processing #3
- LDM-503-17a Test report: Final Pipelines Delivery
