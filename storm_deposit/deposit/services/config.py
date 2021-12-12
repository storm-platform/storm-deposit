# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.services.components import (
    UserComponent,
    ProjectComponent,
)

from storm_deposit.deposit.schema import DepositObjectSchema
from invenio_records_resources.services.records.components import MetadataComponent

from storm_deposit.deposit.models.api import Deposit
from storm_deposit.deposit.services.permissions import DepositPermissionPolicy
from storm_deposit.deposit.services.components import (
    PipelineComponent,
    DepositServiceComponent,
    DepositStatusComponent,
)


class DepositManagementServiceConfig:
    """Deposit management service configuration."""

    #
    # Common configurations
    #
    permission_policy_cls = DepositPermissionPolicy

    #
    # Record configuration
    #
    record_cls = Deposit

    schema = DepositObjectSchema

    #
    # Components
    #
    components = [
        # Contextual components
        ProjectComponent,
        UserComponent,
        PipelineComponent,
        # Metadata components
        MetadataComponent,
        # Deposit components
        DepositServiceComponent,
        DepositStatusComponent,
    ]
