#!/bin/bash
# (C) Copyright 2022- ECMWF.
# (C) Copyright 2022- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

set -e
set -x

LFITOOLS=$1
p=$2
build_dir=$3

test_name=$(basename $p)
 
cd $build_dir
mkdir -p tests_results

cd tests_results

\rm -rf $test_name
mkdir -p $test_name
cd $test_name

export DR_HOOK_NOT_MPI=1

ulimit -s unlimited

export LFITOOLS=$1

$LFITOOLS lfitestformat --nopts 10000 --lfi-file LFITEST
$LFITOOLS lfilist LFITEST > LFITEST.list
diff $p/ref/LFITEST.list LFITEST.list
