# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records.components import ServiceComponent

from storm_project import current_project
from storm_workflow.proxies import current_workflow_service

from storm_deposit.deposit.models.model import DepositTaskStatus


class ProjectComponent(ServiceComponent):
    """Service component which set the project context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.project_id = current_project._obj.model.id


class WorkflowComponent(ServiceComponent):
    """Service component which set the workflow context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.workflows.extend(
            [
                current_workflow_service.read(workflow_id, identity)._obj.model
                for workflow_id in data.get("workflows")
            ]
        )


class DepositComponent(ServiceComponent):
    """Service component which set the workflows associated with the deposit record."""

    def start_deposit(self, identity, data=None, record=None, service=None, **kwargs):
        """Start deposit handler."""
        if record:
            record.status = DepositTaskStatus.QUEUED

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        if record and data:
            record.customizations = data.get("customizations") or {}

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""

        # defining the update strategies
        strategies = {
            "workflows": lambda record, data: [
                current_workflow_service.read(p_id, identity)._obj.model
                for p_id in data.get("workflows", [])
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
    "WorkflowComponent",
    "ProjectComponent",
    "DepositComponent",
)
