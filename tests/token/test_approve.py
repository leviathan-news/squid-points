#!/usr/bin/python3

def test_initial_approval_is_zero(token, alice, bob):
    assert token.allowance(alice, bob) == 0


def test_approve(token, alice, bob):
    token.approve(bob, 10**19, sender = alice)

    assert token.allowance(alice, bob) == 10**19


def test_modify_approve(token, alice, bob):
    token.approve(bob, 10**19, sender = alice)
    token.approve(bob, 12345678, sender = alice)

    assert token.allowance(alice, bob) == 12345678


def test_revoke_approve(token, alice, bob):
    token.approve(bob, 10**19, sender = alice)
    token.approve(bob, 0, sender = alice)

    assert token.allowance(alice, bob) == 0


def test_approve_self(token, alice, bob):
    token.approve(alice, 10**19, sender = alice)

    assert token.allowance(alice, alice) == 10**19


def test_only_affects_target(token, alice, bob):
    token.approve(bob, 10**19, sender = alice)

    assert token.allowance(bob, alice) == 0


def test_returns_true(token, alice, bob):
    tx = token.approve(bob, 10**19, sender = alice)

    assert tx.return_value is True


def test_approval_event_fires(token, alice, bob):
    tx = token.approve(bob, 10**19, sender = alice)

    assert len(tx.events) == 1
    assert tx.events[0]._owner == alice
    assert tx.events[0]._spender == bob
    assert tx.events[0]._value == 10 ** 19
