import unittest
import sys
import os
import time
from datetime import datetime
class TestRunner :
    def __init__ (self ,test_dir =None ,verbosity =2 ):
        self .test_dir =test_dir or os .path .dirname (__file__ )
        self .verbosity =verbosity
        self .results =[]
    def discover_tests (self ,pattern ='test_*.py'):
        loader =unittest .TestLoader ()
        suite =loader .discover (self .test_dir ,pattern =pattern )
        return suite
    def run_all (self ):
        suite =self .discover_tests ()
        return self ._run_suite (suite )
    def run_unit_tests (self ):
        suite =self .discover_tests ('test_unit_*.py')
        return self ._run_suite (suite )
    def run_integration_tests (self ):
        suite =self .discover_tests ('test_integration_*.py')
        return self ._run_suite (suite )
    def run_specific_test (self ,test_name ):
        loader =unittest .TestLoader ()
        suite =loader .loadTestsFromName (test_name )
        return self ._run_suite (suite )
    def _run_suite (self ,suite ):
        start_time =time .time ()
        runner =unittest .TextTestRunner (verbosity =self .verbosity )
        result =runner .run (suite )
        elapsed =time .time ()-start_time
        test_result ={
        'timestamp':datetime .now ().isoformat (),
        'duration':elapsed ,
        'tests_run':result .testsRun ,
        'failures':len (result .failures ),
        'errors':len (result .errors ),
        'skipped':len (result .skipped ),
        'success':result .wasSuccessful ()
        }
        self .results .append (test_result )
        return test_result
    def generate_report (self ):
        if not self .results :
            return "Тесты не запускались"
        report =[]
        report .append ("="*60 )
        report .append ("ОТЧЕТ О ТЕСТИРОВАНИИ")
        report .append ("="*60 )
        total_tests =sum (r ['tests_run']for r in self .results )
        total_failures =sum (r ['failures']for r in self .results )
        total_errors =sum (r ['errors']for r in self .results )
        total_duration =sum (r ['duration']for r in self .results )
        report .append (f"\nВсего тестов: {total_tests }")
        report .append (f"Успешных: {total_tests -total_failures -total_errors }")
        report .append (f"Провалено: {total_failures }")
        report .append (f"Ошибок: {total_errors }")
        report .append (f"Время: {total_duration :.2f}с")
        all_success =all (r ['success']for r in self .results )
        report .append (f"\nСтатус: {'✅ ПРОЙДЕНО'if all_success else '❌ НЕУДАЧА'}")
        return "\n".join (report )
class TestCase (unittest .TestCase ):
    @classmethod
    def setUpClass (cls ):
        pass
    @classmethod
    def tearDownClass (cls ):
        pass
    def setUp (self ):
        pass
    def tearDown (self ):
        pass
    def assertAlmostEqualDict (self ,d1 ,d2 ,places =7 ):
        self .assertEqual (set (d1 .keys ()),set (d2 .keys ()))
        for key in d1 :
            if isinstance (d1 [key ],float ):
                self .assertAlmostEqual (d1 [key ],d2 [key ],places =places )
            else :
                self .assertEqual (d1 [key ],d2 [key ])