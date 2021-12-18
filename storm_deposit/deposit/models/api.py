# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.records.api import BaseRecordModelAPI
from invenio_records.systemfields import SystemFieldsMixin, ModelField

from storm_deposit.deposit.models.model import DepositModel


class Deposit(BaseRecordModelAPI, SystemFieldsMixin):
    """Deposit High-level API"""

    model_cls = DepositModel
    """SQLAlchemy model class defining which table stores the records."""

    # General status
    status = ModelField()
    service = ModelField()

    #
    # Creator
    #
    user = ModelField()
    user_id = ModelField()

    #
    # Associated project
    #
    project = ModelField()
    project_id = ModelField()

    #
    # Used pipeline
    #
    pipelines = ModelField()

    #
    # Extra metadata field
    #
    customizations = ModelField("json")

    is_deleted = ModelField()


__all__ = "Deposit"
