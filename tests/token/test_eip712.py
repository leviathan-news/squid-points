#!/usr/bin/python3


def test_domain_separator_exists(token):
    assert token.DOMAIN_SEPARATOR() != "" and token.DOMAIN_SEPARATOR() is not None
