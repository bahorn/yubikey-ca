class ClientRevokeCmd:
    name = 'client-revoke'
    def __init__(self, subparser=None):
        if subparser:
            parser_client_revoke = subparser.add_parser(self.name)
            parser_client_revoke.add_argument('serial', nargs='+')

    def run(self, **kwargs):
        for serial in args.serial:
            with Shell() as sh:
                sh.run(*openssl_ca(sh), '-revoke', 'certs/%s.pem' % serial, stdout=None)
        ca_commit('SSL: Revokating certificates\n\nSerials: %s' % ', '.join(args.serial))

