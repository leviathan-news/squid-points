import ape
from ape.utils import misc


def test_admin_set_minter_works(token, alice):
    token.admin_set_minter(alice, sender = token.owner())
    assert token.minter() == alice


def test_admin_set_owner_works(token, alice):
    token.admin_set_owner(alice, sender = token.owner())
    assert token.owner() == alice


def test_admin_can_set_nft_addr(token):
    token.admin_set_npc_addr(misc.ZERO_ADDRESS, sender = token.owner())


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


def test_rando_cannot_set_nft_addr(token, charlie):
    with ape.reverts():
        token.admin_set_npc_addr(charlie, sender = charlie)


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
    tx = token.mint(alice, 10**18, {'from': deployer})
    event = tx.events['Transfer']
    assert event['sender'] == misc.ZERO_ADDRESS
    assert event['receiver'] == alice
    assert event['value'] == 10 ** 18

