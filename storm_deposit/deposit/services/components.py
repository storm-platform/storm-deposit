# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.base.components import BaseServiceComponent
from invenio_records_resources.services.records.components import (
    ServiceComponent as ServiceComponentBase,
)

from storm_deposit.deposit.models.model import DepositStatus
from storm_pipeline.pipeline.records.api import ResearchPipeline


class PipelineComponent(ServiceComponentBase):
    """Service component which set the pipeline context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.pipelines.extend(
            [
                ResearchPipeline.pid.resolve(pipeline_id).model
                for pipeline_id in data.get("pipelines")
            ]
        )


class DepositStatusComponent(BaseServiceComponent):
    """Service component which set the deposit status in the record."""

    def start_deposit(self, identity, data=None, record=None, service=None, **kwargs):
        """Create handler."""
        record.status = DepositStatus.STARTING
