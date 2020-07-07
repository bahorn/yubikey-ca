#!/usr/bin/python3

import argparse
import os

from cmds import cmds

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='action')

parser.add_argument('--pkcs11-module', '-m', default=os.getenv('PKCS11_MODULE', 'opensc-pkcs11.so'))
parser.add_argument('--pkcs11-url', '-u', default=os.getenv('PKCS11_URL', 'pkcs11:manufacturer=piv_II;id=%02'))
parser.add_argument('--path', '-p', default='.')
parser.add_argument('--debug', action='store_true')

# Add all the commands
initialized = {}
for cmd in cmds:
    initialized[cmd.name] = cmd(subparsers)

args = parser.parse_args()

if args.debug:
    os.environ['PKCS11SPY'] = args.pkcs11_module
    pkcs11_module = 'pkcs11-spy.so'
else:
    pkcs11_module = args.pkcs11_module

if args.action: initialized[args.action].run(args)
