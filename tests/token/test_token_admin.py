import ape
from ape.utils import misc
from ape import accounts

def test_admin_set_minter_works(token, alice):
    with accounts.use_sender(token.owner()):
        token.admin_set_minter(alice)
    assert token.minter() == alice


def test_admin_set_owner_works(token, alice):
    with accounts.use_sender(token.owner()):
        token.admin_set_owner(alice)
    assert token.owner() == alice


def test_owner_can_mint(token, deployer, alice, bob):
    assert token.balanceOf(alice) == 0
    # Set unique minter/owner address to test
    token.admin_set_owner(bob, sender = deployer)
    token.mint(alice, 10**18, sender = bob)
    assert token.balanceOf(alice) == 10**18


def test_minter_can_mint(token, deployer, alice, bob):
    assert token.balanceOf(alice) == 0
    # Set unique minter/owner address to test
    token.admin_set_minter(bob, sender = deployer)
    token.mint(alice, 10**18, sender = bob)
    assert token.balanceOf(alice) == 10**18


def test_rando_cannot_mint(token, alice, bob):
    with ape.reverts():
        token.mint(alice, 10**18, sender = bob)


def test_rando_cannot_admin_set_owner(token, charlie):
    with ape.reverts():
        token.admin_set_owner(charlie, sender = charlie)


def test_rando_cannot_admin_set_minter(token, charlie):
    with ape.reverts():
        token.admin_set_minter(charlie, sender = charlie)


def test_rando_cannot_mint(token, charlie):
    with ape.reverts():
        token.mint(charlie, 10**18, sender = charlie)


def test_cannot_burn(token, alice, deployer):
    token.mint(alice, 10**18, sender = deployer)
    assert token.balanceOf(alice) == 10**18
    with ape.reverts():
        token.transfer(misc.ZERO_ADDRESS, 10**18, sender = alice)
    assert token.balanceOf(alice) == 10**18


def test_mint_fires_event(token, alice, deployer):
    tx = token.mint(alice, 10**18, sender = deployer)
    event = tx.events
    assert event[0].sender == misc.ZERO_ADDRESS
    assert event[0].receiver == alice
    assert event[0].value == 10 ** 18

