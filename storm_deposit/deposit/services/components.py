# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records.components import ServiceComponent

from storm_project import current_project
from storm_pipeline.proxies import current_pipeline_service

from storm_deposit.deposit.models.model import DepositStatus


class ProjectComponent(ServiceComponent):
    """Service component which set the project context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.project_id = current_project._obj.model.id


class PipelineComponent(ServiceComponent):
    """Service component which set the pipeline context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.pipelines.extend(
            [
                current_pipeline_service.read(pipeline_id, identity)._obj.model
                for pipeline_id in data.get("pipelines")
            ]
        )


class DepositComponent(ServiceComponent):
    """Service component which set the pipelines associated with the deposit record."""

    def start_deposit(self, identity, data=None, record=None, service=None, **kwargs):
        """Start deposit handler."""
        if record:
            record.status = DepositStatus.QUEUED

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        if record and data:
            record.customizations = data.get("customizations") or {}

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""

        # defining the update strategies
        strategies = {
            "pipelines": lambda record, data: [
                current_pipeline_service.read(p_id, identity)._obj.model
                for p_id in data.get("pipelines", [])
            ],
            "service": lambda record, data: data.get("service"),
            "customizations": lambda record, data: data.get("customizations"),
        }

        for key in data.keys():
            if key in strategies:  # to avoid errors
                # using the strategy
                value = strategies.get(key)(record, data)

                # setting the returned value
                setattr(record, key, value)


__all__ = (
    "PipelineComponent",
    "ProjectComponent",
    "DepositComponent",
)
