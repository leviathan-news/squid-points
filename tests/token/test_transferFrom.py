#!/usr/bin/python3
import ape


def test_sender_balance_decreases(alice, bob, charlie, token):
    sender_balance = token.balanceOf(alice)
    amount = sender_balance // 4

    token.approve(bob, amount, sender=alice)
    token.transferFrom(alice, charlie, amount, sender=bob)

    assert token.balanceOf(alice) == sender_balance - amount


def test_receiver_balance_increases(alice, bob, charlie, token):
    receiver_balance = token.balanceOf(charlie)
    amount = token.balanceOf(alice) // 4

    token.approve(bob, amount, sender=alice)
    token.transferFrom(alice, charlie, amount, sender=bob)

    assert token.balanceOf(charlie) == receiver_balance + amount


def test_caller_balance_not_affected(alice, bob, charlie, token):
    caller_balance = token.balanceOf(bob)
    amount = token.balanceOf(alice)

    token.approve(bob, amount, sender=alice)
    token.transferFrom(alice, charlie, amount, sender=bob)

    assert token.balanceOf(bob) == caller_balance


def test_caller_approval_affected(alice, bob, charlie, token):
    approval_amount = token.balanceOf(alice)
    transfer_amount = approval_amount // 4

    token.approve(bob, approval_amount, sender=alice)
    token.transferFrom(alice, charlie, transfer_amount, sender=bob)

    assert token.allowance(alice, bob) == approval_amount - transfer_amount


def test_receiver_approval_not_affected(alice, bob, charlie, token):
    approval_amount = token.balanceOf(alice)
    transfer_amount = approval_amount // 4

    token.approve(bob, approval_amount, sender=alice)
    token.approve(charlie, approval_amount, sender=alice)
    token.transferFrom(alice, charlie, transfer_amount, sender=bob)

    assert token.allowance(alice, charlie) == approval_amount


def test_total_supply_not_affected(alice, bob, charlie, token):
    total_supply = token.totalSupply()
    amount = token.balanceOf(alice)

    token.approve(bob, amount, sender=alice)
    token.transferFrom(alice, charlie, amount, sender=bob)

    assert token.totalSupply() == total_supply


def test_returns_true(alice, bob, charlie, token):
    amount = token.balanceOf(alice)
    token.approve(bob, amount, sender=alice)
    tx = token.transferFrom(alice, charlie, amount, sender=bob)

    assert tx.return_value is True


def test_transfer_full_balance(alice, bob, charlie, token):
    amount = token.balanceOf(alice)
    receiver_balance = token.balanceOf(charlie)

    token.approve(bob, amount, sender=alice)
    token.transferFrom(alice, charlie, amount, sender=bob)

    assert token.balanceOf(alice) == 0
    assert token.balanceOf(charlie) == receiver_balance + amount


def test_transfer_zero_tokens(alice, bob, charlie, token):
    sender_balance = token.balanceOf(alice)
    receiver_balance = token.balanceOf(charlie)

    token.approve(bob, sender_balance, sender=alice)
    token.transferFrom(alice, charlie, 0, sender=bob)

    assert token.balanceOf(alice) == sender_balance
    assert token.balanceOf(charlie) == receiver_balance


def test_transfer_zero_tokens_without_approval(alice, bob, charlie, token):
    sender_balance = token.balanceOf(alice)
    receiver_balance = token.balanceOf(charlie)

    token.transferFrom(alice, charlie, 0, sender=bob)

    assert token.balanceOf(alice) == sender_balance
    assert token.balanceOf(charlie) == receiver_balance


def test_insufficient_balance(alice, bob, charlie, token):
    balance = token.balanceOf(alice)

    token.approve(bob, balance + 1, sender=alice)
    with ape.reverts():
        token.transferFrom(alice, charlie, balance + 1, sender=bob)


def test_insufficient_approval(deployer, bob, charlie, token):
    balance = token.balanceOf(deployer)

    token.approve(bob, balance - 1, sender=deployer)
    with ape.reverts():
        token.transferFrom(deployer, charlie, balance, sender=bob)


def test_no_approval_transfer_fails(deployer, bob, charlie, token):
    balance = token.balanceOf(deployer)

    assert token.allowance(deployer, bob) == 0
    assert balance > 0

    with ape.reverts():
        token.transferFrom(deployer, charlie, balance, sender=bob)


def test_revoked_approval(deployer, bob, charlie, token):
    balance = token.balanceOf(deployer)

    token.approve(bob, balance, sender=deployer)
    token.approve(bob, 0, sender=deployer)

    with ape.reverts():
        token.transferFrom(deployer, charlie, balance, sender=bob)


def test_transfer_to_self(deployer, bob, charlie, token):
    sender_balance = token.balanceOf(deployer)
    amount = sender_balance // 4

    token.approve(deployer, sender_balance, sender=deployer)
    token.transferFrom(deployer, deployer, amount, sender=deployer)

    assert token.balanceOf(deployer) == sender_balance
    assert token.allowance(deployer, deployer) == sender_balance - amount


def test_transfer_to_self_no_approval(deployer, bob, charlie, token):
    amount = token.balanceOf(deployer)

    with ape.reverts():
        token.transferFrom(deployer, deployer, amount, sender=deployer)


def test_transfer_event_fires(deployer, bob, charlie, token):
    amount = token.balanceOf(deployer)

    token.approve(bob, amount, sender=deployer)
    tx = token.transferFrom(deployer, charlie, amount, sender=bob)

    assert len(tx.events) == 1
    assert tx.events[0]._from == deployer
    assert tx.events[0]._to == charlie
    assert tx.events[0]._value == amount
