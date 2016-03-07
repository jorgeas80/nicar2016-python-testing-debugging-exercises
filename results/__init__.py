import json

class SimpleResultLoader(object):
    def handle_result(self, result):
        return result

    def load(self, s):
        parsed = json.loads(s)
        return [self.handle_result(r) for r in parsed['results']]
