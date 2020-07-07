def SSHCertCmd:

    name = 'ssh-cert'
    def __init__(self, subparser=None):
        if subparser:
            parser_ssh_cert = subparser.add_parser(self.name)
            parser_ssh_cert.add_argument('--principals', '-n', help='comma-separated list of principals (see CERTIFICATES in ssh-keygen)')
            parser_ssh_cert.add_argument('--id', '-I')
            parser_ssh_cert.add_argument('--options', '-O', action='append', default=[])
            parser_ssh_cert.add_argument('keyfile')

    def run(self, **kwargs):
        keyfile = args.keyfile
        if not keyfile.endswith('.pub') and os.path.exists(keyfile + '.pub'):
            keyfile += '.pub'

        with open(keyfile) as fd:
            pubkey = fd.read().strip()

        sshca = get_ssh_ca()
        if args.id:
            keyid = args.id
        else:
            keyid = pubkey.split(maxsplit=2)[2]
        serial = int(os.urandom(8).hex(), 16)
        with Shell() as sh:
            ssh_keygen_args = ['-s', sh.pipein(sshca), '-D', pkcs11_module, '-I', keyid, '-z', str(serial)]
            if args.principals:
                ssh_keygen_args.append('-n')
                ssh_keygen_args.append(args.principals)
            if args.options:
                for opt in args.options:
                    ssh_keygen_args.append('-O')
                    ssh_keygen_args.append(opt)
            ssh_keygen_args.append(keyfile)
            sys.stdout.buffer.write(sh.run('ssh-keygen', *ssh_keygen_args))
        pubkey_encoded = base64.b64encode(pubkey.encode()).decode()
        principals = (args.principals and args.principals) or ''
        now = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        with open('ssh-index.txt', 'a+') as fd:
            fd.write('V serial:{serial} added:{now} pub:{pubkey_encoded} principals:{principals} id:{keyid}\n'.format(**locals()))
        ca_commit('SSH: Issuing certificate  %s\n\nId: %s' % (serial, keyid))
