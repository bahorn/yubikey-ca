
class InitKeyCmd:

    name = 'init-key'
    def __init__(self, subparser=None):
        if subparser:
            parser_init_key = subparsers.add_parser(self.name)
            parser_init_key.add_argument('--subject', '-s', default='/CN=Yubikey CA')
            parser_init_key.add_argument('--keyfile', '-k', default='/dev/stdin')
            parser_init_key.add_argument('--generate', '-g', action='store_true', help='Generate key on device')

    def run(self, args):

        if args.generate:
            pubkey = run('yubico-piv-tool', '-s9c', '-agenerate', '-ARSA2048')
            # Generate a temporary self-signed certificate in order to make openssl happy
            with Shell() as sh:
                cert = sh.run('yubico-piv-tool', '-s9c', '-averify', '-P%s' % get_pin(), '-aselfsign', '-i%s' % sh.pipein(pubkey), '-S/CN=TempCA')
            with Shell() as sh:
                sh.run('yubico-piv-tool', '-s9c', '-aimport-certificate', '-i%s' % sh.pipein(cert))
            # Selfsign with openssl now, in order to have CA in purposes
            with Shell() as sh:
                cert = sh.run('openssl', 'req', '-x509', '-days', '3650', '-sha256', '-subj', args.subject, '-engine', 'pkcs11',
                              '-keyform', 'engine', '-key', args.pkcs11_url, '-passin', 'pass:%s' % get_pin())
        else:
            key = open(args.keyfile, 'rb').read()
            with Shell() as sh:
                sh.run('yubico-piv-tool', '-s9c', '-aimport-key', '-i', sh.pipein(key))
            with Shell() as sh:
                cert = sh.run('openssl', 'req', '-x509', '-days', '3650', '-sha256', '-subj', args.subject, '-key', sh.pipein(key))
        with Shell() as sh:
            sh.run('yubico-piv-tool', '-s9c', '-aimport-certificate', '-i', sh.pipein(cert))
