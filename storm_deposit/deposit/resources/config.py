# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import marshmallow as ma

from storm_commons.resources.config import ResourceConfigBase


class DepositManagementResourceConfig(ResourceConfigBase):
    """Deposit management resource config."""

    # Blueprint configuration.
    blueprint_name = "storm_deposit_deposits_management"

    # Request/Response configuration.
    request_view_args = {"deposit_id": ma.fields.Str()}

    # Routes configuration.
    url_prefix = "/projects/<project_id>/deposits"
    routes = {
        # Services operations
        "list-service": "/services",
        # Deposit operations
        "create-item": "",
        "list-item": "",
        "read-item": "/<deposit_id>",
        "update-item": "/<deposit_id>",
        "delete-item": "/<deposit_id>",
        # Deposit actions
        "deposit-item": "/<deposit_id>/actions/deposit",
    }
