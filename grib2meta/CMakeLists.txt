# (C) Copyright 2022- ECMWF.
# (C) Copyright 2022- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

if(HAVE_DOUBLE_PRECISION)
include(ListTests_dp.cmake)
set (LFITOOLS ${CMAKE_BINARY_DIR}/bin/lfitools_dp)
endif()

if(HAVE_SINGLE_PRECISION)
include(ListTests_sp.cmake)
set (LFITOOLS ${CMAKE_BINARY_DIR}/bin/lfitools_sp)
endif()

file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/tests_results)
file(REMOVE_RECURSE ${CMAKE_BINARY_DIR}/tests_results/grib2meta/)
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/tests_results/grib2meta/)

foreach( f ${LIST_TESTS})

add_test(NAME ${f}
    COMMAND bash ${CMAKE_CURRENT_SOURCE_DIR}/test.sh ${f} ${LFITOOLS} ${CMAKE_CURRENT_SOURCE_DIR} ${ECCODES_LIB_DIR} ${CMAKE_BINARY_DIR})
endforeach()
