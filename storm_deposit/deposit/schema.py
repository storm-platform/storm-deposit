# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from flask_marshmallow import Marshmallow

from marshmallow_utils.fields import SanitizedUnicode
from storm_commons.schemas.validators import marshmallow_not_blank_field

ma = Marshmallow()


class DepositObjectSchema(ma.Schema):
    """Deposit Object schema."""

    class Meta:
        # Fields to expose
        fields = (
            "id",
            "service",
            "status",
            "pipelines",
            "links",
        )

    # Deposit
    id = ma.UUID(dump_only=True)
    status = ma.Function(lambda obj: obj.status.value, dump_only=True)

    service = SanitizedUnicode(validate=marshmallow_not_blank_field(), required=True)

    # Project
    project_id = ma.Function(lambda obj: obj.project.data.get("id"), dump_only=True)

    # Pipeline
    pipelines = ma.Function(
        lambda obj: list(map(lambda x: x.data.get("id"), obj.pipelines)),
        lambda obj: obj,
        required=True,
    )

    links = ma.Hyperlinks(
        {
            "self": ma.AbsoluteURLFor(
                "storm_deposits_management.read",
                values=dict(
                    _scheme="https", deposit_id="<id>", project_id="<project.data.id>"
                ),
            )
        }
    )


__all__ = "DepositObjectSchema"
