#!/usr/bin/python3

import pytest
from ape import accounts, project
from eip712.messages import EIP712Message


@pytest.fixture(scope="module")
def root():
    return ""


@pytest.fixture(scope="module")
def init_supply():
    return 10**18


@pytest.fixture(scope="module")
def deployer():
    return accounts.test_accounts[0]


@pytest.fixture(scope="module")
def alice():
    return accounts.test_accounts[1]


@pytest.fixture(scope="module")
def bob():
    return accounts.test_accounts[2]


@pytest.fixture(scope="module")
def charlie():
    return accounts.test_accounts[3]


@pytest.fixture(scope="module")
def token_metadata():
    return {"name": "Leviathan Points", "symbol": "SQUID"}


@pytest.fixture(scope="module")
def delegation_address():
    return "0x7267152C923789712f4518bC2A84b902D6a65A2C"


@pytest.fixture(scope="function")
def token(deployer, init_supply, delegation_address):
    token = project.Token.deploy(delegation_address, deployer, sender=deployer)
    token.mint(deployer, init_supply, sender=deployer)
    return token


@pytest.fixture(scope="function")
def Permit(chain, token):
    class Permit(EIP712Message):
        _name_: "string" = "Leviathan Points"
        _version_: "string" = "1.0"
        _chainId_: "uint256" = chain.chain_id
        _verifyingContract_: "address" = token.address

        owner: "address"
        spender: "address"
        value: "uint256"
        nonce: "uint256"
        deadline: "uint256"

    return Permit
