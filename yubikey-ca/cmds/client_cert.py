
class ClientCertCmd:
    name = 'client-cert'
    def __init__(self, subparser=None):
        if subparser:
            parser_client_cert = subparser.add_parser(self.name)
            parser_client_cert.add_argument('--subject', '-s', require=True)
            parser_client_cert.add_argument('--keyfile', '-k', default='/dev/stdin')
            parser_client_cert.add_argument('--pkcs12', '-e', action='store_true')


    def run(self, **kwargs):
        key = open(args.keyfile, 'rb').read()
        with Shell() as sh:
            csr = sh.run('openssl', 'req', '-new', '-key', sh.pipein(key), '-sha256', '-days', '365', '-subj', args.subject)

        with open('serial') as fd:
            serial = fd.read()

        with Shell() as sh:
            cert = sh.run(*openssl_ca(sh), '-in', sh.pipein(csr), '-days', '365', '-notext')

        if args.pkcs12:
            with Shell() as sh:
                sh.run('openssl', 'pkcs12', '-export', '-in', sh.pipein(cert), '-inkey', sh.pipein(key), stdout=None)
        else:
            sys.stdout.buffer.write(cert)

        ca_commit('SSL: Issuing certificate %s\n\nSubject: %s' % (serial, args.subject))

