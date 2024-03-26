#!/usr/bin/python3
from hexbytes import HexBytes
MULTISIG_ADDR = ''

def main():
    dev = accounts.load('dev')
    MODE = 'testnet'

    if MODE == 'testnet':
        delegation_registry = '0x7267152C923789712f4518bC2A84b902D6a65A2C'
    else:
        delegation_registry = '0xF5cA906f05cafa944c27c6881bed3DFd3a785b6A'

    owner = MULTISIG_ADDR
    token = project.Token.deploy(HexBytes(delegation_registry), owner, sender=dev, publish=True)
