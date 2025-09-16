#!/usr/bin/env python3

"""
Test the LFA low level python API
"""

import tempfile
import numpy
from falfilfa4py import LFA

data = {'float': numpy.arange(20, dtype=numpy.float64),
        'int': numpy.arange(25, dtype=numpy.int64),
        'char': numpy.array(['string', 'longlongstring'])
        }

LFA_MAX_NUM_FIELDS = 10
LFA_MAXSTRLEN = 20

with tempfile.NamedTemporaryFile() as f:

    #######################
    # Write test

    # open
    unit = LFA.wlfaouv(f.name, 'W')

    # write float
    LFA.wlfaecrr(unit, 'float', data['float'], len(data['float']))

    # write int
    LFA.wlfaecri(unit, 'int', data['int'], len(data['int']))

    # write char
    LFA.wlfaecrc(unit, 'char', data['char'], len(data['char']))

    # close
    LFA.wlfafer(unit)

    #######################
    # Read test

    # test and open
    assert LFA.wlfatest(f.name)
    unit = LFA.wlfaouv(f.name, 'R')

    # field list
    list_length, fieldslist = LFA.wlfalaft(unit,
                                           LFA_MAX_NUM_FIELDS,
                                           LFA_MAXSTRLEN)
    fieldslist = [fieldslist[i].strip().decode() for i in range(list_length)]
    assert list_length == len(data) and \
           all(k in fieldslist for k in data)

    # read float
    fieldtype, fieldlength = LFA.wlfacas(unit, 'float')
    assert fieldtype[0] == 'R' and fieldlength == len(data['float'])
    readdata, fieldlength = LFA.wlfalecr(unit, 'float', fieldlength)
    assert numpy.all(readdata == data['float']) and \
           fieldlength == len(data['float'])

    # read int
    fieldtype, fieldlength = LFA.wlfacas(unit, 'int')
    assert fieldtype[0] == 'I' and fieldlength == len(data['int'])
    readdata, fieldlength = LFA.wlfaleci(unit, 'int', fieldlength)
    assert numpy.all(readdata == data['int']) and \
           fieldlength == len(data['int'])

    # read char
    fieldtype, fieldlength = LFA.wlfacas(unit, 'char')
    assert fieldtype[0] == 'C' and fieldlength == len(data['char'])
    strlen = max(len(s) for s in data['char'])
    readdata, fieldlength = LFA.wlfalecc(unit, 'char', fieldlength, strlen)
    readdata = numpy.array([s.decode('utf-8') for s in readdata])
    assert numpy.all(readdata == data['char']) and \
           fieldlength == len(data['char'])

    # close
    LFA.wlfafer(unit)
