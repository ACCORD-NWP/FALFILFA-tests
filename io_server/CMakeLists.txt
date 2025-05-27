# (C) Copyright 2022- ECMWF.
# (C) Copyright 2022- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

if(HAVE_DOUBLE_PRECISION)
    set (LFITOOLS ${CMAKE_BINARY_DIR}/bin/lfitools_dp)
endif()

if(HAVE_SINGLE_PRECISION)
    set (LFITOOLS ${CMAKE_BINARY_DIR}/bin/lfitools_sp)
endif()

add_test(NAME "io_server"
    COMMAND bash ${CMAKE_CURRENT_SOURCE_DIR}/test.sh ${LFITOOLS} ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR})
