import os
import subprocess

from storage.git import Storage

class InitCACmd:

    name = 'init-ca'
    def __init__(self, subparser):
        if subparser:
            subparser.add_parser(self.name)

    def run(self, args):
        return
        if not os.path.exists('.git'):
            subprocess.check_call(['git', 'init'])
        if not os.path.exists('certs'):
            os.mkdir('certs')
        for f in ('index.txt', 'index.txt.attr', 'ssh-index.txt', 'certs/.keep'):
            if not os.path.exists(f):
                with open(f, 'w+') as fd:
                    pass
        for f in ('crlnumber', 'serial'):
            if not os.path.exists(f):
                with open(f, 'w+') as fd:
                    fd.write('00\n')
        for f in ('index.txt', 'index.txt.attr', 'ssh-index.txt', 'certs', 'serial', 'crlnumber'):
            subprocess.check_call(['git', 'add', f])
        subprocess.check_output(['git', 'commit', '-m', 'CA initialization'])
