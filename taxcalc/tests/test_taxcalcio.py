"""
Tests for Tax-Calculator TaxCalcIO class.
"""
# CODING-STYLE CHECKS:
# pep8 --ignore=E402 test_taxcalcio.py
# pylint --disable=locally-disabled test_taxcalcio.py

import os
import tempfile
import pytest
import pandas as pd
from taxcalc import TaxCalcIO, Growdiff  # pylint: disable=import-error


@pytest.fixture(scope='module', name='rawinputfile')
def fixture_rawinputfile():
    """
    Temporary input file that contains minimum required input variables.
    """
    ifile = tempfile.NamedTemporaryFile(suffix='.csv', mode='a', delete=False)
    contents = (
        u'RECID,MARS\n'
        u'    1,   2\n'
        u'    2,   1\n'
        u'    3,   4\n'
        u'    4,   3\n'
    )
    ifile.write(contents)
    ifile.close()
    # must close and then yield for Windows platform
    yield ifile
    if os.path.isfile(ifile.name):
        try:
            os.remove(ifile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='reformfile0')
def fixture_reformfile0():
    """
    Specify JSON reform file.
    """
    txt = """
    { "policy": {
        "_SS_Earnings_c": {"2016": [300000],
                           "2018": [500000],
                           "2020": [700000]}
      }
    }
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    rfile.write(txt + '\n')
    rfile.close()
    # Must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='assumpfile0')
def fixture_assumpfile0():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = """
    {
    "consumption": {},
    "behavior": {"_BE_sub": {"2020": [0.05]}},
    "growdiff_baseline": {},
    "growdiff_response": {"_ABOOK": {"2015": [-0.01]}}
    }
    """
    afile.write(contents)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='reformfile1')
def fixture_reformfile1():
    """
    Temporary reform file with .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = """
    { "policy": {
        "_AMT_brk1": { // top of first AMT tax bracket
          "2015": [200000],
          "2017": [300000]},
        "_EITC_c": { // max EITC amount by number of qualifying kids (0,1,2,3+)
          "2016": [[ 900, 5000,  8000,  9000]],
          "2019": [[1200, 7000, 10000, 12000]]},
        "_II_em": { // personal exemption amount (see indexing changes below)
          "2016": [6000],
          "2018": [7500],
          "2020": [9000]},
        "_II_em_cpi": { // personal exemption amount indexing status
          "2016": false, // values in future years are same as this year value
          "2018": true // values in future years indexed with this year as base
          },
        "_SS_Earnings_c": { // social security (OASDI) maximum taxable earnings
          "2016": [300000],
          "2018": [500000],
          "2020": [700000]},
        "_AMT_em_cpi": { // AMT exemption amount indexing status
          "2017": false, // values in future years are same as this year value
          "2020": true // values in future years indexed with this year as base
        }
      }
    }
    """
    rfile.write(contents)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='reformfilex1')
def fixture_reformfilex1():
    """
    Temporary reform file with .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = '{ "policy": {"_AMT_brk1": {"2015": [-1]}}}'
    rfile.write(contents)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='reformfilex2')
def fixture_reformfilex2():
    """
    Temporary reform file with .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = '{"policy": {"_AMT_bxk1": {"2015": [0]}}}'
    rfile.write(contents)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='assumpfile1')
def fixture_assumpfile1():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = """
    { "consumption": { "_MPC_e18400": {"2018": [0.05]} },
      "behavior": {},
      "growdiff_baseline": {},
      "growdiff_response": {}
    }
    """
    afile.write(contents)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='lumpsumreformfile')
def fixture_lumpsumreformfile():
    """
    Temporary reform file without .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    lumpsum_reform_contents = '{"policy": {"_LST": {"2013": [200]}}}'
    rfile.write(lumpsum_reform_contents)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='assumpfile2')
def fixture_assumpfile2():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    assump2_contents = """
    {
    "consumption": {},
    "behavior": {"_BE_sub": {"2020": [0.05]}},
    "growdiff_baseline": {},
    "growdiff_response": {}
    }
    """
    afile.write(assump2_contents)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='assumpfile3')
def fixture_assumpfile3():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = """
    {
    "consumption": {},
    "behavior": {},
    "growdiff_baseline": {},
    "growdiff_response": {"_ABOOK": {"2015": [-0.01]}},
    "growmodel": {}
    }
    """
    afile.write(contents)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='assumpfile4')
def fixture_assumpfile4():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = """
    {
    "consumption": {},
    "behavior": {"_BE_sub": {"2020": [0.05]}},
    "growdiff_baseline": {},
    "growdiff_response": {},
    "growmodel": {}
    }
    """
    afile.write(contents)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.mark.parametrize('input_data, reform, assump', [
    ('no-dot-csv-filename', 'no-dot-json-filename', 'no-dot-json-filename'),
    (list(), list(), list()),
    ('no-exist.csv', 'no-exist.json', 'no-exist.json'),
])
def test_ctor_errors(input_data, reform, assump):
    """
    Ensure error messages are generated by TaxCalcIO.__init__.
    """
    tcio = TaxCalcIO(input_data=input_data, tax_year=2013,
                     reform=reform, assump=assump)
    assert len(tcio.errmsg) > 0


@pytest.mark.parametrize('year, ref, asm, gdr', [
    (2000, 'reformfile0', 'assumpfile0', Growdiff()),
    (2099, 'reformfile0', None, None),
    (2020, 'reformfile0', None, dict()),
    (2020, 'reformfile0', 'assumpfile0', 'has_gdiff_response'),
    (2020, 'reformfilex1', 'assumpfile0', 'has_gdiff_response'),
    (2020, 'reformfilex2', 'assumpfile0', 'has_gdiff_response'),
    (2020, 'reformfile0', 'assumpfile3', None),
    (2020, 'reformfile0', 'assumpfile4', None),
])
def test_init_errors(reformfile0, reformfilex1, reformfilex2,
                     assumpfile0, assumpfile3, assumpfile4,
                     year, ref, asm, gdr):
    """
    Ensure error messages generated by TaxCalcIO.init method.
    """
    # pylint: disable=too-many-arguments,too-many-locals
    recdict = {'RECID': 1, 'MARS': 1, 'e00300': 100000, 's006': 1e8}
    recdf = pd.DataFrame(data=recdict, index=[0])
    if ref == 'reformfile0':
        reform = reformfile0.name
    elif ref == 'reformfilex1':
        reform = reformfilex1.name
    elif ref == 'reformfilex2':
        reform = reformfilex2.name
    else:
        reform = ref
    if asm == 'assumpfile0':
        assump = assumpfile0.name
    elif asm == 'assumpfile3':
        assump = assumpfile3.name
    elif asm == 'assumpfile4':
        assump = assumpfile4.name
    else:
        assump = asm
    if gdr == 'has_gdiff_response':
        gdiff_response = Growdiff()
        gdiff_response.update_growdiff({2015: {"_ABOOK": [-0.01]}})
    else:
        gdiff_response = gdr
    tcio = TaxCalcIO(input_data=recdf,
                     tax_year=year,
                     reform=reform,
                     assump=assump)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=recdf,
              tax_year=year,
              reform=reform,
              assump=assump,
              growdiff_response=gdiff_response,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) > 0


def test_creation_with_aging(rawinputfile, reformfile0):
    """
    Test TaxCalcIO instantiation with/without no policy reform and with aging.
    """
    taxyear = 2021
    tcio = TaxCalcIO(input_data=rawinputfile.name,
                     tax_year=taxyear,
                     reform=reformfile0.name,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=rawinputfile.name,
              tax_year=taxyear,
              reform=reformfile0.name,
              assump=None,
              growdiff_response=Growdiff(),
              aging_input_data=True,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    assert tcio.tax_year() == taxyear
    taxyear = 2016
    tcio = TaxCalcIO(input_data=rawinputfile.name,
                     tax_year=taxyear,
                     reform=None,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=rawinputfile.name,
              tax_year=taxyear,
              reform=None,
              assump=None,
              growdiff_response=None,
              aging_input_data=True,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    assert tcio.tax_year() == taxyear


def test_ctor_init_with_cps_files():
    """
    Test use of CPS input files.
    """
    # specify valid tax_year for cps.csv input data
    txyr = 2020
    tcio = TaxCalcIO('cps.csv', txyr, None, None)
    tcio.init('cps.csv', txyr, None, None,
              growdiff_response=None,
              aging_input_data=True,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    assert tcio.tax_year() == txyr
    # specify invalid tax_year for cps.csv input data
    txyr = 2013
    tcio = TaxCalcIO('cps.csv', txyr, None, None)
    tcio.init('cps.csv', txyr, None, None,
              growdiff_response=None,
              aging_input_data=True,
              exact_calculations=False)
    assert len(tcio.errmsg) > 0


def test_output_otions(rawinputfile, reformfile1, assumpfile1):
    """
    Test TaxCalcIO output_ceeu & output_dump options when writing_output_file.
    """
    taxyear = 2021
    tcio = TaxCalcIO(input_data=rawinputfile.name,
                     tax_year=taxyear,
                     reform=reformfile1.name,
                     assump=assumpfile1.name)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=rawinputfile.name,
              tax_year=taxyear,
              reform=reformfile1.name,
              assump=assumpfile1.name,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    outfilepath = tcio.output_filepath()
    # --ceeu output and standard output
    try:
        tcio.analyze(writing_output_file=True, output_ceeu=True)
    except:  # pylint: disable=bare-except
        if os.path.isfile(outfilepath):
            try:
                os.remove(outfilepath)
            except OSError:
                pass  # sometimes we can't remove a generated temporary file
        assert 'TaxCalcIO.analyze(ceeu)_ok' == 'no'
    # --dump output
    try:
        tcio.analyze(writing_output_file=True, output_dump=True)
    except:  # pylint: disable=bare-except
        if os.path.isfile(outfilepath):
            try:
                os.remove(outfilepath)
            except OSError:
                pass  # sometimes we can't remove a generated temporary file
        assert 'TaxCalcIO.analyze(dump)_ok' == 'no'
    # if tries were successful, remove output file and doc file
    if os.path.isfile(outfilepath):
        os.remove(outfilepath)
    docfilepath = outfilepath.replace('.csv', '-doc.text')
    if os.path.isfile(docfilepath):
        os.remove(docfilepath)


def test_sqldb_option(rawinputfile, reformfile1, assumpfile1):
    """
    Test TaxCalcIO output_sqldb option when not writing_output_file.
    """
    taxyear = 2021
    tcio = TaxCalcIO(input_data=rawinputfile.name,
                     tax_year=taxyear,
                     reform=reformfile1.name,
                     assump=assumpfile1.name)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=rawinputfile.name,
              tax_year=taxyear,
              reform=reformfile1.name,
              assump=assumpfile1.name,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    outfilepath = tcio.output_filepath()
    dbfilepath = outfilepath.replace('.csv', '.db')
    # --sqldb output
    try:
        tcio.analyze(writing_output_file=False, output_sqldb=True)
    except:  # pylint: disable=bare-except
        if os.path.isfile(dbfilepath):
            try:
                os.remove(dbfilepath)
            except OSError:
                pass  # sometimes we can't remove a generated temporary file
        assert 'TaxCalcIO.analyze(sqldb)_ok' == 'no'
    # if try was successful, remove the db file
    if os.path.isfile(dbfilepath):
        os.remove(dbfilepath)


def test_no_tables_or_graphs(reformfile1):
    """
    Test TaxCalcIO with output_tables=True and output_graphs=True but
    INPUT has zero weights.
    """
    # create input sample that cannot output tables or graphs
    nobs = 10
    idict = dict()
    idict['RECID'] = [i for i in range(1, nobs + 1)]
    idict['MARS'] = [2 for i in range(1, nobs + 1)]
    idict['s006'] = [0.0 for i in range(1, nobs + 1)]
    idict['e00300'] = [10000 * i for i in range(1, nobs + 1)]
    idict['expanded_income'] = idict['e00300']
    idf = pd.DataFrame(idict, columns=list(idict))
    # create and initialize TaxCalcIO object
    tcio = TaxCalcIO(input_data=idf,
                     tax_year=2020,
                     reform=reformfile1.name,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=idf,
              tax_year=2020,
              reform=reformfile1.name,
              assump=None,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    # create TaxCalcIO tables file
    tcio.analyze(writing_output_file=False,
                 output_tables=True,
                 output_graphs=True)
    # delete tables and graph files
    output_filename = tcio.output_filepath()
    fname = output_filename.replace('.csv', '-tab.text')
    if os.path.isfile(fname):
        os.remove(fname)
    fname = output_filename.replace('.csv', '-atr.html')
    if os.path.isfile(fname):
        os.remove(fname)
    fname = output_filename.replace('.csv', '-mtr.html')
    if os.path.isfile(fname):
        os.remove(fname)


def test_tables(reformfile1):
    """
    Test TaxCalcIO with output_tables=True and with positive weights.
    """
    # create tabable input
    nobs = 100
    idict = dict()
    idict['RECID'] = [i for i in range(1, nobs + 1)]
    idict['MARS'] = [2 for i in range(1, nobs + 1)]
    idict['s006'] = [10.0 for i in range(1, nobs + 1)]
    idict['e00300'] = [10000 * i for i in range(1, nobs + 1)]
    idict['expanded_income'] = idict['e00300']
    idf = pd.DataFrame(idict, columns=list(idict))
    # create and initialize TaxCalcIO object
    tcio = TaxCalcIO(input_data=idf,
                     tax_year=2020,
                     reform=reformfile1.name,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=idf,
              tax_year=2020,
              reform=reformfile1.name,
              assump=None,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    # create TaxCalcIO tables file
    tcio.analyze(writing_output_file=False, output_tables=True)
    # delete tables file
    output_filename = tcio.output_filepath()
    fname = output_filename.replace('.csv', '-tab.text')
    if os.path.isfile(fname):
        os.remove(fname)


def test_graphs(reformfile1):
    """
    Test TaxCalcIO with output_graphs=True.
    """
    # create graphable input
    nobs = 100
    idict = dict()
    idict['RECID'] = [i for i in range(1, nobs + 1)]
    idict['MARS'] = [2 for i in range(1, nobs + 1)]
    idict['s006'] = [10.0 for i in range(1, nobs + 1)]
    idict['e00300'] = [10000 * i for i in range(1, nobs + 1)]
    idict['expanded_income'] = idict['e00300']
    idf = pd.DataFrame(idict, columns=list(idict))
    # create and initialize TaxCalcIO object
    tcio = TaxCalcIO(input_data=idf,
                     tax_year=2020,
                     reform=reformfile1.name,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=idf,
              tax_year=2020,
              reform=reformfile1.name,
              assump=None,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    tcio.analyze(writing_output_file=False, output_graphs=True)
    # delete graph files
    output_filename = tcio.output_filepath()
    fname = output_filename.replace('.csv', '-atr.html')
    if os.path.isfile(fname):
        os.remove(fname)
    fname = output_filename.replace('.csv', '-mtr.html')
    if os.path.isfile(fname):
        os.remove(fname)


def test_ceeu_output1(lumpsumreformfile):
    """
    Test TaxCalcIO calculate method with no output writing using ceeu option.
    """
    taxyear = 2020
    recdict = {'RECID': 1, 'MARS': 1, 'e00300': 100000, 's006': 1e8}
    recdf = pd.DataFrame(data=recdict, index=[0])
    tcio = TaxCalcIO(input_data=recdf,
                     tax_year=taxyear,
                     reform=lumpsumreformfile.name,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=recdf,
              tax_year=taxyear,
              reform=lumpsumreformfile.name,
              assump=None,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    tcio.analyze(writing_output_file=False, output_ceeu=True)
    assert tcio.tax_year() == taxyear


def test_ceeu_output2():
    """
    Test TaxCalcIO calculate method with no output writing using ceeu option.
    """
    taxyear = 2020
    recdict = {'RECID': 1, 'MARS': 1, 'e00300': 100000, 's006': 1e8}
    recdf = pd.DataFrame(data=recdict, index=[0])
    tcio = TaxCalcIO(input_data=recdf,
                     tax_year=taxyear,
                     reform=None,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=recdf,
              tax_year=taxyear,
              reform=None,
              assump=None,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    tcio.analyze(writing_output_file=False, output_ceeu=True)
    assert tcio.tax_year() == taxyear


def test_ceeu_with_behavior(lumpsumreformfile, assumpfile2):
    """
    Test TaxCalcIO.analyze method when assuming behavior & doing ceeu calcs.
    """
    taxyear = 2020
    recdict = {'RECID': 1, 'MARS': 1, 'e00300': 100000, 's006': 1e8}
    recdf = pd.DataFrame(data=recdict, index=[0])
    tcio = TaxCalcIO(input_data=recdf,
                     tax_year=taxyear,
                     reform=lumpsumreformfile.name,
                     assump=assumpfile2.name)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=recdf,
              tax_year=taxyear,
              reform=lumpsumreformfile.name,
              assump=assumpfile2.name,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    tcio.analyze(writing_output_file=False, output_ceeu=True)
    assert tcio.tax_year() == taxyear


@pytest.fixture(scope='module', name='warnreformfile')
def fixture_warnreformfile():
    """
    Temporary reform file with .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = '{"policy": {"_STD_Dep": {"2015": [0]}}}'
    rfile.write(contents)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


def test_analyze_warnings_print(warnreformfile):
    """
    Test TaxCalcIO.analyze method when there is a reform warning.
    """
    taxyear = 2020
    recdict = {'RECID': 1, 'MARS': 1, 'e00300': 100000, 's006': 1e8}
    recdf = pd.DataFrame(data=recdict, index=[0])
    tcio = TaxCalcIO(input_data=recdf,
                     tax_year=taxyear,
                     reform=warnreformfile.name,
                     assump=None)
    assert len(tcio.errmsg) == 0
    tcio.init(input_data=recdf,
              tax_year=taxyear,
              reform=warnreformfile.name,
              assump=None,
              growdiff_response=None,
              aging_input_data=False,
              exact_calculations=False)
    assert len(tcio.errmsg) == 0
    tcio.analyze(writing_output_file=False, output_ceeu=False)
    assert tcio.tax_year() == taxyear


@pytest.fixture(scope='module', name='reformfile9')
def fixture_reformfile9():
    """
    Temporary reform file with .json extension.
    """
    rfile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = """
    { "policy": {
        "_SS_Earnings_c": {
          "2014": [300000],
          "2015": [500000],
          "2016": [700000]}
      }
    }
    """
    rfile.write(contents)
    rfile.close()
    # must close and then yield for Windows platform
    yield rfile
    if os.path.isfile(rfile.name):
        try:
            os.remove(rfile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


@pytest.fixture(scope='module', name='assumpfile9')
def fixture_assumpfile9():
    """
    Temporary assumption file with .json extension.
    """
    afile = tempfile.NamedTemporaryFile(suffix='.json', mode='a', delete=False)
    contents = """
    { "consumption": {},
      "behavior": {},
      "growdiff_baseline": {},
      "growdiff_response": {},
      "growmodel": {}
    }
    """
    afile.write(contents)
    afile.close()
    # must close and then yield for Windows platform
    yield afile
    if os.path.isfile(afile.name):
        try:
            os.remove(afile.name)
        except OSError:
            pass  # sometimes we can't remove a generated temporary file


def test_using_growmodel_is_false(assumpfile0):
    """
    Test TaxCalcIO.using_growmodel function calls that return False.
    """
    assert TaxCalcIO.using_growmodel(None) is False
    assert TaxCalcIO.using_growmodel(list()) is False
    assert TaxCalcIO.using_growmodel('unknown.json') is False
    assert TaxCalcIO.using_growmodel(assumpfile0.name) is False


def test_bad_growmodel_analysis(reformfile9, assumpfile9, assumpfile3):
    """
    Test incorrect TaxCalcIO.growmodel_analysis function calls.
    """
    # bad input_data type
    errmsg = TaxCalcIO.growmodel_analysis(input_data=list(),
                                          tax_year=2020,
                                          reform=reformfile9.name,
                                          assump=assumpfile9.name,
                                          aging_input_data=True,
                                          exact_calculations=False)
    assert len(errmsg) > 0
    # bad aging_input_data value
    errmsg = TaxCalcIO.growmodel_analysis(input_data='puf.csv',
                                          tax_year=2020,
                                          reform=reformfile9.name,
                                          assump=assumpfile9.name,
                                          aging_input_data=False,
                                          exact_calculations=False)
    assert len(errmsg) > 0
    # bad input_data value
    errmsg = TaxCalcIO.growmodel_analysis(input_data='bad.csv',
                                          tax_year=2020,
                                          reform=reformfile9.name,
                                          assump=assumpfile9.name,
                                          aging_input_data=True,
                                          exact_calculations=False)
    assert len(errmsg) > 0
    # bad tax_year (because is before first data year)
    errmsg = TaxCalcIO.growmodel_analysis(input_data='cps.csv',
                                          tax_year=2013,
                                          reform=reformfile9.name,
                                          assump=assumpfile9.name,
                                          aging_input_data=True,
                                          exact_calculations=False)
    assert len(errmsg) > 0
    # bad reform file name
    errmsg = TaxCalcIO.growmodel_analysis(input_data='cps.csv',
                                          tax_year=2020,
                                          reform='reform.bad',
                                          assump=assumpfile9.name,
                                          aging_input_data=True,
                                          exact_calculations=False)
    assert len(errmsg) > 0
    # bad assump value
    errmsg = TaxCalcIO.growmodel_analysis(input_data='cps.csv',
                                          tax_year=2020,
                                          reform=reformfile9.name,
                                          assump=assumpfile3.name,
                                          aging_input_data=True,
                                          exact_calculations=False)
    assert len(errmsg) > 0


def test_growmodel_analysis(reformfile9, assumpfile9):
    """
    Test TaxCalcIO.growmodel_analysis function with no output.
    """
    if TaxCalcIO.using_growmodel(assumpfile9.name):
        TaxCalcIO.growmodel_analysis(input_data='cps.csv',
                                     tax_year=2015,
                                     reform=reformfile9.name,
                                     assump=assumpfile9.name,
                                     aging_input_data=True,
                                     exact_calculations=False)
