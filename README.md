***TESTING FALFILFA***
======================

The purposes of these tests are:

- checking that the LFI format implementation works **and** is backward compatible 
- checking that the GRIB edition 2 encoding works **and** gives results identical for metadata encoding **and** gives sensible results for data encoding

GRIB 2 metadata are used in operations to distribute and interpret GRIB data. These metadata should **not** change without an explicit agreement
from our operations. 

Note that change in metadata may come either from:
- changes in the FA library
- changes in eccodes


**Test IO server output retrieval**
===================================

***Polling IO server output***
------------------------------

The output of the IO server is polled using the io_poll script, itself
relying on the lfitools executable.

Polling the IO server output returns a list of historic files and 
GRIB files which are ready for further processing or archiving. These
files are assembled from the files existing in each pool of the IO server.


***Test and compare to reference data***
----------------------------------------

Once historic files and GRIB indexes are created, they are compared to 
a reference packaged with the test case.

The test data are in the io_serv subdirectory.

**Test GRIB edition 2 metadata encoding**
=========================================

***Metadata encoding***
-----------------------

GRIB messages are made of several sections:

- Local section
- Product definition section; which parameter (T, U, V, etc.)
- Geometry definition section (size and limits of the domain)
- Data section (values of the field)

The test series of grib2meta tests the encoding of everything but the data section. 

All Météo-France production of field data relies on the encoding performed by the 
FA library; therefore it is mandatory to keep these metadata constant, as product
dissemination rely on these metadata for identification.

***Configuration files***
-------------------------

Mapping names of FA fields to GRIB keys is performed using the following configuration files:

- faModelName.def
- faLevelName.def
- faFieldName.def

How exactly this mapping occurs relies on eccodes capabilities and is described 
in the section 4.8 of the document encoding_PM_2015.pdf.

The test cases of grib2meta are delivered with configurations files taken 
from Météo-France operational configuration based on cycle 48t1, and
are located in the extra_grib_defs subdirectory.

***Description of the test case***
----------------------------------

The test data of grib2meta have been collected after running a set of Olive experiments
designed to span the whole range of possible field output created by Météo-France
production. The fields have been collected for their metadata, and the values themselves
have been set to zero.

For each file of the data set, we perform the following actions:

- read the names of fields contained in the current file
- for each field, encode a zero-valued field in another file
- compare the GRIB message with the original message using ldifidiff and grib_dump

For now, test data are available both in single and double precision, as small
differences may exists between these two representations.

Test data are in the grib2meta subdirectory (single and double precision).

**Test GRIB edition 2 data encoding**
=====================================

Test data are in the grib2data subdirectory (single and double precision).

***Spectral data***
-------------------

- ARPEGE spectral coefficients; a subtruncation is encoded using IEEE 64 or 32 bits, as in the model.
- AROME spectral coefficients; a subtruncation is encoded using IEEE 64 or 32 bits, as in the model.

Spectral data is encoded using INGRIB=123 (simple packing with a laplacian modulation), and a 
non-compacted subtruncation whose size is determined by the FA library.

***Model grid-point data***
---------------------------

- ARPEGE grid-point fields
- AROME grid-points fields
- SURFEX (ARPEGE + AROME) grid-point fields, with missing data (enables GRIB bitmap)

Grid-point data is encoded with INGRIB=123 (simple packing).

***Latitude/longitude grid-point data***
----------------------------------------

- global lat/lon data
- regional lat/lon data, with/without missing values

Lat/lon data is encoded with INGRIB=141 (simple packing followed by second order packing).

**Test LFI utilities**
======================

Check the following scripts (wrapping lfitools) work:

- lfi_merge; merge several LFI files into a single one
- lfi_copy; smart copy of a LFI file
- lfi_pack; pack multiple LFI files into a single one


**Test LFI format**
===================

This test case (lfiformat) opens a LFI file and performs a random (but reproducible) list 
of 10000 operations:

- add a new record
- remove an existing record
- rename an existing record

The result file is then compared to a reference.

