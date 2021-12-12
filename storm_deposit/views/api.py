# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def create_deposit_management_blueprint_api(app):
    """Create the deposit management API blueprint."""
    ext = app.extensions["storm-deposit"]

    return ext.deposit_management_resource.as_blueprint()


__all__ = "create_deposit_management_blueprint_api"
