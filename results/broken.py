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
            ('contest_code', 1, 4, str),
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
                    result[field_name] = parser(field_raw)

                results.append(result)

        return results
