# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

from marshmallow import fields
from storm_commons.resources.args import BaseSearchRequestArgsSchema


class DepositSearchRequestArgsSchema(BaseSearchRequestArgsSchema):
    """Request URL query string arguments."""

    id = fields.UUID()
    status = fields.String()

    service = fields.String()
    project_id = fields.String()
    workflows = fields.String()
