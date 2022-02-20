# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import request

import marshmallow as ma

from marshmallow_utils.fields import SanitizedUnicode
from storm_commons.plugins.validators import (
    marshmallow_validate_plugin_service,
    marshmallow_validate_custom_plugin_schema,
)


class DepositTaskObjectSchema(ma.Schema):
    """Deposit Object schema."""

    class Meta:
        unknown = ma.EXCLUDE

    # Deposit
    id = ma.fields.UUID(dump_only=True)
    status = ma.fields.Function(lambda obj: obj.status.value, dump_only=True)

    service = SanitizedUnicode(
        validate=lambda obj: marshmallow_validate_plugin_service("storm-deposit")(obj),
        required=True,
    )

    # Project
    project_id = ma.fields.Function(
        lambda obj: obj.project.data.get("id"), dump_only=True
    )

    # Workflow
    workflows = ma.fields.Function(
        lambda obj: list(map(lambda x: x.data.get("id"), obj.workflows)),
        lambda obj: obj,
        required=True,
    )

    # Custom metadata (Schema provided by the plugin services)
    customizations = ma.fields.Dict(
        required=False,
        validate=lambda obj: marshmallow_validate_custom_plugin_schema(
            "storm-deposit", request.json.get("service")
        )(data=obj)
        if obj.customizations
        else True,
    )


__all__ = "DepositObjectSchema"
