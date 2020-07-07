import sys

class CACertCmd:
    name = 'ca-cert'
    def __init__(self, subparser=None):
        if subparser:
            subparser.add_parser(self.name)

    def run(self, args):
        sys.stdout.buffer.write(get_ca_cert())
