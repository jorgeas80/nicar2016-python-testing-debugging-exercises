def parse_names(s):
    """
    Parse a comma-separated name string

    Args:
        s (string): Comma separated string representing a name in the
            format <last name>, <first name>, <middle name>, <suffix>

    Returns:
        Dictonary representing the name components. E.g.:

        {
          'first_name': "Ida",
          'last_name': "Wells",
          'middle_name': "B.",
          'suffix': "Jr.",
        }

    """
    bits = [bit.strip() for bit in s.split(',')]
    fields = ['last_name', 'first_name', 'middle_name', 'suffix']
    parsed = {field:None for field in fields}
    for i, bit in enumerate(bits):
        field_name = fields[i]
        parsed[field_name] = bit

    return parsed
