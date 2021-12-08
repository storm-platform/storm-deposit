# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import enum

from sqlalchemy import Enum
from sqlalchemy_utils.types import UUIDType

from invenio_db import db
from invenio_accounts.models import User as InvenioUser

from storm_project.project.records.models import ResearchProjectMetadata
from storm_pipeline.pipeline.records.models import ResearchPipelineMetadata

from storm_commons.records.base import BaseSQLAlchemyModel


class DepositStatus(enum.Enum):
    """Deposit status."""

    # General
    SENDING = "sending"
    FAILURE = "failure"
    PENDING = "pending"
    PUBLISHED = "published"


class DepositModel(db.Model, BaseSQLAlchemyModel):
    """Deposit database model."""

    __tablename__ = "deposit_deposits"

    #
    # Deposit status
    #
    status = db.Column(Enum(DepositStatus), default=DepositStatus.PENDING)

    #
    # Execution Job User owner
    #
    user_id = db.Column(db.Integer, db.ForeignKey(InvenioUser.id))
    user = db.relationship(InvenioUser)

    #
    # Associated project
    #
    project_id = db.Column(UUIDType, db.ForeignKey(ResearchProjectMetadata.id))
    project = db.relationship(ResearchProjectMetadata)

    #
    # Related pipeline
    #
    pipeline_id = db.Column(UUIDType, db.ForeignKey(ResearchPipelineMetadata.id))
    pipeline = db.relationship(ResearchPipelineMetadata)


__all__ = ("DepositModel", "DepositStatus")
