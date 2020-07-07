import sys

class SSHCACmd:
    name = 'ssh-ca'
    def __init__(self, subparser=None):
        if subparser:
            subparser.add_parser(self.name)

    def run(self, **kwargs):
        sys.stdout.buffer.write(get_ssh_ca())
