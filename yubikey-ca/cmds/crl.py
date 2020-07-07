class CRLCmd:
    name = 'crl'

    def __init__(self, subparser=None):
        if subparser:
            subparser.add_parser(self.name)

    def run(self, args):
        with Shell() as sh:
            sh.run(*openssl_ca(sh), '-gencrl', '-crldays', '3650', stdout=None)
        ca_commit('Issuing a new CRL')
