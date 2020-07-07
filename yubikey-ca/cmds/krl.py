

class KRLCmd:

    name = 'krl'
    def __init__(self, subparser=None):
        if subparser:
            subparsers.add_parser(self.name)

    def run(self, **kwargs):
        krl_data = []
        with open('ssh-index.txt') as fd:
            for entry in fd:
                validity, serial, data = entry.strip().split(maxsplit=2)
                if validity == 'R':
                    krl_data.append('serial: %s' % serial.split(':')[1])
        with Shell() as sh:
            sh.run('ssh-keygen', '-k', '-f', sh.pipeout('krl'), '-s', sh.pipein(get_ssh_ca()), sh.pipein('\n'.join(krl_data).encode()), stdout=sys.stderr)
            sys.stdout.buffer.write(sh.out['krl'])
