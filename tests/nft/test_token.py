import brownie
import pytest
from brownie import ZERO_ADDRESS, accounts, exceptions

#
# These tests are meant to be executed with brownie. To run them:
# brownie test
#

# Test the name method
def test_name(token, token_metadata):
    assert token.name() == token_metadata["name"]


# Test the symbol
def test_symbol(token, token_metadata):
    assert token.symbol() == token_metadata["symbol"]


# Test balanceOf - initially, the entire supply should be
def test_balanceOf(minted, alice, npc, minted_token_id):
    assert npc.ownerOf(minted_token_id) == alice
    assert npc.balanceOf(alice.address) == npc.totalSupply()


# Test a valid transfer
def test_transfer(minted, alice, bob, npc, minted_token_id):
    token = npc
    init_bal_alice = token.balanceOf(alice)
    init_bal_bob = token.balanceOf(bob)

    txn_receipt = token.transferFrom(alice, bob, minted_token_id, {"from": alice})
    assert init_bal_alice - 1 == token.balanceOf(alice)
    assert init_bal_bob + 1 == token.balanceOf(bob)

    # Verify that event has been emitted
    event = txn_receipt.events["Transfer"]
    assert event["_from"] == alice
    assert event["_to"] == bob
    assert event["_tokenId"] == minted_token_id


# Test an unauthorized transferFrom
def test_transfer_nonowner(minted, alice, bob, npc):
    token = npc
    old_balance_alice = token.balanceOf(alice)
    old_balance_bob = token.balanceOf(bob)

    with brownie.reverts():  # "ERC721: transfer caller is not owner nor approved"):
        token.transferFrom(alice, bob, 1, {"from": bob})
    assert token.balanceOf(alice) == old_balance_alice
    assert token.balanceOf(bob) == old_balance_bob


# Test a transfer with no balance
def test_transfer_nobalance(token, alice, bob):

    old_balance_alice = token.balanceOf(alice)
    old_balance_bob = token.balanceOf(bob)

    with brownie.reverts():
        token.transferFrom(alice, bob, 1, {"from": bob})


# Test approval
def test_approve(minted, alice, bob, npc, minted_token_id):
    # Allow bob to spend 100 token on my behalf
    txn_receipt = npc.approve(bob, minted_token_id, {"from": alice})

    # Verify that event has been emitted
    event = txn_receipt.events["Approval"]
    assert event["_owner"] == alice
    assert event["_approved"] == bob
    assert event["_tokenId"] == minted_token_id

    # Check
    assert npc.getApproved(minted_token_id) == bob


# Test approval - overwrite old value
def test_approve_overwrite(minted, alice, bob, charlie, npc, minted_token_id):

    # Allow bob to spend 100 npc on my behalf
    npc.approve(bob, minted_token_id, {"from": alice})

    # Check
    assert npc.getApproved(minted_token_id) == bob

    # Overwrite
    npc.approve(charlie, minted_token_id, {"from": alice})
    assert npc.getApproved(minted_token_id) == charlie


def test_cannot_approve_owner(minted, alice, bob, npc, minted_token_id):

    # Allow bob to spend 100 npc on my behalf
    npc.approve(bob, minted_token_id, {"from": alice})

    # Check
    assert npc.getApproved(minted_token_id) == bob

    # Overwrite
    with brownie.reverts():  # "ERC721: approval to current owner"):
        npc.approve(alice, minted_token_id, {"from": alice})


# Test a valid withdrawal
def test_transferFrom(minted, alice, bob, npc, minted_token_id):
    init_balance_alice = npc.balanceOf(alice)
    init_balance_bob = npc.balanceOf(bob)

    # Authorize bob
    npc.approve(bob, minted_token_id, {"from": alice})
    txn_receipt = npc.transferFrom(alice, bob, minted_token_id, {"from": bob})
    assert init_balance_alice - 1 == npc.balanceOf(alice)
    assert init_balance_bob + 1 == npc.balanceOf(bob)

    # Verify that event has been emitted
    event = txn_receipt.events["Transfer"]
    assert event["_from"] == alice
    assert event["_to"] == bob
    assert event["_tokenId"] == minted_token_id

    # Verify that the approval has been set to ZERO_ADDRESS
    assert npc.getApproved(minted_token_id) == ZERO_ADDRESS
