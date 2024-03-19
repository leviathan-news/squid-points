#!/usr/bin/python3

import pytest
from ape import (
    project,
    accounts
)



@pytest.fixture(scope="module")
def root():
    return ""


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

@pytest.fixture(scope="function")
def token(deployer):
    token = project.Token.deploy(sender= deployer)
    token.mint(deployer, 10**18, sender= deployer)
    return token




