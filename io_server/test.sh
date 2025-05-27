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

export LFITOOLS=$1
p=$2
src_dir=$3
build_dir=$4

test_name=$(basename $p)

cd $build_dir
mkdir -p tests_results

cd tests_results

\rm -rf $test_name
mkdir -p $test_name
cd $test_name

export DR_HOOK_NOT_MPI=1

ulimit -s unlimited

cp -r $p/t0031/* .

for f in lfi_ io_poll
do
  cp $src_dir/share/$f .
  chmod +x $f
done

./lfi_

export PATH=$PWD:$PATH

./io_poll --prefix ICMSH   > list.ICMSH
./io_poll --prefix GRIBPF  > list.GRIBPF

diff list.ICMSH  $p/t0031/ref/list.ICMSH
diff list.GRIBPF $p/t0031/ref/list.GRIBPF

for f in $(cat list.ICMSH)
do
  $LFITOOLS lfidiff --lfi-file-1 $f --lfi-file-2 $p/t0031/ref/$f
done

