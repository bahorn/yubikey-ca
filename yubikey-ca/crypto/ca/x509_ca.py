ca_config = '\n'.join([
    'openssl_conf = openssl_init',
    '[ca]',
    'default_ca = ca_section',
    '[ca_section]',
    'database = ./index.txt',
    'crlnumber = ./crlnumber',
    'serial = ./serial',
    'new_certs_dir = ./certs',
    'crl = ./crl.pem',
    'unique_subject = no',
    'x509_extensions = usr_section',
    'default_md = sha256',
    'default_crl_days = 30',
    'policy = policy_section',
    '[policy_section]',
    'countryName = optional',
    'stateOrProvinceName = optional',
    'organizationName = optional',
    'organizationalUnitName = optional',
    'commonName = supplied',
    'emailAddress = optional',
    '[usr_section]',
    'basicConstraints=CA:FALSE',
    'nsCertType = client, email',
    '[openssl_init]',
    'engines = engine_section',
    '[engine_section]',
    'pkcs11 = pkcs11_section',
    '[pkcs11_section]',
    'engine_id = pkcs11',
    'MODULE_PATH = %s' % pkcs11_module,
    'init = 0',
    (args.debug and 'VERBOSE = EMPTY' or ''),
])

class X509CA(BaseCA):
    def __init__(self):
        pass

    def load(self):
        pass

    def generate(self):
        pass

    def get(self):
        pass
