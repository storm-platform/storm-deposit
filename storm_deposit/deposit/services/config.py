# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-deposit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.services.components import (
    UserComponent,
    RecordMetadataComponent,
    RecordServiceTypeComponent,
)

from storm_deposit.deposit.models.api import Deposit
from storm_deposit.deposit.schema import DepositObjectSchema

from storm_deposit.deposit.services.security.permissions import DepositPermissionPolicy
from storm_deposit.deposit.services.components import (
    PipelineComponent,
    DepositStatusComponent,
    ProjectComponent,
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
        RecordMetadataComponent,
        # Deposit components
        RecordServiceTypeComponent,
        DepositStatusComponent,
    ]
