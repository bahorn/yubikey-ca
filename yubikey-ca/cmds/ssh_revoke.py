
class SSHRevokeCmd:
    name = 'ssh-revoke'
    def __init__(self, subparser=None):
        if subparser:
            parser_client_revoke = subparser.add_parser(self.name)
            parser_client_revoke.add_argument('serial', nargs='+')


    def run(self, **kawgs):
        serials = set("serial:%s" % s for s in args.serial)
        new_index = []
        with open('ssh-index.txt') as fd:
            for entry in fd:
                validity, serial, data = entry.strip().split(maxsplit=2)
                if serial in serials:
                    validity = 'R'
                    new_index.append("%s %s %s" % (validity, serial, data))
            with open('ssh-index.txt', 'w+') as fd:
                fd.write('\n'.join(new_index) + '\n')
            ca_commit('SSH: Revokating certificates\n\nSerials:\n%s\n' % '\n'.join(serials))

