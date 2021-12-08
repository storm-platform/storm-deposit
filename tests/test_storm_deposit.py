# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import Flask

from storm_deposit import StormDeposit


def test_version():
    """Test version import."""
    from storm_deposit import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = StormDeposit(app)
    assert 'storm-deposit' in app.extensions

    app = Flask('testapp')
    ext = StormDeposit()
    assert 'storm-deposit' not in app.extensions
    ext.init_app(app)
    assert 'storm-deposit' in app.extensions


def test_view(base_client):
    """Test view."""
    res = base_client.get("/")
    assert res.status_code == 200
    assert 'Welcome to storm-deposit' in str(res.data)
