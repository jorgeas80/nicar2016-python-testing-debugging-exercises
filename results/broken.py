class BrokenChicagoResultsLoader(object):
    """
    Parse Chicago Board of Elections Results File.

    The file is in this format:

    Description                   Length Column Position

    Contest Code                  4      1-4
    Candidate Number              3      5-7
    # of Eligible Precincts       4      8-11
    Votes                         7      12-18
    # Completed precincts         4      19-22
    Party Abbreviation            3      23-25
    Political Subdivision Abbrev  7      26-32
    Contest name                  56     33-88
    Candidate Name                38     89-126
    Politicalcal subdivision name 25     127-151
    Vote For                      3      152-154

    """
    def load(self, path):
        results = []
        fields = [
            ('contest_code', 0, 4, str),    # Fixed. It was ('contest_code', 1, 4, str),
            ('candidate_number', 4, 3, str),
            ('num_eligible_precincts', 7, 4, int),
            ('votes', 11, 7, int),
            ('num_completed_precincts', 18, 4, int),
            ('party_abbreviation', 22, 3, str),
            ('political_subdivision_abbreviation', 25, 7, str),
            ('contest_name', 32, 56, str),
            ('candidate_name', 88, 38, str),
            ('political_subdivision_name', 126, 25, str),
            ('vote_for', 151, 3, int),
        ]
        with open(path, 'r') as f:
            for line in f:
                result = {}
                for field_name, field_start, field_length, parser in fields:
                    field_raw = line[field_start:field_start + field_length]
                    field_raw = field_raw.strip()
                    try:
                        result[field_name] = parser(field_raw)
                    except Exception:
                        # From the output of unittest, we know the error
                        # occurred with this call in the code.  Catch
                        # the exception and start the debugger
                        import sys
                        import pdb
                        exc_name, exc_value, exc_traceback = sys.exc_info()
                        pdb.post_mortem(exc_traceback)
                        # Once in the debugger, I'd use print() to look at some
                        # of the variables in the frame:
                        #
                        # > /Users/ghing/Dropbox/nicar2016/nicar2016-python-testing-debugging-excercises/results/broken.py(44)load()
                        # -> result[field_name] = parser(field_raw)
                        # (Pdb) l
                        #  44                             result[field_name] = parser(field_raw)
                        #  45                         except Exception:
                        #  46                             import sys
                        #  47                             import pdb
                        #  48                             exc_name, exc_value, exc_traceback = sys.exc_info()
                        #  49  ->                         pdb.post_mortem(exc_traceback)
                        #  50
                        #  51                     results.append(result)
                        #  52
                        #  53             return results
                        # [EOF]
                        # (Pdb) print(field_raw)
                        # Álvaro R. Obregón (Sanders)
                        # (Pdb) print(line)
                        # 0023012034800000000000DEM       Delegate, National Convention 4th DEM                   Álvaro R. Obregón (Sanders)           4th Congressional Distric005
                        #
                        # It looks like the issue is that there are non-ASCII
                        # characters in the data that we'll have to handle
                        # somehow

                results.append(result)

        return results
