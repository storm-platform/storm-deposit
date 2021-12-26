# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import enum

from sqlalchemy import Enum
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils.types import JSONType, UUIDType

from invenio_db import db
from invenio_accounts.models import User as InvenioUser

from storm_commons.records.model import BaseRecordModel
from storm_project.project.records.models import ResearchProjectMetadata


# Deposit and pipeline relationship
deposit_pipeline_table = db.Table(
    "deposit_deposits_pipeline",
    db.Column(
        "deposit_id",
        UUIDType,
        db.ForeignKey("deposit_deposits.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "pipeline_id",
        UUIDType,
        db.ForeignKey("pipeline_research_pipelines.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class DepositStatus(enum.Enum):
    """Deposit status."""

    # General
    CREATED = "created"
    FINISHED = "finished"
    FAILED = "failed"
    QUEUED = "queued"

    RUNNING = "running"


class DepositModel(db.Model, BaseRecordModel):
    """Deposit database model."""

    __tablename__ = "deposit_deposits"

    #
    # Deposit
    #
    service = db.Column(db.String)

    status = db.Column(Enum(DepositStatus), default=DepositStatus.CREATED)

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
    # Related pipelines
    #
    pipelines = db.relationship(
        "ResearchPipelineMetadata", secondary=deposit_pipeline_table
    )

    #
    # Extra metadata
    #
    json = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=True,
    )
    """Store metadata in JSON format.

    When you create a new ``Record`` the ``json`` field value should never be
    ``NULL``. Default value is an empty dict. ``NULL`` value means that the
    record metadata has been deleted.

    This definition is extracted from ``invenio-records``
    (https://github.com/inveniosoftware/invenio-records/blob/bb4448a2c2abf448c3ba647590729cd6bc8478df/invenio_records/models.py#L69)
    """


__all__ = ("DepositModel", "DepositStatus")
