# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Deposit module for the Storm Platform."""

from storm_commons.plugins.manager import PluginManager
from storm_commons.plugins.factory import plugin_factory

from storm_deposit.deposit.resources.config import DepositManagementResourceConfig
from storm_deposit.deposit.resources.resource import DepositManagementResource
from storm_deposit.deposit.services.config import DepositManagementServiceConfig
from storm_deposit.deposit.services.service import DepositManagementService

from . import config


class StormDeposit(object):
    """storm-deposit extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        self.init_plugins(app)
        self.init_services(app)
        self.init_resources(app)

        app.extensions["storm-deposit"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            # if k.startswith("STORM_DEPOSIT_"):
            app.config.setdefault(k, getattr(config, k))

    def init_plugins(self, app):
        """Initialize the avaliable service plugins for the deposit operations."""
        available_plugin_services = plugin_factory(app, "storm_deposit.plugins")

        self.plugin_manager = PluginManager(available_plugin_services)

    def init_services(self, app):
        """Initialize the deposit management services."""
        self.deposit_management_service = DepositManagementService(
            self.plugin_manager, DepositManagementServiceConfig
        )

    def init_resources(self, app):
        """Initialize the deposit management resources."""
        self.deposit_management_resource = DepositManagementResource(
            DepositManagementResourceConfig, self.deposit_management_service
        )
