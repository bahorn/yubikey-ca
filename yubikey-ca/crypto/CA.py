
def get_ca_cert():
    return run('p11tool', '--provider=%s' % pkcs11_module, '--export', '%s;type=cert' % args.pkcs11_url).strip()+b"\n"

def get_ssh_ca():
    pubkey = run('openssl', 'x509', '-noout', '-pubkey', input=get_ca_cert())
    return run('ssh-keygen', '-i', '-m', 'PKCS8', '-f', '/dev/stdin', input=pubkey)

def openssl_ca(sh):
    return ('openssl', 'ca', '-config', sh.pipein(ca_config.encode()), '-engine', 'pkcs11', '-keyform', 'engine', '-batch',
            '-keyfile', args.pkcs11_url, '-passin', 'pass:%s' % get_pin(), '-cert', sh.pipein(get_ca_cert()))


