import codecs
import logging
import json

from .broken import BrokenChicagoResultsLoader

# If you wanted to just use the root logger, do this:
# logging.basicConfig(level=logging.DEBUG)

# But, we're going to make our own logger
logger = logging.getLogger(__name__)
# And set its minimum level to DEBUG so we'll capture
# the debug messages in our code
logger.setLevel(logging.DEBUG)

# And make a handler that sends log messages to a file 
handler = logging.FileHandler('results_log.txt')
logger.addHandler(handler)

class SimpleResultLoader(object):
    def handle_result(self, result):
        return result

    def load(self, s):
        try:
            parsed = json.loads(s)
        except ValueError:
            return []

        return [self.handle_result(r) for r in parsed['results']]


class ChicagoResultsLoader(object):
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

    def parse_result(self, line):
        fields = [
            ('contest_code', 0, 4, unicode),
            ('candidate_number', 4, 3, unicode),
            ('num_eligible_precincts', 7, 4, int),
            ('votes', 11, 7, int),
            ('num_completed_precincts', 18, 4, int),
            ('party_abbreviation', 22, 3, unicode),
            ('political_subdivision_abbreviation', 25, 7, unicode),
            ('contest_name', 32, 56, unicode),
            ('candidate_name', 88, 38, unicode),
            ('political_subdivision_name', 126, 25, unicode),
            ('vote_for', 151, 3, int),
        ]

        result = {}

        line_len = len(line) 
        for field_name, field_start, field_length, parser in fields:
            if field_start >= line_len:
                break

            field_raw = line[field_start:field_start + field_length]
            field_raw = field_raw.strip()
            result[field_name] = parser(field_raw)

        return result    

    def load(self, path):
        results = []
        with codecs.open(path, 'r', 'utf-8') as f:
            for line in f:
                result = self.parse_result(line)
                results.append(result)
                if 'candidate_name' in result:
                    msg = (u"Parsed result for candidate {} ({}), {} party, in race {} ({}) "
                           "with {} votes").format(
                                result['candidate_name'],
                                result['candidate_number'],
                                result['party_abbreviation'] or 'no',
                                result['contest_name'],
                                result['contest_code'],
                                result['votes'])
                            
                else:
                    msg = (u"Parsed result for candidate number {} in race with "
                            "id {} with {} votes").format(
                                result['candidate_number'],
                                result['contest_code'],
                                result['votes'])
                            
                # If you just want to debug messages to the root logger, do
                # this:
                # logging.debug(msg)

                # But we'll use our own logger
                logger.debug(msg)

        return results
