Testing and Debugging News Applications in Python
=================================================

## Assumptions

* Python 2.7, because that's what is installed in the NICAR lab
* Git
* Know how to handle a Python exception with `try`/`except`.
* Know how to implement a Python class and class methods.

## Roadmap

* Running tests 
* Reading error messages 
* Unit testing
* Outputting debugging messages
* Debugging with pdb

## Getting started

Clone the this repository:

    git clone https://github.com/ghing/nicar2016-python-testing-debugging-exercises.git

All further commands will be run from the top-level of the checked-out local copy of the repository:

    cd nicar2016-python-testing-debugging-excercises


## Running tests

The Python standard library includes [unittest](https://docs.python.org/2/library/unittest.html), a unit testing framework.  We'll talk more about how to write tests soon, but first, let's learn how to run tests.  We're going to do this first because we'll interact with all the code we're going to write and fix in the excercises for this session through unit test cases.

Let's try running a module containing tests: 

    python -m unittest tests.test_basic

`unittest` is running tests in the module `tests.test_basic` (which can be found in the `tests/test_basic.py`) file in the current directory.

You should see output like:

    F..
    ======================================================================
    FAIL: test_true_is_true (tests.test_basic.FailingTestCase)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_basic.py", line 13, in test_true_is_true
        self.assertEqual(False, True)
    AssertionError: False != True

    ----------------------------------------------------------------------
    Ran 3 tests in 0.000s

    FAILED (failures=1)


You can run a specific test case:

    python -m unittest tests.test_basic.NoFailuresTestCase 

You should see output like this:

    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK

You can even run a specific test within a test case:

    python -m unittest tests.test_basic.NoFailuresTestCase.test_true_is_true

Output should look like this:

    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

## Reading an error message 

When there is an unhandled exception in your code, Python will display an error message and a **traceback**.  A traceback shows the code that was called leading up to an error. 

Here's an example traceback from the publishing tools we use for dynamic visualizations and interactives at the Chicago Tribune:

    Traceback (most recent call last):
      File "/usr/local/bin/tarbell", line 9, in <module>
        load_entry_point('tarbell==1.0.4', 'console_scripts', 'tarbell')()
      File "/usr/local/lib/python2.7/site-packages/tarbell/cli.py", line 74, in main
        command.__call__(command, args)
      File "/usr/local/lib/python2.7/site-packages/tarbell/cli.py", line 931, in __call__
        return self.fn(*args, **kw_args)
      File "/usr/local/lib/python2.7/site-packages/tarbell/cli.py", line 390, in tarbell_publish
        site.call_hook("publish", site, s3)
      File "/usr/local/lib/python2.7/site-packages/tarbell/app.py", line 359, in call_hook
        function.__call__(*args, **kwargs)
      File "/Users/abercrombiesmyth/tarbell/bears85/_blueprint/blueprint.py", line 115, in p2p_publish
        created, response = p2p_conn.create_or_update_content_item(content_item)
      File "/usr/local/lib/python2.7/site-packages/p2p/__init__.py", line 290, in create_or_update_content_item
        response = self.update_content_item(content_item)
      File "/usr/local/lib/python2.7/site-packages/p2p/__init__.py", line 252, in update_content_item
        resp = self.put_json("/content_items/%s.json" % slug, d)
      File "/usr/local/lib/python2.7/site-packages/p2p/__init__.py", line 727, in put_json
        return utils.parse_response(resp.json())
      File "/usr/local/lib/python2.7/site-packages/requests/models.py", line 763, in json
        return json.loads(self.text, **kwargs)
      File "/Library/Python/2.7/site-packages/simplejson/__init__.py", line 505, in loads
        return _default_decoder.decode(s)
      File "/Library/Python/2.7/site-packages/simplejson/decoder.py", line 370, in decode
        obj, end = self.raw_decode(s)
      File "/Library/Python/2.7/site-packages/simplejson/decoder.py", line 400, in raw_decode
        return self.scan_once(s, idx=_w(s, idx).end())
    simplejson.scanner.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

This traceback is rather long and involves a number of calls from Python modules in the project, the standard library and packages from PyPI.  Let's look at a simpler example to learn how to read an error message in Python.

Run the tests for a simple elections result loader:

    python -m unittest tests.test_result_loader

The tests fail, and show the following error output:

    E
    ======================================================================
    ERROR: test_load_bad_json (tests.test_result_loader.SimpleResultLoaderTestCase)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "tests/test_result_loader.py", line 13, in test_load_bad_json
        results = loader.load(sample_json)
      File "results/__init__.py", line 5, in load
        parsed = json.loads(s)
      File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/__init__.py", line 339, in loads
        return _default_decoder.decode(s)
      File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 364, in decode
        obj, end = self.raw_decode(s, idx=_w(s, 0).end())
      File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 382, in raw_decode
        raise ValueError("No JSON object could be decoded")
    ValueError: No JSON object could be decoded

    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    FAILED (errors=1)

The last line of the message is the exception that was raised:

    ValueError: No JSON object could be decoded

Prior to that, the traceback shows the calls leading up to and including the one that caused the error.  These are grouped in pairs of lines, where the first line shows the file name, line number and function name where the call occurred.  The second line in the pair shows the the code that was executed.

The call that raised the exception is shown as the last line in the traceback:

    File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 382, in raw_decode
      raise ValueError("No JSON object could be decoded")

The first line is the code where execution started:

    File "tests/test_result_loader.py", line 13, in test_load_bad_json
      results = loader.load(sample_json)

The execution that eventually caused the error starts in our test case.

Update the result loader so it catches the `ValueError` and returns an empty list.  From the traceback, can you see where we should look to fix our code?

## Unit testing

Unit testing is named because it involves testing the smallest possible "unit" in your code.  This usually means a function, procedure or method. This ensures that tests run quickly but also encourages us to organize our code in small, reusable pieces where each piece has a clear and specific purpose.

If you've ever had to repeatedly run a script that processes an entire data file to see if a bugfix worked, or walked through a multiple-step flow in a web application, you know how long this can take.  Unit testing lets us quickly know if our code works.

Consider `ApStyleNumbersTestCase.test_format_cardinal_number` in `tests/test_apstyle.py`:

    class ApStyleNumbersTestCase(unittest.TestCase):
        def test_format_cardinal_number(self):
            self.assertEqual(format_cardinal_number(1), "one")
            self.assertEqual(format_cardinal_number(10), "10")
            self.assertEqual(format_cardinal_number(1050), "1,050")
            self.assertEqual(format_cardinal_number(2000000), "2 million")

What's the "unit"?

You can see from the assertions that the test is calling `format_cardinal_number()` with different inputs and comparing the return value with expected results.  In this test, `format_cardinal_number()` is the "unit" under test.

### unittest

For this workshop, we're using Python's built in [unittest](https://docs.python.org/2/library/unittest.html) package.

Unittest is a framework that makes it easier to write, organize and run tests.  It provides tools for:

* test fixtures - set up an environment for testing.  This might involve creating a test database, reading test data from a file or instantiating an object used in multiple tests
* test cases - tests code against specified inputs
* test suites - a collection of test cases
* test discovery and running

Here are some basics for getting started with unittest:

* Create a module in a file named `test_<some_identifier_for_what_youre_testing>.py`
* Import `unittest`
* Create a subclass of `unittest.TestCase` 
* Implement tests as methods of your test case named `test_<some_identifier_for_the_unit_under_test>`

Assertions methods of `unittest.TestCase` help us check our expectations:

* assertEqual(a, b)
* assertNotEqual(a, b)
* assertTrue(x)
* assertFalse(x)
* assertIs(a, b)
* assertIsNot(a, b)
* assertIsNone(x)
* assertIn(a, b)
* assertNotIn(a, b)
* assertIsInstance(a, b)
* assertNotIsInstance(a, b)

For a full list of assertion methods see the [unittest.TestCase docs](https://docs.python.org/2/library/unittest.html#unittest.TestCase).

### Test driven development (TDD)

It's a good practice to write our tests *before we write the code that does stuff*.  We watch the tests fail and then implement our code until the tests pass.  This helps us think through the interface, design and behavior of our function or procedure before we implement our code.  It also means that we'll always have a test that will let us make sure that future changes to the code don't accidently break something else.

### Excercise: Let's write a test case

We're going to write a function called `parse_name()` that takes a string as an input.  The string will be a comma separated list of name components in the format "last,first,middle,suffix".  For example:

    Hing, Geoff, George

The function should return a dictionary with keys for each component.  For example:

    {
        "first_name": "Geoff",
        "last_name": "Hing",
        "middle_name": "George",
        "Suffix": None 
    }

Create a test case in `tests/test_names.py` with a test or tests for `parse_name()`.

Then, implement `parse_names()` so it passes the test.

## Writing testable code

To make our code easily testable, we should break pieces of functionality into separate functions, methods, classes an modules.  This lets us test each operation separately and quickly.

We should strive toward test-driven development, where we write tests first to define the "contract" between our code and its inputs and outputs.  However, in a newsroom environment, it can sometimes be difficult to rigorously follow disciplined software engineering practices.  Even when we don't write tests first, or write tests at all, it's a good practice to think about how you would test a piece of code.  If the answer to that question isn't clear, you might want to refactor the code.

### Exercise: refactoring to for better testing

`results.ChicagoResultsLoader` is a loader for the elections results feed of the [Chicago Board of Elections](http://www.chicagoelections.com/).  You can see the implementatin in `results/__init__.py`.  To run a very basic test of the results loader, run:

    python -m unittest tests.test_chicago_result_loader

You can see some results data in `tests/data/summary.txt`.

Surprise! On elections night, the Chicago Board of Elections removes the full-text of the race and candidate names (as well as other information) and only publishes the first fields.

So, instead of a row of data like:

    0079002206900000000000DEM       State's Attorney, Cook County                           Anita Alvarez                         Cook County              001

You get:

    0079002206900000000000

This will break our parsing logic.

We'll need to update our loader to handle this new case.  Since we're doing test driven development, we'll want to write our test(s) before we update our implementation.  However, the current tests operate on an entire row of data.

* Imagine how you would refactor the `load()` method to break out the parsing of a single line into its own method.  Let's call it `parse_result()`
* Write a test for that new method, taking into account both data formats
* Write the new method
* Update `load()` to use the new method

## Fixtures

Fixtures define the test environment.  This could include setting up a test database, loading test data from a file, creating dummy records, or instantiating an object used in multiple tests.

With the `unittest` framework, we create a fixture by implementing the `setUp()` method of our `TestCase` subclass.  If we need to do some cleanup after the tests have been run, implement the `tearDown()` method.

## Excercise: Fixtures

You've likely instantiated a new loader in each of the test methods in `tests.test_chicago_result_loader.TestChicagoResultLoader`.  Since our implementation of the loader doesn't store state, let's just instantiate one loader and reuse it in each of the test methods.

## Other kinds of testing

* Integration tests

## Next steps

* Mocks
* Continuous integration

## Knowing what's going on

While we strive to make our programs well behaved by writing tests, when we're handling a difficult problem, working with a poorly documented data format or API, or inheriting a code base from someone else (often without documentation or tests), we need to figure out what's going on in our program. 

## pprint

For many cases, `print()` works fine for displaying values in your code, but for complex data structures, the output can be difficult to read.  For example:

    >>> import json
    >>> with open('tests/data/ap_elections_loader_recording-1456935370.json') as f:
    ...     data = json.load(f)
    ...     print(data['races'][0])
    ...
    {u'raceTypeID': u'R', u'statePostal': u'FL', u'raceID': u'10673', u'national': True, u'officeName': u'President', u'lastUpdated': u'2016-03-02T15:42:49Z', u'candidates': [{u'candidateID': u'20408', u'last': u'Bush', u'polNum': u'14561', u'polID': u'1239', u'party': u'GOP', u'ballotOrder': 1, u'first': u'Jeb'}, {u'candidateID': u'20409', u'last': u'Carson', u'polNum': u'14562', u'polID': u'64509', u'party': u'GOP', u'ballotOrder': 2, u'first': u'Ben'}, {u'candidateID': u'20410', u'last': u'Christie', u'polNum': u'14563', u'polID': u'60051', u'party': u'GOP', u'ballotOrder': 3, u'first': u'Chris'}, {u'candidateID': u'20411', u'last': u'Cruz', u'polNum': u'14564', u'polID': u'61815', u'party': u'GOP', u'ballotOrder': 4, u'first': u'Ted'}, {u'candidateID': u'20414', u'last': u'Fiorina', u'polNum': u'14566', u'polID': u'60339', u'party': u'GOP', u'ballotOrder': 5, u'first': u'Carly'}, {u'candidateID': u'20416', u'last': u'Graham', u'polNum': u'14568', u'polID': u'1408', u'party': u'GOP', u'ballotOrder': 7, u'first': u'Lindsey'}, {u'abbrv': u'Huckabe', u'candidateID': u'20419', u'last': u'Huckabee', u'polNum': u'14569', u'polID': u'1187', u'party': u'GOP', u'ballotOrder': 8, u'first': u'Mike'}, {u'candidateID': u'20421', u'last': u'Kasich', u'polNum': u'14571', u'polID': u'36679', u'party': u'GOP', u'ballotOrder': 9, u'first': u'John'}, {u'candidateID': u'20423', u'last': u'Paul', u'polNum': u'14573', u'polID': u'60208', u'party': u'GOP', u'ballotOrder': 10, u'first': u'Rand'}, {u'candidateID': u'20425', u'last': u'Rubio', u'polNum': u'12082', u'polID': u'53044', u'party': u'GOP', u'ballotOrder': 11, u'first': u'Marco'}, {u'candidateID': u'20427', u'last': u'Santorum', u'polNum': u'13890', u'polID': u'1752', u'party': u'GOP', u'ballotOrder': 12, u'first': u'Rick'}, {u'candidateID': u'20428', u'last': u'Trump', u'polNum': u'14574', u'polID': u'8639', u'party': u'GOP', u'ballotOrder': 13, u'first': u'Donald'}, {u'candidateID': u'20429', u'last': u'Gilmore', u'polNum': u'14567', u'polID': u'45650', u'party': u'GOP', u'ballotOrder': 6, u'first': u'Jim'}], u'officeID': u'P', u'party': u'GOP'}

`pprint.pprint()` pretty prints the data structure making it much easier for us to inspect. 

    >>> import pprint
    >>> import json
    >>> with open('tests/data/ap_elections_loader_recording-1456935370.json') as f:
    ...     data = json.load(f)
    ...     pprint.pprint(data['races'][0])
    ...
    {u'candidates': [{u'ballotOrder': 1,
                      u'candidateID': u'20408',
                      u'first': u'Jeb',
                      u'last': u'Bush',
                      u'party': u'GOP',
                      u'polID': u'1239',
                      u'polNum': u'14561'},
                     {u'ballotOrder': 2,
                      u'candidateID': u'20409',
                      u'first': u'Ben',
                      u'last': u'Carson',
                      u'party': u'GOP',
                      u'polID': u'64509',
                      u'polNum': u'14562'},
                     {u'ballotOrder': 3,
                      u'candidateID': u'20410',
                      u'first': u'Chris',
                      u'last': u'Christie',
                      u'party': u'GOP',
                      u'polID': u'60051',
                      u'polNum': u'14563'},
                     {u'ballotOrder': 4,
                      u'candidateID': u'20411',
                      u'first': u'Ted',
                      u'last': u'Cruz',
                      u'party': u'GOP',
                      u'polID': u'61815',
                      u'polNum': u'14564'},
                     {u'ballotOrder': 5,
                      u'candidateID': u'20414',
                      u'first': u'Carly',
                      u'last': u'Fiorina',
                      u'party': u'GOP',
                      u'polID': u'60339',
                      u'polNum': u'14566'},
                     {u'ballotOrder': 7,
                      u'candidateID': u'20416',
                      u'first': u'Lindsey',
                      u'last': u'Graham',
                      u'party': u'GOP',
                      u'polID': u'1408',
                      u'polNum': u'14568'},
                     {u'abbrv': u'Huckabe',
                      u'ballotOrder': 8,
                      u'candidateID': u'20419',
                      u'first': u'Mike',
                      u'last': u'Huckabee',
                      u'party': u'GOP',
                      u'polID': u'1187',
                      u'polNum': u'14569'},
                     {u'ballotOrder': 9,
                      u'candidateID': u'20421',
                      u'first': u'John',
                      u'last': u'Kasich',
                      u'party': u'GOP',
                      u'polID': u'36679',
                      u'polNum': u'14571'},
                     {u'ballotOrder': 10,
                      u'candidateID': u'20423',
                      u'first': u'Rand',
                      u'last': u'Paul',
                      u'party': u'GOP',
                      u'polID': u'60208',
                      u'polNum': u'14573'},
                     {u'ballotOrder': 11,
                      u'candidateID': u'20425',
                      u'first': u'Marco',
                      u'last': u'Rubio',
                      u'party': u'GOP',
                      u'polID': u'53044',
                      u'polNum': u'12082'},
                     {u'ballotOrder': 12,
                      u'candidateID': u'20427',
                      u'first': u'Rick',
                      u'last': u'Santorum',
                      u'party': u'GOP',
                      u'polID': u'1752',
                      u'polNum': u'13890'},
                     {u'ballotOrder': 13,
                      u'candidateID': u'20428',
                      u'first': u'Donald',
                      u'last': u'Trump',
                      u'party': u'GOP',
                      u'polID': u'8639',
                      u'polNum': u'14574'},
                     {u'ballotOrder': 6,
                      u'candidateID': u'20429',
                      u'first': u'Jim',
                      u'last': u'Gilmore',
                      u'party': u'GOP',
                      u'polID': u'45650',
                      u'polNum': u'14567'}],
     u'lastUpdated': u'2016-03-02T15:42:49Z',
     u'national': True,
     u'officeID': u'P',
     u'officeName': u'President',
     u'party': u'GOP',
     u'raceID': u'10673',
     u'raceTypeID': u'R',
     u'statePostal': u'FL'}

## logging.debug

While using `print()` and `pprint.pprint()` can help us understand what's going on in our code, they become less useful if our code is outputting information to the console, or if it's running on a remote hosts where we don't have a console.

Luckily, the Python standard library includes the helpful, and relatively easy to use [`logging`](http://docs.python.org/library/logging) package which can give us more control over our debugging messages. 

The logging framework provides and lets users define a number of components, including:

* formatters - which control the format of the output log entries
* handlers - direct log entries to various destinations.  This could be the console, a file, email, syslog or a cloud-based log collection service.

While the full functionality of the `logging` package is beyond the scopeof this workshop, we can explore some of the package's most convenient features.

To use `logging`, we first need to import it.

    import logging

As a convenience, the `logging` package provides a "root logger" with some default configurations.  You can log a debug message to the root logger, by calling `logging.debug`.

    logging.debug("Logging to the root logger")

However the debug messages won't show up by default.  This is because the root logger defaults to only showing messages with a level of `logging.WARN` (in case you were wondering, the hierarchy of levels goes "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").  We need to set the log level of the root logger:

    logging.basicConfig(level=logging.DEBUG)

## Excercise: add logging using the root logger

Update `resuts.ChicagoResultsLoader.load()` to use the root logger to log the contest code, candidate number, votes and, if available, the contest name, candidate name and party.

## Creating loggers

Instead of using the root logger, we can instantiate a logger using `logging.getLogger()`. `logging.getLogger()` takes a `name` argument that specifies the component of your program where logging is happening.  This makes it easier to filter log messages.  It is conventional to use `__name__` to name the logger.

    logger = logging.getLogger(__name__)

We can then call `debug()` on our logger to log debugging messages.

    logger.debug("Testing logging debug messages")

You can set the base log level for the logger using the `setLevel()` method.

    logger.setLevel(logging.DEBUG)

You can also instantiate a new log handler.  For example, a [`FileHandler`](https://docs.python.org/2/library/logging.handlers.html#filehandler) will output log messages to a file.

    handler = logging.FileHandler('debug_log.txt')

And then add it to the logger:

    logger.addHandler(handler)

## Excercise: logging to a file

Update the `results` module to use a logger you instantiate instead of the root logger.  Configure the logger so that it will log debug messages to a file named `results_log.txt`.

### repr() methods in your classes


### Being explicit about assumptions with `assert`

### Debugging with pdb


    def get_race_name(cls, race):
        race_name = super(IllinoisAPAPIResultLoader, cls).get_race_name(race)
        race_name = race_name.replace("State House", "Illinois House")
        race_name = race_name.replace("State Senate", "Illinois Senate")
        if race.seatname and "County" in race.seatname and race_name.endswith(race.seatname):
            # Put the county name at the beginning of the race instead of the end
            # and remove county from the office name
            race_name = (race.seatname + " " +
                         race_name.replace(race.seatname, "")
                                  .replace("County", "").strip())

## Glossary

Unit test

Test case

Test suite

Exception: An unexpected error detected during program execution.  The [Errors and Exceptions](https://docs.python.org/2/tutorial/errors.html) section of the [Python Tutorial](https://docs.python.org/2/tutorial/) is a useful reference on exceptions.
